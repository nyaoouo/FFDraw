import typing
from nylib.utils.win32 import memory as ny_mem

_T = typing.TypeVar("_T")
_T2 = typing.TypeVar("_T2")


class Pointer(typing.Generic[_T]):
    _item_type_: typing.Type[_T]

    def __init__(self, *args, **kwargs):
        _obj = self._item_type_(*args, **kwargs)
        self.handle = _obj.handle
        self._address = _obj.address

    @property
    def address(self):
        return ny_mem.read_address(self.handle, self._address)

    def __bool__(self):
        return bool(self.address)

    @property
    def content(self) -> _T:
        if address := self.address:
            return self._item_type_(self.handle, address)

    def __class_getitem__(cls, item: typing.Type[_T2]) -> 'typing.Type[Pointer[_T2]]':
        return type(f"Pointer<{item.__name__}>", (Pointer,), {"_item_type_": item})
