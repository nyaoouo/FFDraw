import ctypes

from ff_draw.mem.utils import direct_mem_property
from ffd_plus.api.utils import imgui_display_data
from .agent_base import AgentBase
from .agent_id import AgentId


class AgentCountDown(AgentBase):
    _agent_id_ = AgentId.countdown

    class offsets:
        counter = 0X28  # float
        prev_counter = 0X2C  # float
        dialog_id = 0X30  # int32
        screen_id = 0X34  # int32
        is_count = 0X38  # int8
        is_text_command = 0X39  # int8
        is_log = 0X3A  # int8
        count_starter = 0X3C  # uint32
        is_show_screen = 0X40  # int8
        is_working = 0X41  # int8

    counter = direct_mem_property(ctypes.c_float)
    prev_counter = direct_mem_property(ctypes.c_float)
    dialog_id = direct_mem_property(ctypes.c_int32)
    screen_id = direct_mem_property(ctypes.c_int32)
    is_count = direct_mem_property(ctypes.c_int8)
    is_text_command = direct_mem_property(ctypes.c_int8)
    is_log = direct_mem_property(ctypes.c_int8)
    count_starter = direct_mem_property(ctypes.c_uint32)
    is_show_screen = direct_mem_property(ctypes.c_int8)
    is_working = direct_mem_property(ctypes.c_int8)

    def render_panel_extra(self):
        imgui_display_data('counter', self.counter)
        imgui_display_data('prev_counter', self.prev_counter)
        imgui_display_data('dialog_id', self.dialog_id)
        imgui_display_data('screen_id', self.screen_id)
        imgui_display_data('is_count', self.is_count)
        imgui_display_data('is_text_command', self.is_text_command)
        imgui_display_data('is_log', self.is_log)
        imgui_display_data('count_starter', self.count_starter)
        imgui_display_data('is_show_screen', self.is_show_screen)
        imgui_display_data('is_working', self.is_working)

