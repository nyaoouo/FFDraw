from ctypes import *
from ctypes.wintypes import *
from typing import TypeVar, Type, Callable
from .winapi import structure, kernel32
from .exception import WinAPIError


def alloc(
        handle,
        size: int,
        allocation_type=structure.MEMORY_STATE.MEM_COMMIT.value,
        protection_type=structure.MEMORY_PROTECTION.PAGE_EXECUTE_READWRITE.value
) -> int:
    windll.kernel32.SetLastError(0)
    address = kernel32.VirtualAllocEx(
        handle,
        None,
        size,
        allocation_type,
        protection_type
    )
    err_code = kernel32.GetLastError()
    if err_code: raise WinAPIError(err_code, "VirtualAllocEx")
    return address


def iter_memory_region(handle, start=0, end=None):
    pos = start
    mbi = structure.MEMORY_BASIC_INFORMATION()
    size = sizeof(structure.MEMORY_BASIC_INFORMATION)
    while kernel32.VirtualQueryEx(
            handle,
            pos,
            byref(mbi),
            sizeof(mbi)
    ) == size:
        if mbi.Protect & 256 != 256 and mbi.Protect & 4 == 4:
            yield mbi.BaseAddress, mbi.RegionSize
        next_addr = mbi.BaseAddress + mbi.RegionSize
        if pos >= next_addr or end is not None and end < next_addr: break
        pos = next_addr


_t = TypeVar('_t')


def read_memory(handle, d_type: Type[_t], address: int) -> _t:
    buf = d_type()
    windll.kernel32.SetLastError(0)
    if kernel32.ReadProcessMemory(
            handle,
            address,
            byref(buf),
            sizeof(buf),
            None
    ): return buf
    raise WinAPIError(kernel32.GetLastError(), "ReadProcessMemory")


def write_memory(handle, address: int, data: _t) -> _t:
    windll.kernel32.SetLastError(0)
    if kernel32.WriteProcessMemory(
            handle,
            address,
            byref(data),
            sizeof(data),
            None
    ): return data
    raise WinAPIError(kernel32.GetLastError(), "WriteProcessMemory")


def read_bytes(handle, address: int, size: int) -> bytearray:
    buf = bytearray(size)
    _buf = (c_ubyte * size).from_buffer(buf)
    windll.kernel32.SetLastError(0)
    if kernel32.ReadProcessMemory(
            handle,
            address,
            _buf,
            size,
            None
    ): return buf
    raise WinAPIError(kernel32.GetLastError(), "ReadProcessMemory")


def write_bytes(handle, address: int, data: bytearray | bytes) -> bytearray:
    if isinstance(data, bytes): data = bytearray(data)
    size = len(data)
    _buf = (c_ubyte * size).from_buffer(data)
    windll.kernel32.SetLastError(0)
    if kernel32.WriteProcessMemory(
            handle,
            address,
            _buf,
            size,
            None
    ): return data
    raise WinAPIError(kernel32.GetLastError(), "WriteProcessMemory")


num_size_map = {
    8: c_uint8,
    9: c_int8,
    16: c_uint16,
    17: c_int16,
    32: c_uint32,
    33: c_int32,
    64: c_uint64,
    65: c_int64,
}


def read_num_func(size: int, signed=True) -> Callable[[any, int], int]:
    if size % 8 or size not in num_size_map: raise ValueError(f"Invalid size {size}")
    d_type = num_size_map[size + signed]

    def func(handle, address: int) -> int:
        return read_memory(handle, d_type, address).value

    return func


def write_num_func(size: int, signed=True) -> Callable[[any, int, int], int]:
    if size % 8 or size not in num_size_map: raise ValueError(f"Invalid size {size}")
    d_type = num_size_map[size + signed]

    def func(handle, address: int, value: int) -> int:
        return write_memory(handle, address, d_type(value)).value

    return func


def read_float(handle, address: int) -> float:
    return read_memory(handle, c_float, address).value


def write_float(handle, address: int, value: float | int) -> float:
    return write_memory(handle, address, c_float(value)).value


def read_string(handle, address: int, max_length: int = 255, encoding='utf-8') -> str | bytearray:
    res = read_bytes(handle, address, max_length)
    if encoding:
        return res.split(b'\0')[0].decode(encoding, 'ignore')
    return res


def write_string(handle, address: int, value: str | bytearray | bytes) -> bytearray:
    if isinstance(value, str): value = value.encode(structure.DEFAULT_CODING)
    if isinstance(value, bytes): value = bytearray(value)
    return write_bytes(handle, address, value)


def read_string_safe(handle, address: int, max_length: int = 255, encoding='utf-8') -> str:
    data = bytearray()
    for i in range(max_length):
        try:
            new_byte = read_ubyte(handle, address + i)
        except WinAPIError:
            break
        if not new_byte: break
        data.append(new_byte)
    return data.decode(encoding)


