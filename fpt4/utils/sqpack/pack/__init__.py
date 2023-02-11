import io
import threading
from pathlib import Path
from logging import getLogger
from threading import Lock, get_ident
from typing import Dict, Tuple, IO
from .indexfile import Index, FileInfo
from .file import file_from_stream, TextureFile

PACK_TYPE_TO_KEY_MAP = {
    b"common": 0x00,
    b"bgcommon": 0x01,
    b"bg": 0x02,
    b"cut": 0x03,
    b"chara": 0x04,
    b"shader": 0x05,
    b"ui": 0x06,
    b"sound": 0x07,
    b"vfx": 0x08,
    b"exd": 0x0a,
    b"game_script": 0x0b,
    b"music": 0x0c,
    b"_sqpack_test": 0x12,
    b"_debug": 0x13,
}
PACK_KEY_TO_TYPE_MAP = {v: k for k, v in PACK_TYPE_TO_KEY_MAP.items()}


class PackIdentifier:
    type_str = property(lambda self: PACK_KEY_TO_TYPE_MAP.get(self.type_key, f'unknown_pack_type_{self.type_key:x}'))
    expansion_str = property(lambda self: f'ex{self.expansion_key}' if self.expansion_key else 'ffxiv')

    def __init__(self, type_key: int, expansion_key: int, number: int):
        self.type_key = type_key
        self.expansion_key = expansion_key
        self.number = number
        self._hash = self.type_key << 16 | self.expansion_key << 8 | self.number

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return isinstance(other, PackIdentifier) and other._hash == self._hash

    def __repr__(self):
        return f"PackId({self.type_str}/{self.expansion_str}/{self.number})"

    @classmethod
    def from_path(cls, full_path: str | bytes):
        if isinstance(full_path, str):
            full_path = full_path.encode('utf-8')
        type_sep = full_path.find(b'/')
        assert type_sep > 0, ValueError(f'type sep is not found in {full_path}')
        type_key = PACK_TYPE_TO_KEY_MAP.get(full_path[:type_sep], None)
        assert type_key is not None, ValueError(f'type key is undefined for {full_path}')
        exp_sep = full_path.find(b'/', type_sep + 1)
        expansion = 0  # DEFAULT_EXPANSION
        number = 0
        if exp_sep > type_sep:
            _expansion = full_path[exp_sep - 1] - 48
            if _expansion < 9: expansion = _expansion
            number_end = full_path.find(b'_', exp_sep)
            if number_end - exp_sep == 3:
                try:
                    number = int(full_path[exp_sep + 1:number_end], 16)
                except RuntimeError:
                    number = 0
        return cls(type_key, expansion, number)

    def index_file_path(self, data_directory: Path):
        return data_directory.joinpath(
            self.expansion_str,
            f"{self.type_key:02x}{self.expansion_key:02x}{self.number:02x}.win32.index"
        )

    def index2_file_path(self, data_directory: Path):
        return data_directory.joinpath(
            self.expansion_str,
            f"{self.type_key:02x}{self.expansion_key:02x}{self.number:02x}.win32.index2"
        )

    def dat_file_path(self, data_directory: Path, dat_file: int = 0):
        return data_directory.joinpath(
            self.expansion_str,
            f"{self.type_key:02x}{self.expansion_key:02x}{self.number:02x}.win32.dat{dat_file}"
        )


class PackManager(object):
    packs: 'Dict[PackIdentifier,Pack]'
    logger = getLogger(f'SqPack/PackCollection')

    def __init__(self, data_directory: str | bytes | Path):
        if isinstance(data_directory, str):
            data_directory = Path(data_directory)
        if isinstance(data_directory, Path):
            if not (data_directory.exists() and data_directory.is_dir()):
                raise FileNotFoundError
        else:
            raise TypeError("data_directory")
        self.data_directory = data_directory
        self.packs = {}

    def get_pack(self, id_or_path: str | bytes | PackIdentifier) -> 'Pack|None':
        if isinstance(id_or_path, str):
            id_or_path = id_or_path.encode('utf-8')
        if isinstance(id_or_path, bytes):
            id_or_path = PackIdentifier.from_path(id_or_path)
        if id_or_path not in self.packs:
            self.packs[id_or_path] = Pack(self.data_directory, id_or_path, self)
        return self.packs[id_or_path]

    def get_texture_file(self, path_or_key: str| bytes | int) -> TextureFile:
        assert isinstance(_file := self.get_file(path_or_key), TextureFile), f"{path_or_key} is not TextureFile but {type(_file)}"
        return _file

    def get_file(self, path_or_key: str | bytes | Tuple[int, int]):
        return self.get_pack(path_or_key).get_file(path_or_key)


class Pack:
    """
    Class for a SqPack.
    """
    logger = getLogger(f'SqPack/Pack')

    @property
    def keep_in_memory(self):
        return self._keep_in_memory

    @keep_in_memory.setter
    def keep_in_memory(self, value):
        if value == self.keep_in_memory: return
        self._keep_in_memory = value
        if not value: self._buffers.clear()

    def __init__(self, data_directory: str | bytes | Path, _id: PackIdentifier, mgr: PackManager = None):
        if not isinstance(data_directory, Path):
            data_directory = Path(data_directory)
        if not (data_directory.exists() and data_directory.is_dir()):
            raise FileNotFoundError(data_directory)

        self.mgr = mgr
        self.data_directory = data_directory
        self.id = _id
        self._data_streams = threading.local()
        self._data_streams_lock = Lock()
        self._keep_in_memory = False
        self._buffers: Dict[int, bytes] = {}
        index_path = self.id.index_file_path(self.data_directory)
        self.index = Index(self, index_path) if index_path.exists() and index_path.is_file() else None
        index_path2 = self.id.index2_file_path(self.data_directory)
        self.index2 = Index(self, index_path2) if index_path2.exists() and index_path2.is_file() else None

    def get_data_stream(self, dat_file=0) -> IO:
        key = str(dat_file)
        if not hasattr(self._data_streams, key):
            full_path = self.id.dat_file_path(self.data_directory, dat_file)
            if self.keep_in_memory:
                if dat_file not in self._buffers:
                    self.logger.debug('loading Mode: Read Id: %s Tid: %s FullPath: %s', self.id, get_ident(), full_path)
                    self._buffers[dat_file] = full_path.read_bytes()
                setattr(self._data_streams, key, io.BytesIO(self._buffers[dat_file]))
            else:
                self.logger.debug('loading Mode: Open Id: %s Tid: %s FullPath: %s', self.id, get_ident(), full_path)
                setattr(self._data_streams, key, full_path.open(mode='rb'))
        return getattr(self._data_streams, key)

    def __repr__(self):
        _id = self.id
        return f"Pack({_id.type_str}, {_id.expansion_str}, {_id.number})"

    def get_file(self, path_or_key: str | bytes | int):
        file_index = None
        if self.index: file_index = self.index.get_file(path_or_key)
        if file_index is None and self.index2: file_index = self.index2.get_file(path_or_key)
        if file_index is None: raise FileNotFoundError(f'{path_or_key} is not found')
        return self.get_file_by_info(file_index)

    def get_file_by_info(self, file_info: FileInfo):
        stream = self.get_data_stream(file_info.info.data_file_id)
        stream.seek(file_info.offset)
        return file_from_stream(file_info, stream)
