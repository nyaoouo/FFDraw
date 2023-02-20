import json
import logging
import pathlib
import typing

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
        self._json_file.parent.mkdir(parents=True,exist_ok=True)
        with self._json_file.open('w', encoding='utf-8') as f:
            json.dump(self.data, f)


class FFDrawPlugin:
    main: 'FFDraw'

    def __init__(self, main):
        self.main = main
        self.logger = logging.getLogger(self.__class__.__name__)
        self.storage = PluginStorage(self.main.app_data_path / 'plugins' / self.__class__.__name__)

    @property
    def data(self):
        return self.storage.data

    @data.setter
    def data(self, v):
        self.storage.data = v

    def __init_subclass__(cls, **kwargs):
        super(FFDrawPlugin, cls).__init_subclass__()
        plugins.append(cls)

    def update(self, main: 'FFDraw'):
        pass

    def process_command(self, data: dict) -> bool:
        return False


plugins: list[typing.Type[FFDrawPlugin]] = []
