import ctypes
import typing

from nylib.utils.win32 import memory as ny_mem

_T = typing.TypeVar("_T")
_T2 = typing.TypeVar("_T2")


class _SimpleArr(typing.Generic[_T]):
    _item_count_: int
    _item_size_: int
    _reader_: typing.Callable[[typing.Any, int], _T]
    _writer_: typing.Callable[[typing.Any, int, _T], None]

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    def __len__(self):
        return self._item_count_

    @typing.overload
    def __getitem__(self, idx: int) -> _T:
        ...

    @typing.overload
    def __getitem__(self, idx: slice) -> typing.Generator[_T, None, None]:
        ...

    def _simp_slice_(self, key):
        start = key.start or 0
        if start < 0: start += self._item_count_
        stop = key.stop or self._item_count_
        if stop < 0: stop += self._item_count_
        return start, stop

    def __getitem__(self, idx):
        assert (address := self.address), "Null pointer"
        if isinstance(idx, int):
            return self._reader_(self.handle, address + idx * self._item_size_)
        elif isinstance(idx, slice):
            start, stop = self._simp_slice_(idx)
            return tuple(self._reader_(self.handle, address + i * self._item_size_) for i in range(start, stop))
        else:
            raise TypeError(f"Invalid index type: {type(idx)}")

    def __setitem__(self, key, value):
        assert (address := self.address), "Null pointer"
        if isinstance(key, int):
            self._writer_(self.handle, address + key * self._item_size_, value)
        elif isinstance(key, slice):
            start, stop = self._simp_slice_(key)
            for i, item in zip(range(start, stop), value):
                self._writer_(self.handle, address + i * self._item_size_, item)

    def __iter__(self) -> typing.Generator[_T, None, None]:
        assert (address := self.address), "Null pointer"
        if hasattr(self, '_item_count_'):
            for i in range(self._item_count_):
                yield self._reader_(self.handle, address + i * self._item_size_)
        else:
            while True:
                yield self._reader_(self.handle, address)
                address += self._item_size_

    def __class_getitem__(cls: typing.Type[_T2], item_count: int) -> typing.Type[_T2]:
        assert (dims := getattr(cls, "_arr_dims_", 0)) < 1, "SimpleArr cannot be nested"
        return type(f'{cls.__name__}[{item_count}]', (cls,), {
            '_item_count_': item_count,
            '_arr_dims_': dims + 1
        })


def _simple_arr_factory(t_name, reader, writer, item_size, hint_type: typing.Type[_T]) -> 'type[_SimpleArr[_T]]':
    return type(f'Arr<{t_name}>', (_SimpleArr,), {'_item_size_': item_size, '_reader_': staticmethod(reader), '_writer_': staticmethod(writer)})


class _SimplePtr(_SimpleArr[_T]):
    def __init__(self, handle, address):
        self.handle = handle
        self.p_address = address

    @property
    def address(self):
        assert (p_address := self.p_address), "Null pointer"
        return ny_mem.read_address(self.handle, p_address)

    @address.setter
    def address(self, value):
        assert (p_address := self.p_address), "Null pointer"
        ny_mem.write_address(self.handle, p_address, value)

    @property
    def content(self) -> _T:
        return self[0]

    @content.setter
    def content(self, value):
        self[0] = value


def _simple_ptr_factory(t_name, reader, writer, item_size, hint_type: typing.Type[_T]) -> 'type[_SimplePtr[_T]]':
    return type(f'Ptr<{t_name}>', (_SimplePtr,), {'_item_size_': item_size, '_reader_': staticmethod(reader), '_writer_': staticmethod(writer)})


int8_arr = _simple_arr_factory('int8', ny_mem.read_int8, ny_mem.write_int8, 1, int)
int16_arr = _simple_arr_factory('int16', ny_mem.read_int16, ny_mem.write_int16, 2, int)
int32_arr = _simple_arr_factory('int32', ny_mem.read_int32, ny_mem.write_int32, 4, int)
int64_arr = _simple_arr_factory('int64', ny_mem.read_int64, ny_mem.write_int64, 8, int)
uint8_arr = _simple_arr_factory('uint8', ny_mem.read_uint8, ny_mem.write_uint8, 1, int)
uint16_arr = _simple_arr_factory('uint16', ny_mem.read_uint16, ny_mem.write_uint16, 2, int)
uint32_arr = _simple_arr_factory('uint32', ny_mem.read_uint32, ny_mem.write_uint32, 4, int)
uint64_arr = _simple_arr_factory('uint64', ny_mem.read_uint64, ny_mem.write_uint64, 8, int)
float_arr = _simple_arr_factory('float', ny_mem.read_float, ny_mem.write_float, 4, float)
ptr_arr = _simple_arr_factory('ptr', ny_mem.read_address, ny_mem.write_address, ctypes.sizeof(ctypes.c_void_p), int)

int8_ptr = _simple_ptr_factory('int8', ny_mem.read_int8, ny_mem.write_int8, 1, int)
int16_ptr = _simple_ptr_factory('int16', ny_mem.read_int16, ny_mem.write_int16, 2, int)
int32_ptr = _simple_ptr_factory('int32', ny_mem.read_int32, ny_mem.write_int32, 4, int)
int64_ptr = _simple_ptr_factory('int64', ny_mem.read_int64, ny_mem.write_int64, 8, int)
uint8_ptr = _simple_ptr_factory('uint8', ny_mem.read_uint8, ny_mem.write_uint8, 1, int)
uint16_ptr = _simple_ptr_factory('uint16', ny_mem.read_uint16, ny_mem.write_uint16, 2, int)
uint32_ptr = _simple_ptr_factory('uint32', ny_mem.read_uint32, ny_mem.write_uint32, 4, int)
uint64_ptr = _simple_ptr_factory('uint64', ny_mem.read_uint64, ny_mem.write_uint64, 8, int)
float_ptr = _simple_ptr_factory('float', ny_mem.read_float, ny_mem.write_float, 4, float)
ptr_ptr = _simple_ptr_factory('ptr', ny_mem.read_address, ny_mem.write_address, ctypes.sizeof(ctypes.c_void_p), int)
