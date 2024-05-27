import ctypes

from ffd_plus.api.utils.commons import CharArr
from nylib.utils.imgui import ctx as imgui_ctx
from ff_draw.mem.utils import direct_mem_property, struct_mem_property
from ffd_plus.api.utils import imgui_display_data


class AccountInfo:  # LobbyProtoDownAccountInfo
    class offsets:
        id = 0X0
        index = 0X8
        param = 0X9
        status = 0XA
        name = 0XC

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    id = direct_mem_property(ctypes.c_uint64)
    index = direct_mem_property(ctypes.c_uint8)
    param = direct_mem_property(ctypes.c_uint8)
    status = direct_mem_property(ctypes.c_uint16)
    name = struct_mem_property(CharArr[64])

    def render_panel(self, prefix: str = ''):
        ac_id = self.id
        name = self.name.value.decode('utf-8')
        title = f"{prefix}{name}-{ac_id}"
        with imgui_ctx.TreeNode(title + f'#{self.address:X}') as n, n, imgui_ctx.ImguiId(title):
            imgui_display_data('id', self.id)
            imgui_display_data('index', self.index)
            imgui_display_data('param', self.param)
            imgui_display_data('status', self.status)
            imgui_display_data('name', name)
