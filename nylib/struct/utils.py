import ctypes
import typing

_T = typing.TypeVar('_T')

if typing.TYPE_CHECKING:
    class CArray(ctypes.Array, typing.Generic[_T]):
        def __getitem__(self, item) -> _T: ...

        def __iter__(self) -> typing.Iterable[_T]: ...


class fctypes:
    c_char: typing.Type[bytes] = bytes
    c_int: typing.Type[int] = int
    c_uint: typing.Type[int] = int
    c_int8: typing.Type[int] = int
    c_int16: typing.Type[int] = int
    c_int32: typing.Type[int] = int
    c_int64: typing.Type[int] = int
    c_uint8: typing.Type[int] = int
    c_uint16: typing.Type[int] = int
    c_uint32: typing.Type[int] = int
    c_uint64: typing.Type[int] = int
    c_byte: typing.Type[int] = int
    c_ubyte: typing.Type[int] = int
    c_short: typing.Type[int] = int
    c_ushort: typing.Type[int] = int
    c_long: typing.Type[int] = int
    c_ulong: typing.Type[int] = int
    c_longlong: typing.Type[int] = int
    c_ulonglong: typing.Type[int] = int
    c_float: typing.Type[float] = float
    c_double: typing.Type[float] = float
    c_void_p = ctypes.c_void_p

    @staticmethod
    def array(t: typing.Type[_T], size) -> 'typing.Type[CArray[_T]]':
        return t * size


def next_bit(byte_offset, bit_offset=0):
    bit_offset += 1
    return byte_offset + bit_offset // 8, bit_offset % 8


for k in fctypes.__annotations__.keys():
    setattr(fctypes, k, getattr(ctypes, k))
