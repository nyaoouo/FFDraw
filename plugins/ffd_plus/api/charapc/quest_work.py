import ctypes

from ff_draw.mem.utils import direct_mem_property, struct_mem_property
from ffd_plus.api.utils import imgui_display_data
from nylib.utils.imgui import ctx as imgui_ctx
from ffd_plus.api.utils.commons import simple_type as st


class QuestWork:
    class offsets:
        id = 0X8
        seq = 0XA
        flag = 0XB
        vars = 0XC
        class_job = 0X12
        size_ = 0X18

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    id = direct_mem_property(ctypes.c_uint16)
    seq = direct_mem_property(ctypes.c_uint8)
    flag = direct_mem_property(ctypes.c_uint8)
    vars = struct_mem_property(st.uint8_arr[6])
    class_job = direct_mem_property(ctypes.c_uint8)

    def render_panel(self):
        with imgui_ctx.TreeNode(f'QuestWork#{self.address:X}', push_id=True) as n, n:
            imgui_display_data('id', self.id)
            imgui_display_data('seq', self.seq)
            imgui_display_data('flag', self.flag)
            imgui_display_data('vars', self.vars[:])
            imgui_display_data('class_job', self.class_job)

    def render_game(self):
        pass
