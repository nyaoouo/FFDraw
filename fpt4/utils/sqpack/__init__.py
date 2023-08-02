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
        _cached_sqpack[game_path, default_language] = self
        self.game_path = game_path if isinstance(game_path, Path) else Path(game_path)
        self.pack = PackManager(self.game_path / 'sqpack')
        self.exd = ExdManager(self.pack, default_language=default_language)
        if not _pure_exd:
            self.sheets = Sheets(self)

    @classmethod
    def get(cls, game_path: str | Path = None, default_language: Language = Language.en) -> 'SqPack':
        if game_path is None: return next(iter(_cached_sqpack.values()))
        game_path = (Path(game_path) if isinstance(game_path, str) else game_path).absolute()
        return _cached_sqpack.get((game_path, default_language)) or SqPack(game_path, default_language)
