import ctypes
import typing

from ff_draw.mem.utils import direct_mem_property
from nylib.utils.imgui import ctx as imgui_ctx


class AgentBase:
    _agent_id_: int
    agent_types: 'dict[int,typing.Type[AgentBase]]' = {}

    def __init_subclass__(cls, **kwargs):
        if hasattr(cls, '_agent_id_'):
            cls.agent_types[cls._agent_id_] = cls

    class offsets:
        flag = 0X8
        p_ui_module = 0X10
        p_event = 0X18
        addon_id = 0X20

    flag = direct_mem_property(ctypes.c_uint8)
    p_ui_module = direct_mem_property(ctypes.c_size_t)
    p_event = direct_mem_property(ctypes.c_size_t)
    addon_id = direct_mem_property(ctypes.c_uint32)

    def __init__(self, handle, address: int):
        self.handle = handle
        self.address = address

    def render_panel(self):
        with imgui_ctx.TreeNode(f'{self.__class__.__name__}#{self.address:X}', push_id=True) as n, n:
            self.render_panel_extra()

    def render_panel_extra(self):
        pass

    def render_game(self):
        pass
