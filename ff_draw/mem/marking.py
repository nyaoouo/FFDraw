import typing
import glm
from nylib.utils.win32 import memory as ny_mem

if typing.TYPE_CHECKING:
    from . import XivMem


class WayMark:
    a = 0
    b = 1
    c = 2
    d = 3
    n1 = 4
    n2 = 5
    n3 = 6
    n4 = 7

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    @property
    def pos(self):
        return glm.vec3.from_bytes(bytes(ny_mem.read_bytes(self.handle, self.address, 0xc)))

    @property
    def is_enable(self):
        return ny_mem.read_byte(self.handle, self.address + 0x1c) != 0


class MarkingController:
    def __init__(self, main: 'XivMem'):
        self.main = main
        self.handle = main.handle
        self.address = main.scanner.find_point('48 8D ? * * * * 41 B0 ? E8 ? ? ? ? 85 C0')[0]
        self.way_marks = [WayMark(self.handle, self.address + 0x1b0 + (i * 0x20)) for i in range(8)]
