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
from fpt4.utils.sqpack import SqPack

try:
    import aiohttp_cors
except ImportError:
    use_aiohttp_cors = False
else:
    use_aiohttp_cors = True

from . import gui, omen, mem, func_parser, plugins, update

cfg_path = pathlib.Path(os.environ['ExcPath']) / 'config.json'
default_cn = bool(os.environ.get('DefaultCn'))


class FFDraw:
    omens: dict[int, omen.BaseOmen]
    logger = logging.getLogger('FFDraw')

    def __init__(self, pid: int):
        self.config = json.loads(cfg_path.read_text('utf-8')) if cfg_path.exists() else {}
        self.rpc_password = self.config.setdefault('rpc_password', '')
        if default_cn:
            self.path_encoding = self.config.setdefault('path_encoding', 'gbk')
        else:
            self.path_encoding = self.config.setdefault('path_encoding', sys.getfilesystemencoding())
        web_server_cfg = self.config.setdefault('web_server', {})
        self.http_host = web_server_cfg.setdefault('host', '127.0.0.1')
        self.http_port = web_server_cfg.setdefault('port', 8001)
        self.enable_cors = web_server_cfg.setdefault('enable_cors', False) and use_aiohttp_cors

        self.logger.debug(f'set path_encoding:%s', self.path_encoding)

        threading.Thread(target=update.check, args=(
            self.config.setdefault('update_source', ('fastgit' if default_cn else 'github')),
        )).start()

        self.mem = mem.XivMem(self, pid)
        self.sq_pack = SqPack(pathlib.Path(self.mem.base_module.filename.decode(self.path_encoding)).parent)

        self.gui = gui.Drawing(self)
        self.gui.always_draw = self.config.setdefault('gui', {}).setdefault('always_draw', False)
        self.gui.interfaces.add(self.update)
        self.gui_thread = None

        self.parser = func_parser.FuncParser(self)

        self.omens = {}
        self.preset_omen_colors = omen.preset_colors.copy()
        for k, v in self.config.setdefault('omen', {}).setdefault('preset_colors', {}).items():
            surface_color = glm.vec4(*v['surface']) if 'surface' in v else None
            line_color = glm.vec4(*v['line']) if 'surface' in v else None
            self.logger.debug(f'load color {k}: surface={surface_color} line={line_color}')
            self.preset_omen_colors[k] = surface_color, line_color

        self.plugins = []
        self.load_plugins()
        self.save_config()

    def save_config(self):
        cfg_path.write_text(json.dumps(self.config, ensure_ascii=False, indent=4), encoding='utf-8')

    def load_plugins(self):
        plugin_path = os.path.join(os.environ['ExcPath'], 'plugins')
        sys.path.append(plugin_path)
        enable_plugins = self.config.setdefault('enable_plugins', [])
        disable_plugins = self.config.setdefault('disable_plugins', [])
        for i, mod in enumerate(pkgutil.iter_modules([plugin_path])):
            if mod.name in enable_plugins:
                self.logger.debug(f'load plugin {mod.name}')
                importlib.import_module(mod.name)
            else:
                self.logger.debug(f'disable plugin {mod.name}')
                if mod.name not in disable_plugins:
                    disable_plugins.append(mod.name)
        self.plugins = [p(self) for p in plugins.plugins if p != plugins.FFDrawPlugin]
        for plugin in self.plugins:
            if plugin.__class__.update != plugins.FFDrawPlugin.update:
                self.gui.interfaces.add(plugin.update)

    def start_gui_thread(self):
        assert not self.gui_thread
        self.gui_thread = threading.Thread(target=self.gui.start, daemon=True)
        self.gui_thread.start()

    def update(self, _=None):
        for omen in list(self.omens.values()):
            try:
                omen.draw()
            except Exception as e:
                self.logger.error(f"error when drawing omen:", exc_info=e)
                omen.destroy()
        # try:
        #     self.draw_me()
        # except Exception as e:
        #     self.logger.error(f"error when drawing point:", exc_info=e)

    def draw_me(self):
        if me := self.mem.actor_table.me:
            self.gui.add_3d_shape(
                0x50000 | 90,
                glm.translate(me.pos) *
                glm.rotate(me.facing, glm.vec3(0, 1, 0)) *
                glm.scale(glm.vec3(5, 5, 5)),
                glm.vec4(.5, .5, 1, .3),
                glm.vec4(.5, .5, 1, .7),
            )

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
