import ctypes

from nylib.utils.win32 import memory as ny_mem
from nylib.utils.imgui import ctx as imgui_ctx
from ff_draw.mem.utils import direct_mem_property, struct_mem_property
from ffd_plus.api.utils import imgui_display_data
from ffd_plus.api.utils.commons import CharArr


class CharacterInfo:
    class offsets:
        player_id = 0X0
        character_id = 0X8
        index = 0X10
        param1 = 0X11
        status = 0X12
        param2 = 0X14
        world_id = 0X18
        home_world_id = 0X1A
        save_time = 0X1C
        save_platform = 0X20
        save_error = 0X24
        token = 0X28
        name = 0X2C
        world_name = 0X4C
        home_world_name = 0X6C
        graphic_data = 0X8C

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    player_id = direct_mem_property(ctypes.c_uint64)
    character_id = direct_mem_property(ctypes.c_uint64)
    index = direct_mem_property(ctypes.c_uint8)
    param1 = direct_mem_property(ctypes.c_uint8)
    status = direct_mem_property(ctypes.c_uint16)
    param2 = direct_mem_property(ctypes.c_uint32)
    world_id = direct_mem_property(ctypes.c_uint16)
    home_world_id = direct_mem_property(ctypes.c_uint16)
    save_time = direct_mem_property(ctypes.c_uint32)
    save_platform = direct_mem_property(ctypes.c_uint32)
    save_error = direct_mem_property(ctypes.c_uint8)
    token = direct_mem_property(ctypes.c_uint32)

    name = struct_mem_property(CharArr[32])
    world_name = struct_mem_property(CharArr[32])
    home_world_name = struct_mem_property(CharArr[32])

    graphic_data = direct_mem_property(ctypes.c_uint8 * 1024)

    def render_panel(self, prefix=''):
        title = prefix + str(home_world_name := self.home_world_name.se_string) + ' - ' + str(name := self.name.se_string)
        with imgui_ctx.TreeNode(title + f'#{self.address:X}') as n, n, imgui_ctx.ImguiId(title):
            imgui_display_data('player_id', self.player_id)
            imgui_display_data('character_id', self.character_id)
            imgui_display_data('index', self.index)
            imgui_display_data('param1', self.param1)
            imgui_display_data('status', self.status)
            imgui_display_data('param2', self.param2)
            imgui_display_data('world_id', self.world_id)
            imgui_display_data('home_world_id', self.home_world_id)
            imgui_display_data('save_time', self.save_time)
            imgui_display_data('save_platform', self.save_platform)
            imgui_display_data('save_error', self.save_error)
            imgui_display_data('token', self.token)
            imgui_display_data('name', name)
            imgui_display_data('world_name', self.world_name)
            imgui_display_data('home_world_name', home_world_name)


class CharacterInfo11:
    class offsets:
        id = 0X0
        index = 0X4
        param1 = 0X5
        status = 0X6
        name = 0X8

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    id = direct_mem_property(ctypes.c_uint32)
    index = direct_mem_property(ctypes.c_uint8)
    param1 = direct_mem_property(ctypes.c_uint8)
    status = direct_mem_property(ctypes.c_uint16)

    @property
    def name(self):
        return ny_mem.read_string(self.handle, self.address + self.offsets.name, 32)

    def render_panel(self, prefix=''):
        title = prefix + (name := self.name)
        with imgui_ctx.TreeNode(title + f'#{self.address:X}') as n, n, imgui_ctx.ImguiId(title):
            imgui_display_data('id', self.id)
            imgui_display_data('index', self.index)
            imgui_display_data('param1', self.param1)
            imgui_display_data('status', self.status)
            imgui_display_data('name', name)
