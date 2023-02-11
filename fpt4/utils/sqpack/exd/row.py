import struct
from typing import TYPE_CHECKING, Generic, TypeVar
from .reader import read_data
from .data_row import RowData, DynamicForeign, RowForeign, ListData

_DataRow = RowData, DynamicForeign, RowForeign, ListData

if TYPE_CHECKING:
    from .sheet import BlockSheet

_T = TypeVar("_T")


class RowBase:
    row: 'DataRow|SubDataRow|None'

    def __init__(self, block_sheet: 'BlockSheet', key, offset: int, row_offset=0):
        self.column = block_sheet.columns
        self.buffer = block_sheet.buffer
        self.cache = {}
        self.key = key
        self.sheet = block_sheet.sheet
        self.lang_sheet = block_sheet.lang_sheet
        self.block_sheet = block_sheet
        self._offset = offset
        self.row_offset = offset + row_offset  # header size
        self.row = None

    def as_dict(self):
        row_class = self.row.__class__
        if issubclass(row_class, SubDataRow):
            return {rb.key[-1]: rb.as_dict() for rb in (r.row_base for r in self.row)}
        k = '__data_row_name'
        if not hasattr(row_class, k):
            setattr(row_class, k, [
                attr_name for attr_name in row_class.__dict__.keys()
                if isinstance(getattr(row_class, attr_name, None), _DataRow)
            ])
        if not (keys := getattr(row_class, k)):
            return list(self.row)
        return {
            key: getattr(self.row, key)
            for key in keys
        }


class DataRow(Generic[_T]):
    _sign: bytes
    _map = {}
    sheet_name: None | str = None
    _display: int | str | None = None

    def __bool__(self):
        return bool(self.row_base.key[0])

    key = property(lambda self: self.row_base.key if len(self.row_base.key) > 1 else self.row_base.key[0])

    def __init__(self, base: RowBase):
        base.row = self
        self.row_base = base

    def __iter__(self):
        for i in range(len(self.row_base.column)): yield self[i]

    def __getitem__(self, key: int) -> _T:
        if key not in self.row_base.cache:
            if len(self.row_base.column) <= key: return None
            self.row_base.cache[key] = read_data(self.row_base.buffer, self, self.row_base.column[key])
        return self.row_base.cache[key]

    def __repr__(self):
        if self._display is not None:
            k = getattr(self, self._display) if isinstance(self._display, str) else self[self._display]
            return f"DataRow({self.row_base.sheet.name}#{self.key}, {k})"
        return f"DataRow({self.row_base.sheet.name}#{self.key})"

    def __int__(self):
        return self.row_base.key[0]

    def __eq__(self, other):
        if isinstance(other, DataRow):
            return other.row_base.sheet.name == self.row_base.sheet.name and other.key == self.key
        else:
            return self.key == other

    def __init_subclass__(cls, **kwargs):
        if hasattr(cls, '_sign'): cls._map[cls._sign] = cls


class SubDataRow(DataRow, Generic[_T]):
    def __init__(self, base: RowBase):
        super().__init__(base)
        o = base.row_offset
        self.size, self.count = struct.unpack_from('>lh', base.block_sheet.buffer, base._offset)
        sub_is_data_row = base.sheet.header.header.subkey_count - 1 == len(base.key)
        if sub_is_data_row:
            for _ in range(self.count):
                _key, = struct.unpack_from(">h", base.buffer, o)
                base.cache[_key] = base.block_sheet.sheet.row_type(RowBase(base.block_sheet, base.key + (_key,), o + 2, 0))
                o += base.sheet.header.header.binary_data_length + 2
        else:
            for _ in range(self.count):
                _key, = struct.unpack_from(">h", base.buffer, o)
                _row = base.cache[_key] = SubDataRow(RowBase(base.block_sheet, base.key + (_key,), o + 2, 6))
                o += _row.size

    def __iter__(self):
        row: _T
        for row in self.row_base.cache.values():
            yield row

    def __getitem__(self, key: int):
        return self.row_base.cache[key]

    def __repr__(self):
        return f"SubDataRow({self.row_base.sheet.name},{self.key},{self.count})"


def make_row(block_sheet: 'BlockSheet', key, offset: int) -> SubDataRow | DataRow:
    if isinstance(key, int): key = key,
    if block_sheet.sheet.header.header.subkey_count > len(key):
        return SubDataRow(RowBase(block_sheet, key, offset, 6))
    else:
        return block_sheet.sheet.row_type(RowBase(block_sheet, key, offset, 6))
