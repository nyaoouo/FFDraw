import dataclasses
import struct
import typing

T = typing.TypeVar('T')  # collections.namedtuple


class NativeNamedTuple(typing.Generic[T]):
    def __init__(self, t: typing.Type[T], p: bytes | str):
        self.struct = struct.Struct(p)
        self.t = t
        self.size = self.struct.size
        self.__name__ = t.__name__

    def unpack(self, buf, offset=0) -> T:
        return self.t._make(self.struct.unpack_from(buf, offset))

    def pack(self, v: T):
        return self.struct.pack(*v)

@dataclasses.dataclass
class NativeDataClass(typing.Generic[T]):
    pass
