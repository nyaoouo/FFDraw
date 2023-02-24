from struct import unpack_from
from typing import TYPE_CHECKING, Generic, TypeVar, Callable, Dict, Any
from fpt4.utils.se_string import SeString

_T = TypeVar("_T")

if TYPE_CHECKING:
    from .row import DataRow
    from .exh import Column


class DataReader(Generic[_T]):
    def __init__(self, name, size, func: Callable[[bytearray, int], _T]):
        self.name = name
        self.size = size
        self.func = func

    def __call__(self, buffer: bytearray, offset: int) -> _T:
        return self.func(buffer, offset)


def simple_struct_reader(struct_format: str):
    def func(buffer: bytearray, row: 'DataRow', col: 'Column'):
        return unpack_from(struct_format, buffer, row.row_base.row_offset + col.offset)[0]
    func.__name__ = f"simple_struct_reader[{struct_format}]"
    return func


def bit_field_reader(bit_offset: int):
    def func(buffer: bytearray, row: 'DataRow', col: 'Column'):
        return (buffer[row.row_base.row_offset + col.offset] >> bit_offset) & 1 > 0

    func.__name__ = f"bit_field_reader[{bit_offset}]"
    return func


def string_reader(buffer: bytearray, row: 'DataRow', col: 'Column'):
    end_of_fixed = row.row_base.row_offset + row.row_base.sheet.header.header.binary_data_length
    # print(buffer[row.row_base.row_offset + col.offset:row.row_base.row_offset + col.offset+4].hex(' '))
    start = end_of_fixed + unpack_from(">l", buffer, row.row_base.row_offset + col.offset)[0]
    if start < 0: return None
    # return buffer[BEGIN:buffer.find(b'\0', BEGIN)]
    if (buf := buffer[start:buffer.find(b'\0', start)]).startswith(b'_rsv_'):
        return row.row_base.sheet.mgr.rsv_string.get(s := buf.decode('utf-8', errors='ignore'), s)
    return SeString.from_buffer(buf)


DATA_READERS: 'Dict[int,Callable[[bytearray,DataRow,Column],Any]]' = {
    0x0000: string_reader,
    0x0001: lambda d, r, c: d[r.row_base.row_offset + c.offset] != 0,
    0x0002: simple_struct_reader(">b"),
    0x0003: simple_struct_reader(">B"),
    0x0004: simple_struct_reader(">h"),
    0x0005: simple_struct_reader(">H"),
    0x0006: simple_struct_reader(">l"),
    0x0007: simple_struct_reader(">L"),
    0x0009: simple_struct_reader(">f"),
    0x000B: simple_struct_reader(">q")
}

for i in range(0, 8):
    DATA_READERS[0x19 + i] = bit_field_reader(i)


def read_data(buffer: bytearray, row: 'DataRow', col: 'Column'):
    # print(row.row_offset, col.offset)
    return DATA_READERS[col.type](buffer, row, col)
