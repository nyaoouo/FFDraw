import importlib
import inspect
import json
import logging
import os
import pathlib
import pkgutil
import sys
import typing

if typing.TYPE_CHECKING:
    from ff_draw.main import FFDraw

plugin_path = os.path.join(os.environ['ExcPath'], 'plugins')
sys.path.append(plugin_path)


class PluginStorage:
    def __init__(self, path: pathlib.Path):
        self.path = path
        self._json_file = self.path / 'data.json'
        self.data = self.load()

    def load(self):
        if self._json_file.exists():
            with self._json_file.open(encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {}
        self.data = data
        return data

    def save(self):
        self._json_file.parent.mkdir(parents=True, exist_ok=True)
        with self._json_file.open('w', encoding='utf-8') as f:
            json.dump(self.data, f)


class FFDrawPlugin:
    main: 'FFDraw'
    plugin_name = ''

    def __init__(self, main):
        self.main = main
        self.logger = logging.getLogger(self.__class__.__name__)
        self.storage = PluginStorage(self.main.app_data_path / 'plugins' / self.__class__.__name__)
        self.__is_update_override = self.__class__.update != FFDrawPlugin.update
        if self.__is_update_override: main.gui.draw_update_call.add(self.update)
        if old_plugin := self.main.plugins.pop(self.plugin_name, None):
            old_plugin.unload()
        self.main.plugins[self.plugin_name] = self

    def unload(self):
        self.on_unload()
        if self.__is_update_override: self.main.gui.draw_update_call.remove(self.update)
        self.main.plugins.pop(self.plugin_name, None)

    def on_unload(self):
        pass

    @property
    def data(self):
        return self.storage.data

    @data.setter
    def data(self, v):
        self.storage.data = v

    def __init_subclass__(cls, **kwargs):
        super(FFDrawPlugin, cls).__init_subclass__()
        pkg_name = inspect.stack()[1].frame.f_globals['__name__'].split('.', 1)[0]
        cls.plugin_name = pkg_name + '/' + cls.__name__
        plugins[cls.plugin_name] = cls

    def update(self, main: 'FFDraw'):
        pass

    def draw_panel(self):
        pass

    def process_command(self, data: dict) -> bool:
        return False


def reload_plugin_lists():
    plugins.clear()
    for i, mod in enumerate(pkgutil.iter_modules([plugin_path])):
        for m in list(sys.modules.keys()):
            if m.startswith(mod.name):
                del sys.modules[m]
        importlib.import_module(mod.name)
    return plugins


plugins: dict[str, typing.Type[FFDrawPlugin]] = {}
