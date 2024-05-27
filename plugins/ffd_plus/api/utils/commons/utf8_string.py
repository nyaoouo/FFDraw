import ctypes
from nylib.utils.win32 import memory as ny_mem,process as ny_proc
from ff_draw.mem.utils import direct_mem_property
from ffd_plus.api.utils.mem import ClassFunction, scan_val,scan_straight
from fpt4.utils.se_string import SeString


class Utf8String:  # size:0x68
    class offsets:
        p_buffer = 0x0
        buffer_size = 0x8
        buffer_used = 0x10
        data_length = 0x18

    def __init__(self, handle, address, _self_allocated:ny_mem.RemoteMemory=None):
        self.handle = handle
        self.address = address
        self._self_allocated = _self_allocated

    p_buffer = direct_mem_property(ctypes.c_size_t)
    buffer_size = direct_mem_property(ctypes.c_uint64)
    buffer_used = direct_mem_property(ctypes.c_uint64)
    data_length = direct_mem_property(ctypes.c_uint64)

    @property
    def se_string(self):
        if val := self.value:
            return SeString.from_buffer(val)
        return val

    @property
    def value(self) -> bytearray | None:
        if p_buffer := self.p_buffer:
            return ny_mem.read_bytes(self.handle, p_buffer, self.buffer_used)

    _init_by_char_p = ClassFunction(scan_straight("48 89 5C 24 08 48 89 74 24 10 57 48 83 EC 20 48 8D 41 22 66 C7 41 20 01 01 48 89 01 49 8B D8"), "c_void_p", "c_char_p", "c_size_t")
    _set_value = ClassFunction(scan_val("e8 * * * * 48 ? ? e8 ? ? ? ? 48 ? ? ? ? 48 ? ? ? ? 4c ? ? ? ? 48"), "c_void_p", "c_char_p", "c_size_t")
    _destruct = ClassFunction(scan_straight("80 79 21 00 75 12 48 8B 51 08 41 B8 33 00 00 00 48 8B 09 E9 ?? ?? ?? 00 C3"), "c_void_p")

    def __del__(self):
        if self._self_allocated:
            self._destruct()
            self._self_allocated.free()
            self.address = 0

    @classmethod
    def create(cls, handle, value: str | bytes | bytearray = b''):
        if isinstance(value, str):
            value = value.encode("utf-8")
        elif isinstance(value, bytearray):
            value = bytes(value)
        mem = ny_mem.RemoteMemory(handle, 0x68).alloc()
        obj = cls(handle, mem.address, mem)
        obj._init_by_char_p(value, len(value))
        return obj

    @value.setter
    def value(self, value: str | bytes | bytearray):
        if isinstance(value, str):
            value = value.encode("utf-8")
        elif isinstance(value, bytearray):
            value = bytes(value)
        self._set_value(value, len(value))
