import ctypes
import dataclasses
import enum
import typing
from typing import TypeVar, Generic

from .structs import IpcHeader, BundleHeader, ElementHeader

T = TypeVar('T')
T2 = TypeVar('T2')
_header_size = ctypes.sizeof(IpcHeader)


@dataclasses.dataclass
class IpcMessage(Generic[T]):
    bundle_header: BundleHeader
    el_header: ElementHeader
    element: IpcHeader
    message: T
    raw_data: bytearray


@dataclasses.dataclass
class ElementMessage(Generic[T]):
    bundle_header: BundleHeader
    el_header: ElementHeader
    element: T
    raw_data: bytearray

    def to_ipc(self, other: typing.Type[T2] = None) -> IpcMessage[T2]:
        assert isinstance(self.element, IpcHeader)
        if other is None:
            msg = memoryview(self.raw_data)[_header_size:]
        else:
            msg = other.from_buffer(self.raw_data, _header_size)
        return IpcMessage(self.bundle_header, self.el_header, self.element, msg, self.raw_data)


@dataclasses.dataclass
class BaseMessage:
    bundle_header: BundleHeader
    el_header: ElementHeader
    raw_data: bytearray

    def to_el(self, other: typing.Type[T] = None) -> ElementMessage[T]:
        raw = self.raw_data
        if other:
            el = other.from_buffer(raw)
        else:
            el = memoryview(raw)
        return ElementMessage(self.bundle_header, self.el_header, el, raw)

    def to_ipc(self, other: typing.Type[T]) -> IpcMessage[T]:
        return self.to_el(IpcHeader).to_ipc(other)


@dataclasses.dataclass
class NetworkMessage(Generic[T]):
    proto_no: enum.Enum | int
    raw_message: ElementMessage[IpcHeader] | IpcMessage[T]
    header: ElementHeader
    message: T


@dataclasses.dataclass
class ActorControlMessage(Generic[T]):
    raw_msg: NetworkMessage
    id: int
    args: list[int]
    param: T = None
    source_id: int = 0xe0000000
    target_id: int = 0xe0000000

    def __str__(self):
        return f'ActorControl {self.id}\t{self.source_id:#x}=>{self.target_id:#x} ' + (
            str(self.param) if self.param else '/'.join(map(str, self.args))
        )


@dataclasses.dataclass
class PlayActionTimelineMessage(Generic[T]):
    raw_msg: NetworkMessage|ActorControlMessage
    id: int
    timeline_id: int
