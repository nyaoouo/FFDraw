import importlib
import json
import logging
import os
import pathlib
import pkgutil
import sys
import threading

import aiohttp.web
import glm
import requests

from fpt4.utils.sqpack import SqPack

try:
    import aiohttp_cors
except ImportError:
    use_aiohttp_cors = False
else:
    use_aiohttp_cors = True

from . import gui, omen, mem, func_parser, plugins, update
from .sniffer import sniffer_main as sniffer

default_cn = bool(os.environ.get('DefaultCn'))


class FFDraw:
    omens: dict[int, omen.BaseOmen]
    logger = logging.getLogger('FFDraw')
    plugins: 'dict[str,plugins.FFDrawPlugin]'
    instance: 'FFDraw' = None

    def __init__(self, pid: int):
        FFDraw.instance = self
        self.app_data_path = pathlib.Path(os.environ['ExcPath']) / 'AppData'
        self.cfg_path = self.app_data_path / 'config.json'
        self.config = json.loads(self.cfg_path.read_text('utf-8')) if self.cfg_path.exists() else {}
        self.rpc_password = self.config.setdefault('rpc_password', '')
        if default_cn:
            self.path_encoding = self.config.setdefault('path_encoding', 'gbk')
        else:
            self.path_encoding = self.config.setdefault('path_encoding', sys.getfilesystemencoding())

        proxy_cfg = self.config.setdefault('proxy', {})

        self.requests = requests.Session()
        if http_proxy := proxy_cfg.get('http'):
            self.requests.proxies['http'] = http_proxy
            self.logger.debug(f'set http proxy: {http_proxy}')
        if https_proxy := proxy_cfg.get('https'):
            self.requests.proxies['https'] = https_proxy
            self.logger.debug(f'set https proxy: {https_proxy}')

        web_server_cfg = self.config.setdefault('web_server', {})
        self.http_host = web_server_cfg.setdefault('host', '127.0.0.1')
        self.http_port = web_server_cfg.setdefault('port', 8001)
        self.enable_cors = web_server_cfg.setdefault('enable_cors', False) and use_aiohttp_cors

        self.logger.debug(f'set path_encoding:%s', self.path_encoding)

        threading.Thread(target=update.check, args=(
            self.requests,
            self.config.setdefault('update_source', ('fastgit' if default_cn else 'github')),
        )).start()

        self.mem = mem.XivMem(self, pid)
        self.sq_pack = SqPack(pathlib.Path(self.mem.base_module.filename.decode(self.path_encoding)).parent)

        self.gui = gui.Drawing(self)
        self.gui.always_draw = self.config.setdefault('gui', {}).setdefault('always_draw', False)
        self.gui.draw_update_call.add(self.update)
        self.gui_thread = None

        self.sniffer = sniffer.Sniffer(self)

        self.parser = func_parser.FuncParser(self)

        self.omens = {}
        self.preset_omen_colors = omen.preset_colors.copy()
        for k, v in self.config.setdefault('omen', {}).setdefault('preset_colors', {}).items():
            surface_color = glm.vec4(*v['surface']) if (_surface_color := v.get('surface')) else None
            line_color = glm.vec4(*v['line']) if (_line_color := v.get('line')) else None
            self.logger.debug(f'load color {k}: surface={surface_color} line={line_color}')
            self.preset_omen_colors[k] = surface_color, line_color

        self.plugins = {}
        self.enable_plugins = self.config.setdefault('enable_plugins', {})
        self.plugin_path = [os.path.join(os.environ['ExcPath'], 'plugins'), *(p for p in self.config.setdefault('plugin_paths', []))]
        self.load_init_plugins()
        self.save_config()

    def save_config(self):
        self.cfg_path.parent.mkdir(exist_ok=True, parents=True)
        self.cfg_path.write_text(json.dumps(self.config, ensure_ascii=False, indent=4), encoding='utf-8')

    def reload_plugin_lists(self):
        for p in self.plugin_path:
            if p not in sys.path:
                sys.path.insert(0, p)
        for i, mod in enumerate(pkgutil.iter_modules(self.plugin_path)):
            importlib.import_module(mod.name)
        return plugins.plugins

    def reload_plugin(self, name):
        if plugin := self.plugins.pop(name, None): plugin.unload()
        self.reload_plugin_lists()[name](self)

    def load_init_plugins(self):
        self.reload_plugin_lists()
        for k, p in plugins.plugins.items():
            if self.enable_plugins.setdefault(k, False):
                self.logger.debug(f'load plugin {k}')
                p(self)
            else:
                self.logger.debug(f'disable plugin {k}')
        for k in list(self.enable_plugins.keys()):
            if k not in plugins.plugins:
                self.enable_plugins.pop(k, None)

    def start_gui_thread(self):
        assert not self.gui_thread
        self.gui_thread = threading.Thread(target=self.gui.start, daemon=True)
        self.gui_thread.start()

    def start_sniffer(self):
        self.sniffer.start()

    def update(self, _=None):
        for omen in list(self.omens.values()):
            try:
                omen.draw()
            except Exception as e:
                self.logger.error(f"error when drawing omen:", exc_info=e)
                omen.destroy()

    async def rpc_handler(self, request):
        line = await request.text()
        try:
            return aiohttp.web.json_response({'success': True, 'res': self.parser.parse_func(json.loads(line))})
        except Exception as e:
            self.logger.warning('exception in processing rpc request line:' + line, exc_info=e)
            return aiohttp.web.json_response({'success': False, 'msg': 'server exception'})

    async def rpc_handler_required_password(self, request):
        return aiohttp.web.json_response({'success': False, 'msg': 'required password'})

    def start_http_server(self, host=None, port=None):
        app = aiohttp.web.Application()
        if self.rpc_password:
            app.router.add_post('/rpc/' + self.rpc_password, self.rpc_handler)
            app.router.add_post('/rpc', self.rpc_handler_required_password)
        else:
            app.router.add_post('/rpc', self.rpc_handler)
        if self.enable_cors:
            cors = aiohttp_cors.setup(app, defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                )
            })
            for route in list(app.router.routes()):
                cors.add(route)
        aiohttp.web.run_app(app, host=host or self.http_host, port=port or self.http_port)
