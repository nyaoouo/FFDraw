import typing

_T = typing.TypeVar("_T")
_T2 = typing.TypeVar("_T2")


class Arr:
    _item_size_: int
    _item_count_: int

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    def __len__(self):
        return self._item_count_

    def __getitem__(self, idx) -> int:
        return self.address + idx * self._item_size_

    def __iter__(self) -> typing.Generator[int, None, None]:
        if self._item_count_ < 0:
            ptr = self.address
            while True:
                yield ptr
                ptr += self._item_size_
        else:
            ptr = self.address
            end = self.address + self._item_size_ * self._item_count_
            while ptr < end:
                yield ptr
                ptr += self._item_size_

    def __class_getitem__(cls, item: typing.Tuple[int, int] | int) -> 'type[Arr]':
        if isinstance(item, int):
            item_size = item
            item_count = -1
        else:
            item_size, item_count = item
        assert isinstance(item_size, int) and item_size > 0
        return type(f"Arr<{item_size},{item_count}>", (Arr,), {
            "_item_size_": item_size,
            "_item_count_": item_count
        })


class ItemArr(Arr, typing.Generic[_T]):
    _item_type_: typing.Type[_T]

    def __getitem__(self, idx) -> _T:
        return self._item_type_(self.handle, super().__getitem__(idx))

    def __iter__(self) -> typing.Generator[_T, None, None]:
        for ptr in super().__iter__():
            yield self._item_type_(self.handle, ptr)

    def __class_getitem__(cls, item: typing.Tuple[typing.Type[_T2], int, int] | typing.Tuple[typing.Type[_T2], int]) -> 'type[ItemArr[_T2]]':
        if len(item) == 3:
            item_type, item_size, item_count = item
        else:
            item_type, item_size = item
            item_count = -1
        assert isinstance(item_size, int) and item_size > 0
        return type(f"ItemArr<{item_type.__name__},{item_count}>", (ItemArr,), {
            "_item_size_": item_size,
            "_item_count_": item_count,
            "_item_type_": item_type
        })
