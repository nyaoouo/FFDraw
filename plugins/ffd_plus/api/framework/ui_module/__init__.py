import functools
import struct

from ff_draw.mem.utils import struct_mem_property
from nylib.utils import LazyClassAttr
from nylib.utils.win32 import memory as ny_mem
from nylib.utils.imgui import ctx as imgui_ctx
from ffd_plus.api.utils.commons import Utf8String
from ffd_plus.api.utils.mem import ClassFunction, scan_straight
from .pronoun_module import PronounModule
from .rapture_atk_module import RaptureAtkModule


class UiModuleOffsets:
    def __init__(self):
        from ffd_plus.api import Api
        scanner = Api.instance.scanner
        self.atk, = scanner.find_val("4c ? ? <? ? ? ?> 4c ? ? ? ? ? ? 4c ? ? 48 ? ? ? ? 49")

        self.__vfunc_get_pronoun_module_off, = scanner.find_val("ff 50 <?> 44 ? ? ? 48 ? ? ? ? 48 ? ? e8")

    @functools.cached_property
    def pronoun(self):
        from .. import Framework
        ui_module = Framework.instance.ui_module
        handle = ui_module.handle
        p_func = ny_mem.read_address(handle, ny_mem.read_address(handle, ui_module.address) + self.__vfunc_get_pronoun_module_off)
        code = ny_mem.read_bytes(handle, p_func, 8)
        assert code.startswith(b'\x48\x8d\x81') and code.endswith(b'\xc3'), 'func pattern not match'
        return struct.unpack('i', code[3:7])[0]


class UiModule:
    offsets: 'UiModuleOffsets' = LazyClassAttr(UiModuleOffsets)

    def __init__(self, handle, address: int):
        self.handle = handle
        self.address = address

    atk = struct_mem_property(RaptureAtkModule)
    pronoun = struct_mem_property(PronounModule)
    _do_text_command = ClassFunction(scan_straight("48 89 5C 24 ? 57 48 83 EC 20 48 8B FA 48 8B D9 45 84 C9"), "c_void_p", "c_void_p", "c_void_p", "c_void_p", main_loop=True)

    def do_text_command(self, text: str | bytes, set_history=False):
        s = Utf8String.create(self.handle, text)
        self._do_text_command(s.address, 0, int(set_history))

    def render_panel(self):
        with imgui_ctx.TreeNode(f'UiModule#{self.address:X}', push_id=True) as n, n:
            self.atk.render_panel()
            self.pronoun.render_panel()

    def render_game(self):
        self.atk.render_game()
        self.pronoun.render_game()
