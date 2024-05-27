import typing

from fpt4.utils.se_string import SeString
from nylib.utils.win32 import memory as ny_mem


class CharArr:
    _size_: int

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    def __class_getitem__(cls, item) -> 'typing.Type[CharArr]':
        return type(f"CharArr[{item}]", (CharArr,), {
            "_size_": item
        })

    @property
    def se_string(self):
        return SeString.from_buffer(self.value)

    @property
    def value(self):
        return ny_mem.read_bytes_zero_trim(self.handle, self.address, self._size_)

    @value.setter
    def value(self, value):
        ny_mem.write_bytes(self.handle, self.address, value)

    @typing.overload
    def __getitem__(self, item: int) -> int:
        ...

    @typing.overload
    def __getitem__(self, item: slice) -> bytearray:
        ...

    def __getitem__(self, item):
        if isinstance(item, int):
            return ny_mem.read_uint8(self.handle, self.address + item)
        elif isinstance(item, slice):
            start = item.start or 0
            stop = item.stop or self._size_
            return ny_mem.read_bytes(self.handle, self.address + start, stop - start)
        else:
            raise TypeError(f"Unsupported type {type(item)}")

    def __setitem__(self, key, value):
        if isinstance(key, int):
            ny_mem.write_uint8(self.handle, self.address + key, value)
        elif isinstance(key, slice):
            start = key.start or 0
            if key.stop is not None:
                assert len(value) <= key.stop - start, "Value too long"
            ny_mem.write_bytes(self.handle, self.address + start, value)
        else:
            raise TypeError(f"Unsupported type {type(key)}")

    def __len__(self):
        return self._size_

    def __iter__(self):
        i = 0
        if hasattr(self, "_size_"):
            while i < self._size_:
                yield ny_mem.read_uint8(self.handle, self.address + i)
                i += 1
        else:
            while True:
                yield ny_mem.read_uint8(self.handle, self.address + i)
                i += 1


class CharPtr:

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    @property
    def address_value(self):
        return ny_mem.read_address(self.handle, self.address)

    @address_value.setter
    def address_value(self, value):
        ny_mem.write_address(self.handle, self.address, value)

    @property
    def se_string(self):
        return SeString.from_buffer(v) if (v := self.value) is not None else None

    @property
    def value(self):
        if (addr := self.address_value) == 0: return None
        return ny_mem.read_bytes_zero_trim(self.handle, addr)

    @value.setter
    def value(self, value):
        if value is None:
            value = 0
        if isinstance(value, int):
            self.address_value = value
        raise TypeError(f"Unsupported set type {type(value)}")

    def __bool__(self):
        return self.address_value != 0

    @typing.overload
    def __getitem__(self, item: int) -> int:
        ...

    @typing.overload
    def __getitem__(self, item: slice) -> bytearray:
        ...

    def __getitem__(self, item):
        addr_value = self.address_value
        if addr_value == 0: raise ValueError("Null pointer")
        if isinstance(item, int):
            return ny_mem.read_uint8(self.handle, addr_value + item)
        elif isinstance(item, slice):
            start = item.start or 0
            assert item.stop is not None and item.stop >= start, "Invalid slice"
            return ny_mem.read_bytes(self.handle, addr_value + start, item.stop - start)
        else:
            raise TypeError(f"Unsupported type {type(item)}")

    def __setitem__(self, key, value):
        addr_value = self.address_value
        if addr_value == 0: raise ValueError("Null pointer")
        if isinstance(key, int):
            ny_mem.write_uint8(self.handle, addr_value + key, value)
        elif isinstance(key, slice):
            start = key.start or 0
            if key.stop is not None:
                assert len(value) <= key.stop - start, "Value too long"
            ny_mem.write_bytes(self.handle, addr_value + start, value)
        else:
            raise TypeError(f"Unsupported type {type(key)}")

    def __iter__(self):
        addr_value = self.address_value
        if addr_value == 0:
            return
        while True:
            yield ny_mem.read_uint8(self.handle, addr_value)
            addr_value += 1
