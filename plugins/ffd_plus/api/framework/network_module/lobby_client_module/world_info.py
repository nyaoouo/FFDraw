import ctypes

from nylib.utils.win32 import memory as ny_mem
from nylib.utils.imgui import ctx as imgui_ctx
from ff_draw.mem.utils import direct_mem_property, struct_mem_property
from ffd_plus.api.utils import imgui_display_data
from ffd_plus.api.utils.commons import CharArr


class WorldInfo:
    class offsets:
        id = 0X0
        index = 0X2
        param1 = 0X4
        stat1 = 0X8
        stat2 = 0XC
        mode = 0X10
        world_name = 0X14
        display_name = 0X34

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    id = direct_mem_property(ctypes.c_uint16)
    index = direct_mem_property(ctypes.c_uint16)
    param1 = direct_mem_property(ctypes.c_uint8)
    stat1 = direct_mem_property(ctypes.c_uint32)
    stat2 = direct_mem_property(ctypes.c_uint32)
    mode = direct_mem_property(ctypes.c_uint32)
    world_name = struct_mem_property(CharArr[32])
    display_name = struct_mem_property(CharArr[32])

    def render_panel(self, prefix=''):
        world_name = self.world_name.se_string
        display_name = self.display_name.se_string
        title = prefix + (display_name or world_name)
        with imgui_ctx.TreeNode(title + f'#{self.address:X}') as n, n, imgui_ctx.ImguiId(title):
            imgui_display_data('id', self.id)
            imgui_display_data('index', self.index)
            imgui_display_data('param1', self.param1)
            imgui_display_data('stat1', self.stat1)
            imgui_display_data('stat2', self.stat2)
            imgui_display_data('mode', self.mode)
            imgui_display_data('world_name', world_name)
            imgui_display_data('display_name', display_name)
