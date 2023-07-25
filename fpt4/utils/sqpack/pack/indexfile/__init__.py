import zlib
from pathlib import Path
from typing import TYPE_CHECKING, IO, Dict, Tuple, Type
from .structure import VersionInfo, IndexFileInfo, DirectoryIndexInfo
from .structure import SynonymTableElem_Hash32, SynonymTableElem_Hash64
from .structure import HashTableElem_Hash32, HashTableElem_Hash64

if TYPE_CHECKING:
    from . import Pack


def compute_hash_32(s: str | bytes):
    if isinstance(s, str): s = s.encode('utf-8')
    return ~zlib.crc32(s.lower()) & 0xFFFFFFFF


class FileInfo:
    def __init__(self, _dir: 'Directory', info: HashTableElem_Hash64 | HashTableElem_Hash32):
        self.dir = _dir
        self.info = info
        self.offset = self.info.block_offset << 7
        self.key = self.dir.index.get_hash_hoge(info)
        if _dir.index.is_index1:
            self.hash = self.key & 0xFFFFFFFF
        else:
            self.hash = self.key
            self.key &= _dir.hash << 32
        self._name = b'file_hash_%d' % self.hash
        self.full_path = b'%s/file_hash_%d' % (self.dir.path, self.hash)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str | bytes):
        if isinstance(name, str): name = name.encode('utf-8')
        self._name = name
        self.full_path = b'%s/%s' % (self.dir.path, name)

    def __repr__(self):
        return f'FileIndex({self.full_path})'

    def __hash__(self):
        return self.key

    def __eq__(self, other):
        if isinstance(other, FileInfo): return other.key == self.key
        return self.key == other


class Directory:
    files: Dict[int, FileInfo] = {}

    def __init__(self, index: 'Index', info: DirectoryIndexInfo):
        self.index = index
        self.info = info
        self.hash = info.dir_hash
        self._path = b'dir_hash_%d' % self.hash

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path: str | bytes):
        if isinstance(path, str):
            path = path.encode('utf-8')
        if path != self._path:
            self._path = path
            for file in self.files.values():
                file.full_path = b'%s/%s' % (path, file.name)

    def build_files(self, stream: IO, index_data_type: Type[HashTableElem_Hash64 | HashTableElem_Hash32], start_pos=0):
        if not self.info.size: return
        stream.seek(start_pos + self.info.offset)
        el_size = index_data_type._size_
        self.files = {}
        for _ in range(self.info.size // el_size):
            file = FileInfo(self, index_data_type.from_buffer_copy(stream.read(el_size)))
            self.files[file.hash] = file
        return self

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        if isinstance(other, Directory): return other.hash == self.hash
        if isinstance(other, int): return other == self.hash
        return False

    def __repr__(self):
        return f'Directory({self._path.decode()})'

    def get_file(self, name_or_hash: str | int) -> FileInfo | None:
        if isinstance(name_or_hash, int):
            return self.files.get(name_or_hash)
        file_hash = compute_hash_32(name_or_hash)
        file = self.files.get(file_hash)
        if file is None: return
        file.name = name_or_hash
        return file


class Index:
    """
    Class representing the data inside a *.index file.
    """
    synonyms: Dict[int, SynonymTableElem_Hash32 | SynonymTableElem_Hash64] = {}
    dirs: Dict[int, Directory] = {}
    files: Dict[int, FileInfo] = {}

    def __init__(self, pack: 'Pack', path_or_stream: IO | str | Path):
        self.pack = pack
        if isinstance(path_or_stream, (str, Path)):
            with open(path_or_stream, 'rb') as stream:
                self._load(stream)
        else:
            self._load(path_or_stream)

    def _load(self, stream: IO):
        start_pos = stream.tell()
        self.version_info = VersionInfo.from_buffer_copy(stream.read(VersionInfo._size_))
        assert self.version_info.magic_str == b'SqPack', Exception('version_info magic_str not pair')
        assert self.version_info.size == VersionInfo._size_, Exception('version_info size not pair')
        self.index_file_info = IndexFileInfo.from_buffer_copy(stream.read(IndexFileInfo._size_))
        self.is_index1 = self.index_file_info.index_type != 2
        self.get_hash_hoge = get_hash_hoge = (lambda x: x.hash_hoge64) if self.is_index1 else (lambda x: x.hash_hoge32)

        if self.index_file_info.synonym_data_size:
            self.synonyms = {}
            synonym_type = SynonymTableElem_Hash64 if self.is_index1 else SynonymTableElem_Hash32
            stream.seek(start_pos + self.index_file_info.synonym_data_offset)
            el_size = synonym_type._size_
            for _ in range(self.index_file_info.synonym_data_size // el_size):
                synonym = synonym_type.from_buffer_copy(stream.read(el_size))
                self.synonyms[get_hash_hoge(synonym)] = synonym

        if self.index_file_info.dir_index_data_size:
            self.dirs = {}
            el_size = DirectoryIndexInfo._size_
            stream.seek(start_pos + self.index_file_info.dir_index_data_offset)
            for _ in range(self.index_file_info.dir_index_data_size // el_size):
                _dir = Directory(self, DirectoryIndexInfo.from_buffer_copy(stream.read(el_size)))
                self.dirs[_dir.hash] = _dir

        if self.dirs:
            self.files = {}
            index_data_type = HashTableElem_Hash64 if self.is_index1 else HashTableElem_Hash32
            for _dir in self.dirs.values():
                for file in _dir.build_files(stream, index_data_type, start_pos).files.values():
                    self.files[file.key] = file

    def file_exists(self, path: str | bytes) -> bool:
        if isinstance(path, str): path = path.encode('utf-8')
        dir_path, base_name = path.rsplit(b'/', 1)
        return compute_hash_32(dir_path) << 32 + compute_hash_32(base_name) in self.files

    def get_directory(self, name_or_hash: str | bytes | int) -> Directory | None:
        if isinstance(name_or_hash, str):
            name_or_hash = name_or_hash.encode('utf-8')
        if isinstance(name_or_hash, int):
            return self.dirs.get(name_or_hash)
        dir_hash = compute_hash_32(name_or_hash)
        _dir = self.dirs.get(dir_hash)
        if _dir is None: return
        _dir.path = name_or_hash
        return _dir

    def get_file(self, path_or_key: str | bytes | Tuple[int, int]) -> FileInfo | None:
        if isinstance(path_or_key, str):
            path_or_key = path_or_key.encode('utf-8')
        if isinstance(path_or_key, bytes):
            dir_key, base_key = path_or_key.rsplit(b'/', 1)
        else:
            dir_key, base_key = path_or_key
        directory = self.get_directory(dir_key)
        if directory is None: return None
        return directory.get_file(base_key)

    def get_file_fast(self, path_or_key: str | bytes | int) -> FileInfo | None:
        if isinstance(path_or_key, str):
            path = path_or_key.encode('utf-8')
        if isinstance(path_or_key, bytes):
            dir_path, base_name = path_or_key.rsplit(b'/', 1)
            return self.files.get(compute_hash_32(dir_path) << 32 + compute_hash_32(base_name))
        return self.files.get(path_or_key)
