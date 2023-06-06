import typing
from nylib.utils.win32 import memory as ny_mem, process as ny_proc

if typing.TYPE_CHECKING:
    from . import XivMem


class Utf8String:
    _p_init: int
    _p_del: int
    _p_set: int

    def __init__(self, handle, address, ns):
        self.handle = handle
        self.ns = ns
        self.address = address

    @classmethod
    def create(cls, handle, content):
        ns = ny_mem.Namespace(handle)
        address = ns.take(0x64)
        ny_proc.remote_call(handle, cls._p_init, address, content, len(content))
        return cls(handle, address, ns)

    @classmethod
    def from_address(cls, handle, address):
        return cls(handle, address, None)

    @property
    def content(self):
        return ny_mem.read_bytes(self.handle, ny_mem.read_address(self.handle, self.address), ny_mem.read_uint64(self.handle, self.address + 16))

    @content.setter
    def content(self, value):
        ny_proc.remote_call(self.handle, self._p_set, self.address, value, len(value))

    def free(self):
        if self.ns:
            ny_proc.remote_call(self.handle, self._p_del, self.address)
            self.ns.free()
            self.ns = None

    def __del__(self):
        self.free()

    @classmethod
    def init_cls(cls, mem: 'XivMem'):
        cls._p_init = mem.scanner.find_address("48 89 5C 24 08 48 89 74 24 10 57 48 83 EC 20 48 8D 41 22 66 C7 41 20 01 01 48 89 01 49 8B D8")
        cls._p_del = mem.scanner.find_address("80 79 21 00 75 12 48 8B 51 08 41 B8 33 00 00 00 48 8B 09 E9 ?? ?? ?? 00 C3")
        cls._p_set, = mem.scanner.find_point("e8 * * * * 48 ? ? e8 ? ? ? ? 48 ? ? ? ? 48 ? ? ? ? 4c ? ? ? ? 48")
