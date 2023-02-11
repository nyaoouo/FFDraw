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


def load_plugins():
    plugin_path = os.path.join(os.environ['ExcPath'], 'plugins')
    sys.path.append(plugin_path)
    for i, mod in enumerate(pkgutil.iter_modules([plugin_path])):
        importlib.import_module(mod.name)


from . import gui, omen, mem, func_parser, plugins


class FFDraw:
    omens: dict[int, omen.BaseOmen]
    logger = logging.getLogger('FFDraw')

    def __init__(self, pid: int):
        self.mem = mem.XivMem(pid)
        self.sq_pack = SqPack(pathlib.Path(self.mem.base_module.filename.decode(os.environ['PathEncoding'])).parent)
        self.gui = gui.Drawing(self)
        self.parser = func_parser.FuncParser(self)
        self.omens = {}
        self.gui.always_draw = True
        self.gui.interfaces.add(self.update)
        self.gui_thread = None
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
            return aiohttp.web.json_response({'success': False})

    def start_http_server(self, host='0.0.0.0', port=8001):
        app = aiohttp.web.Application()
        app.add_routes([aiohttp.web.post('/rpc', self.rpc_handler)])
        aiohttp.web.run_app(app, host=host, port=port)


load_plugins()