r_ui8 = read_uint8 = read_num_func(8, False)
w_ui8 = write_uint8 = write_num_func(8, False)
r_i8 = read_int8 = read_num_func(8, True)
w_i8 = write_int8 = write_num_func(8, True)
r_ui16 = read_uint16 = read_num_func(16, False)
w_ui16 = write_uint16 = write_num_func(16, False)
r_i16 = read_int16 = read_num_func(16, True)
w_i16 = write_int16 = write_num_func(16, True)
r_ui32 = read_uint32 = read_num_func(32, False)
w_ui32 = write_uint32 = write_num_func(32, False)
r_i32 = read_int32 = read_num_func(32, True)
w_i32 = write_int32 = write_num_func(32, True)
r_ui64 = read_uint64 = read_num_func(64, False)
w_ui64 = write_uint64 = write_num_func(64, False)
r_i64 = read_int64 = read_num_func(64, True)
w_i64 = write_int64 = write_num_func(64, True)
r_ub = read_ubyte = read_num_func(sizeof(c_ubyte) * 8, False)
w_ub = write_ubyte = write_num_func(sizeof(c_ubyte) * 8, False)
r_b = read_byte = read_num_func(sizeof(c_byte) * 8, True)
w_b = write_byte = write_num_func(sizeof(c_byte) * 8, True)
r_us = read_ushort = read_num_func(sizeof(c_ushort) * 8, False)
w_us = write_ushort = write_num_func(sizeof(c_ushort) * 8, False)
r_s = read_short = read_num_func(sizeof(c_short) * 8, True)
w_s = write_short = write_num_func(sizeof(c_short) * 8, True)
r_ui = read_uint = read_num_func(sizeof(c_uint) * 8, False)
w_ui = write_uint = write_num_func(sizeof(c_uint) * 8, False)
r_i = read_int = read_num_func(sizeof(c_int) * 8, True)
w_i = write_int = write_num_func(sizeof(c_int) * 8, True)
r_ul = read_ulong = read_num_func(sizeof(c_ulong) * 8, False)
w_ul = write_ulong = write_num_func(sizeof(c_ulong) * 8, False)
r_l = read_long = read_num_func(sizeof(c_long) * 8, True)
w_l = write_long = write_num_func(sizeof(c_long) * 8, True)
r_ull = read_ulonglong = read_num_func(sizeof(c_ulonglong) * 8, False)
w_ull = write_ulonglong = write_num_func(sizeof(c_ulonglong) * 8, False)
r_ll = read_longlong = read_num_func(sizeof(c_longlong) * 8, True)
w_ll = write_longlong = write_num_func(sizeof(c_longlong) * 8, True)
read_word = read_num_func(sizeof(WORD) * 8, False)
write_word = write_num_func(sizeof(WORD) * 8, False)
read_dword = read_num_func(sizeof(WORD) * 8 * 2, False)
write_dword = write_num_func(sizeof(WORD) * 8 * 2, False)
read_qword = read_num_func(sizeof(WORD) * 8 * 4, False)
write_qword = write_num_func(sizeof(WORD) * 8 * 4, False)
r_a = read_address = read_num_func(sizeof(c_void_p) * 8, False)
w_a = write_address = write_num_func(sizeof(c_void_p) * 8, False)
r_f = read_float
w_f = write_float
rm = read_memory
wm = write_memory
r_st = read_string
w_st = write_string
r_sts = read_string_safe


class RemoteMemory:
    def __init__(self, handle, size):
        self.handle = handle
        self.size = size
        self.address = None

    def alloc(self, init_data: bytes = None):
        if self.address is None:
            self.address = alloc(self.handle, self.size, structure.MEMORY_STATE.MEM_COMMIT | structure.MEMORY_STATE.MEM_RESERVE)
        if init_data is not None:
            self.value = init_data
        return self

    def free(self):
        if self.address is not None:
            kernel32.VirtualFreeEx(self.handle, self.address, self.size, structure.MEMORY_STATE.MEM_DECOMMIT | structure.MEMORY_STATE.MEM_RELEASE)
        return self

    def __enter__(self):
        return self.alloc()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.free()

    @property
    def value(self):
        return read_bytes(self.handle, self.address, self.size)

    @value.setter
    def value(self, v: bytes):
        write_bytes(self.handle, self.address, v[:self.size])


aligned4 = lambda v: (v + 0x3) & (~0x3)
aligned16 = lambda v: (v + 0xf) & (~0xf)


class Namespace:
    chunk_size = 0x10000

    def __init__(self, handle):
        self.handle = handle
        self.res = []
        self.ptr = 0
        self.remain = 0

    def store(self, data: bytes):
        write_bytes(self.handle, (p_buf := self.take(len(data))), data)
        return p_buf

    def take(self, size):
        size = aligned16(size)
        if self.remain < size:
            alloc_size = max(self.chunk_size, size)
            self.res.append(new_mem := RemoteMemory(self.handle, alloc_size).alloc())
            self.remain = alloc_size - size
            self.ptr = new_mem.address + size
            return new_mem.address
        else:
            self.remain -= size
            res = self.ptr
            self.ptr += size
            return res

    def free(self):
        for chunk in self.res:
            chunk.free()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.free()
