import ctypes.wintypes
import re
from nylib.utils.win32 import memory as ny_mem


class direct_mem_property:
    def __init__(self, _type, offset_key=None):
        self.type = _type
        self.offset_key = offset_key

    def __set_name__(self, owner, name):
        if not self.offset_key:
            self.offset_key = name

    def __get__(self, instance, owner) -> 'float | int | direct_mem_property':
        if instance is None: return self
        return ny_mem.read_memory(instance.handle, self.type, instance.address + getattr(instance.offsets, self.offset_key)).value


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
    match = re.search(r'(\d{3})\\trunk\\prog\\client\\Build\\FFXIVGame\\x64-Release\\ffxiv_dx11.pdb'.encode(), base_data)
    game_version: tuple[int, int, int] = tuple(b - 48 for b in match.group(1))
    return game_version, game_build_date
