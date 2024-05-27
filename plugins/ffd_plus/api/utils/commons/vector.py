import ctypes
import typing

from ff_draw.mem.utils import direct_mem_property

_T = typing.TypeVar("_T")
_T2 = typing.TypeVar("_T2")


class Vector:
    _item_size_: int

    class offsets:
        start = 0x0
        finish = 0x8
        end_of_storage = 0x10

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    start = direct_mem_property(ctypes.c_size_t)
    finish = direct_mem_property(ctypes.c_size_t)
    end_of_storage = direct_mem_property(ctypes.c_size_t)

    def __len__(self):
        return (self.finish - self.start) // self._item_size_

    def __getitem__(self, idx) -> int:
        return (self.finish if idx < 0 else self.start) + idx * self._item_size_

    def __iter__(self) -> typing.Generator[int, None, None]:
        ptr = self.start
        end = self.finish
        while ptr < end:
            yield ptr
            ptr += self._item_size_

    def __class_getitem__(cls, item_size) -> 'type[Vector]':
        assert isinstance(item_size, int) and item_size > 0
        return type(f"Vector<{item_size}>", (Vector,), {"_item_size_": item_size})


class ItemVector(Vector, typing.Generic[_T]):
    _item_type_: typing.Type[_T]

    def __getitem__(self, idx) -> _T:
        return self._item_type_(self.handle, super().__getitem__(idx))

    def __iter__(self) -> typing.Generator[_T, None, None]:
        for ptr in super().__iter__():
            yield self._item_type_(self.handle, ptr)

    def __class_getitem__(cls, item: typing.Tuple[typing.Type[_T2], int]) -> 'type[ItemVector[_T2]]':
        item_type, item_size = item
        assert isinstance(item_size, int) and item_size > 0
        return type(f"ItemVector<{item_type.__name__}>", (ItemVector,), {
            "_item_size_": item_size,
            "_item_type_": item_type
        })
