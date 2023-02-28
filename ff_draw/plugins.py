import importlib
import inspect
import json
import logging
import os
import pathlib
import pkgutil
import sys
import threading
import typing

from nylib.utils import Counter, ResEvent

from nylib.utils.threading import terminate_thread

if typing.TYPE_CHECKING:
    from ff_draw.main import FFDraw


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
            json.dump(self.data, f, indent=4, ensure_ascii=False)


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
        self._missions = {}
        self._mission_id_counter = Counter()

    def unload(self):
        self.on_unload()
        self._mission_id_counter = None
        while self._missions:
            try:
                k = next(iter(self._missions.keys()))
            except StopIteration:
                break
            if t := self._missions.pop(k, None):
                terminate_thread(t)
        if self.__is_update_override: self.main.gui.draw_update_call.remove(self.update)
        self.main.plugins.pop(self.plugin_name, None)

    def create_mission(self, func, *args, _log_exception=False, **kwargs):
        mid = self._mission_id_counter.get()
        res = ResEvent()

        def _run_mission():
            try:
                res.set(func(*args, **kwargs))
            except Exception as e:
                if _log_exception:
                    self.logger.error('error in mission', exc_info=e)
                res.set_exception(e)
            finally:
                self._missions.pop(mid, None)

        self._missions[mid] = t = threading.Thread(target=_run_mission, daemon=True)
        t.start()
        return res

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


plugins: dict[str, typing.Type[FFDrawPlugin]] = {}
