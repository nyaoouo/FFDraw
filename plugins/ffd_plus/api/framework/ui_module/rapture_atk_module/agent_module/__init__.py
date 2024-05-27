import ctypes
import typing

import imgui

from ff_draw.mem.utils import direct_mem_property, struct_mem_property
from ffd_plus.api.utils.commons import simple_type as st
from ffd_plus.api.utils import imgui_display_data
from nylib.utils.imgui import ctx as imgui_ctx
from .agents.agent_base import AgentBase
from .agents.agent_id import AgentId

_T = typing.TypeVar('_T', bound=AgentBase)


class AgentModuleOffsets:
    p_ui_module = 0X8  # size_t
    is_initialized = 0X10  # bool
    need_update = 0X11  # bool
    frame_cnt = 0X14  # uint32
    delta_sec = 0X18  # float
    agents = 0X20


class AgentModule:
    offsets = AgentModuleOffsets

    def __init__(self, handle, address: int):
        self.handle = handle
        self.address = address

    p_ui_module = direct_mem_property(ctypes.c_size_t)
    is_initialized = direct_mem_property(ctypes.c_int8)
    need_update = direct_mem_property(ctypes.c_int8)
    frame_cnt = direct_mem_property(ctypes.c_uint32)
    delta_sec = direct_mem_property(ctypes.c_float)
    agents = struct_mem_property(st.ptr_arr)

    @property
    def ui_module(self):
        if a := self.p_ui_module:
            from ffd_plus.api.framework.ui_module import UiModule
            return UiModule(self.handle, a)

    def render_panel(self):
        with imgui_ctx.TreeNode(f'AgentModule#{self.address:X}', push_id=True) as n, n:
            imgui_display_data('is_initialized', self.is_initialized)
            imgui_display_data('need_update', self.need_update)
            imgui_display_data('frame_cnt', self.frame_cnt)
            imgui_display_data('delta_sec', self.delta_sec)
            with imgui_ctx.TreeNode(f'agents') as n_, n_:
                for a_id, a_t in AgentBase.agent_types.items():
                    if a := self.get_agent(a_id):
                        a.render_panel()

    def get_agent(self, agent: int | typing.Type[_T]) -> _T | None:
        if not isinstance(agent, int):
            agent_id = agent._agent_id_
            agent_type = agent
        else:
            agent_id = agent
            agent_type = AgentBase.agent_types.get(agent_id, AgentBase)
        if agent_id < 0: return
        if a := self.agents[agent_id]:
            return agent_type(self.handle, a)

    def render_game(self):
        pass
