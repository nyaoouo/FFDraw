from os import environ

from pathlib import Path
from .pack import PackManager
from .exd import ExdManager
from .utils import Language

if not (_pure_exd := bool(environ.get('__sqpack_pure_exd__'))):
    from .sheets import Sheets

_cached_sqpack = {}


class SqPack:
    def __init__(self, game_path: str | Path, default_language: Language = Language.en):
        self.game_path = game_path if isinstance(game_path, Path) else Path(game_path)
        self.pack = PackManager(self.game_path / 'sqpack')
        self.exd = ExdManager(self.pack, default_language=default_language)
        if not _pure_exd:
            self.sheets = Sheets(self)

    @classmethod
    def get(cls, game_path: str | Path, default_language: Language = Language.en) -> 'SqPack':
        game_path = (Path(game_path) if isinstance(game_path, str) else game_path).absolute()
        k = game_path, default_language
        if k not in _cached_sqpack:
            _cached_sqpack[k] = SqPack(game_path, default_language)
        return _cached_sqpack[k]
