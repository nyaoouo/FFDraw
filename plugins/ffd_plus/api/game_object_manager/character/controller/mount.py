import ctypes

from ff_draw.mem.utils import direct_mem_property
from nylib.utils.imgui import ctx as imgui_ctx


class MountController:
    class offsets:
        p_character = 0x8
        p_mount = 0x10
        mount_id = 0x18

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    p_character = direct_mem_property(ctypes.c_size_t)
    p_mount = direct_mem_property(ctypes.c_size_t)
    mount_id = direct_mem_property(ctypes.c_uint16)

    @property
    def character(self):
        if p_character := self.p_character:
            from .. import Character
            return Character(self.handle, p_character)

    @property
    def mount(self):
        if p_mount := self.p_mount:
            from .. import Character
            return Character(self.handle, p_mount)

    def render_panel(self):
        with imgui_ctx.TreeNode(f'Cls#{self.address:X}') as n, n, imgui_ctx.ImguiId('Cls'):
            pass

    def render_game(self):
        pass
