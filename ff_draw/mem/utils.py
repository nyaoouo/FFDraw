import ctypes.wintypes
import re
import typing

from nylib.utils.win32 import memory as ny_mem
from nylib.utils.win32.exception import WinAPIError

_addr_size = ctypes.sizeof(ctypes.c_void_p)
_T = typing.TypeVar('_T')


class direct_mem_property:
    def __init__(self, _type, offset_key=None, default=0):
        self.type = _type
        self.offset_key = offset_key
        self.default = default

    def __set_name__(self, owner, name):
        if not self.offset_key:
            self.offset_key = name

    def __get__(self, instance, owner) -> 'float | int | direct_mem_property':
        if instance is None: return self
        if not (addr := instance.address): return self.default
        try:
            return ny_mem.read_memory(
                instance.handle, self.type,
                addr + getattr(instance.offsets, self.offset_key)).value
        except WinAPIError:
            return self.default


def get_hwnd(pid):
    _p_hwnds = []

    def _filter_func(hwnd, param):
        rtn_value = ctypes.wintypes.DWORD()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(rtn_value))
        if rtn_value.value == pid:
            str_buffer = (ctypes.c_char * 512)()
            ctypes.windll.user32.GetClassNameA(hwnd, str_buffer, 512)
            if str_buffer.value == b'FFXIVGAME': _p_hwnds.append(hwnd)

    _c_filter_func = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)(_filter_func)
    ctypes.windll.user32.EnumWindows(_c_filter_func, 0)
    return _p_hwnds[0] if _p_hwnds else None


def get_game_version_info(file_name):
    with open(file_name, 'rb') as f: base_data = f.read()
    match = re.search(r"/\*{5}ff14\*{6}rev\d+_(\d{4})/(\d{2})/(\d{2})".encode(), base_data)
    game_build_date: str = f"{match.group(1).decode()}.{match.group(2).decode()}.{match.group(3).decode()}.0000.0000"
    match = re.search(r'(\d{3})\\trunk\\prog\\client\\Build\\FFXIVGame\\x64-Release\\ffxiv_dx11.pdb'.encode(),
                      base_data)
    game_version: tuple[int, int, int] = tuple(b - 48 for b in match.group(1))
    return game_version, game_build_date


def read_utf8_string(handle, d: int, encoding='utf-8'):
    return ny_mem.read_string(handle, ny_mem.read_address(handle, d), ny_mem.read_ulonglong(handle, d + 0x10), encoding)


class StdVector(typing.Generic[_T]):
    def __init__(self, handle, address, d_type: typing.Type[_T], d_size):
        self.handle = handle
        self.address = address
        self.d_type = d_type
        self.d_size = d_size

    @property
    def p_start(self):
        return ny_mem.read_address(self.handle, self.address)

    @property
    def p_end(self):
        return ny_mem.read_address(self.handle, self.address + _addr_size)

    def __len__(self):
        return (self.p_end - self.p_start) // self.d_size

    def __getitem__(self, index) -> _T:
        return self.d_type(self.handle, self.p_start + index * self.d_size)

    def __iter__(self) -> typing.Iterator[_T]:
        first = self.p_start
        last = self.p_end
        for i in range((last - first) // self.d_size):
            yield self.d_type(self.handle, first + i * self.d_size)
