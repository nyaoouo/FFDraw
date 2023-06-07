import typing
from nylib.utils.win32 import memory as ny_mem, process as ny_proc

from .utf8string import Utf8String

if typing.TYPE_CHECKING:
    from . import XivMem


class DoTextCommand:
    def __init__(self, main: 'XivMem'):
        self.main = main
        self.handle = main.handle
        self.func_ptr = main.scanner.find_address("48 89 5C 24 ? 57 48 83 EC 20 48 8B FA 48 8B D9 45 84 C9")
        self.p_ui_module, = main.scanner.find_point("48 8B 05 * * * * 48 8B D9 8B 40 14 85 C0")

    def __call__(self, text: str | bytes):
        if isinstance(text, str): text = text.encode('utf-8')
        ui_module = ny_mem.read_address(self.handle, ny_mem.read_address(self.handle, self.p_ui_module))
        string = Utf8String.create(self.handle, text)
        self.main.call_native_once_game_main(self.func_ptr, 'c_void_p', ('c_void_p', 'c_void_p', 'c_void_p', 'c_void_p'), (ui_module, string.address, 0, 0))
        # ny_proc.remote_call(self.handle, self.func_ptr, ui_module, string.address, 0, 0)
        string.free()
