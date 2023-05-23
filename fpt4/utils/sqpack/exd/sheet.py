import base64
import struct
import zlib
from threading import Lock
from typing import TYPE_CHECKING, Dict, TypeVar, Generic, Callable
from collections import namedtuple
from .exh import ExhFile
from .row import make_row, DataRow
from .data_row import RowData, RowForeign, IconRow, DynamicForeign, ListData

if TYPE_CHECKING:
    from . import ExdManager, Language

_T = TypeVar('_T', bound=DataRow)
_T2 = TypeVar('_T2', bound=DataRow)

dummy = object()

Header = namedtuple('ExdHeader', [
    # Common::Component::Excel::EXData::EXD
    'magic',
    'version',
    'reserved1',
    'index_session_length',
    'data_session_length',
    'reserved2',
    'reserved3',
    'reserved4',
    'reserved5',
])

SIGN_DATA_TYPE = {
    0x0000: ord(b's'),  # string
    0x0001: ord(b'b'),  # bool
    0x0002: ord(b'n'),  # signed byte
    0x0003: ord(b'n'),  # unsigned byte
    0x0004: ord(b'n'),  # signed short
    0x0005: ord(b'n'),  # unsigned short
    0x0006: ord(b'n'),  # signed long
    0x0007: ord(b'n'),  # unsigned long
    0x0009: ord(b'n'),  # float
    0x000B: ord(b'n'),  # signed longlong
    **{0x19 + i: ord(b'f') for i in range(0, 8)},  # bit_field
}


class BlockSheet(Generic[_T]):
    row_offset_map: Dict[int, int]
    rows: Dict[int, _T]

    def __init__(self, lang_sheet: 'LangSheet', block_range: range):
        self.sheet = lang_sheet.sheet
        self.lang_sheet = lang_sheet
        self.block_range = block_range
        self.subkey_count = lang_sheet.sheet.header.header.subkey_count
        self.columns = lang_sheet.sheet.header.columns

        self.name = f"exd/{lang_sheet.sheet.name}_{block_range.start}{lang_sheet.lang.suffix}.exd"
        self.rows = {}

        self.buffer = lang_sheet.sheet.mgr.get_exd_data(self.name)
        self.header = Header._make(struct.unpack_from(f'>I2H6I', self.buffer, 0))
        assert self.header.magic == 0x45584446, ValueError('exd header magic unpair')  # b'EXDF'
        self.row_offset_map = {}
        offset = 0x20
        while offset - 0x20 < self.header.index_session_length:
            row_id, row_offset = struct.unpack_from('>II', self.buffer, offset)
            self.row_offset_map[row_id] = row_offset
            offset += 8

    def __repr__(self):
        return f'BlockSheet({self.name})'

    def get_row(self, row_id: int) -> _T:
        if row_id not in self.rows:
            self.rows[row_id] = row = make_row(self, (row_id,), self.row_offset_map[row_id])
            return row
        return self.rows[row_id]


class LangSheet(Generic[_T]):
    row_to_block_sheet_map: 'Dict[int,BlockSheet[_T]]'
    range_to_block_sheet_map: 'Dict[range,BlockSheet[_T]]'

    def __init__(self, sheet: 'Sheet', lang: 'Language', lazy=True):
        self.sheet = sheet
        self.lang = lang
        self.row_to_block_sheet_map = {}
        self.range_to_block_sheet_map = {}
        self.is_all_block_initialized = False

        if not lazy:
            self.check_is_all_block_initialized()

    def check_is_all_block_initialized(self):
        if self.is_all_block_initialized: return
        for _range in self.sheet.header.blocks:
            try:
                self.get_block_sheet_by_range(_range)
            except FileNotFoundError:
                pass
        self.is_all_block_initialized = True

    def __repr__(self):
        return f'LangSheet({self.sheet.name}_{self.lang.name})'

    def get_row(self, row_id: int, default=dummy):
        try:
            return self.get_block_sheet_by_row(row_id).get_row(row_id)
        except KeyError:
            if default != dummy: return default
            raise

    def get_block_sheet_by_row(self, row: int):
        if row not in self.row_to_block_sheet_map:
            return self.get_block_sheet_by_range(self.sheet.get_row_range(row))
        return self.row_to_block_sheet_map[row]

    def get_block_sheet_by_range(self, block_range: range):
        if block_range not in self.range_to_block_sheet_map:
            self.range_to_block_sheet_map[block_range] = _block_sheet = BlockSheet(self, block_range)
            for row_id in _block_sheet.row_offset_map.keys(): self.row_to_block_sheet_map[row_id] = _block_sheet
        return self.range_to_block_sheet_map[block_range]

    def iter_rows(self, condition: Callable[[_T], bool] = None):
        self.check_is_all_block_initialized()
        if condition is None:
            for k in self.row_to_block_sheet_map.keys():
                yield self.get_row(k)
        else:
            for k in self.row_to_block_sheet_map.keys():
                row = self.get_row(k)
                if condition(row):
                    yield row


class Sheet(Generic[_T]):
    _sheets: 'Dict[Language,LangSheet[_T]]' = {}

    def __repr__(self):
        return f'Sheet({self.name})'

    def __init__(self, mgr: 'ExdManager', name: str, lazy=True, row_type=DataRow):
        from . import Language
        self.mgr = mgr
        self.name = name
        self.header = ExhFile(mgr.get_exd_data(f'exd/{name}.exh'))
        if row_type is None:
            assert (row_type := DataRow._map.get(self.get_sign())), f"no sign match for sheet {self.name}"
        elif hasattr(row_type, '_sign') and (sheet_sign := self.get_sign()) != getattr(row_type, '_sign', sheet_sign):
            assert (row_type := DataRow._map.get(sheet_sign)), f"no sign match for sheet {self.name}"
        self._sheets = {}
        self.lazy = lazy
        self.lang_sheet_create_lock = Lock()
        self.row_type = row_type

        self._fix_lang = None
        if len(self.header.langs) == 1:
            self._fix_lang = Language(next(iter(self.header.langs)))
        elif len(self.header.langs) == 0:
            self._fix_lang = Language.none

        if not self.lazy:
            for lang in self.header.langs:
                self.get_lang_sheet(Language(lang))

    def get_sign(self):
        return self.name.encode() + b'|' + base64.b64encode(zlib.compress(bytes(
            SIGN_DATA_TYPE[col.type] for col in self.header.columns
        )))

    def get_min_id(self):
        return min(r.start for r in self.header.blocks)

    def get_max_id(self):
        return max(r.start + r.stop for r in self.header.blocks)

    def get_lang(self, user_lang: 'Language' = None):
        if self._fix_lang is not None: return self._fix_lang
        if user_lang is not None: return user_lang
        return self.mgr.default_language

    def get_lang_sheet(self, user_lang: 'Language' = None):
        user_lang = self.get_lang(user_lang)
        if user_lang not in self._sheets:
            with self.lang_sheet_create_lock:
                if user_lang not in self._sheets:
                    self._sheets[user_lang] = LangSheet(self, user_lang, self.lazy)
        return self._sheets[user_lang]

    def get_row_range(self, row: int):
        for block_range in self.header.blocks:
            if row in block_range: return block_range
        raise KeyError(f"{row} is not in range of sheet {self.name}")

    def get_row(self, row_id: int, user_lang: 'Language' = None, default=dummy) -> _T:
        return self.get_lang_sheet(user_lang).get_row(row_id, default)

    def iter_rows(self, condition: Callable[[_T], bool] = None, user_lang: 'Language' = None):
        return self.get_lang_sheet(user_lang).iter_rows(condition)

    def first(self, condition: Callable[[_T], bool], user_lang: 'Language' = None, default: _T2 = None) -> _T | _T2:
        return next(self.get_lang_sheet(user_lang).iter_rows(condition), default)

    def __getitem__(self, item):
        return self.get_row(item)

    def __iter__(self):
        return self.iter_rows()

    def get_row_offset(self, col_name):
        col_type = getattr(self.row_type, col_name, None)
        if isinstance(col_type, (RowData, RowForeign, IconRow, DynamicForeign)):
            cid = col_type.col_id
        else:
            raise TypeError(f'col type {type(col_type)} of col name {col_name} is not support')
        return self.header.columns[cid].offset
