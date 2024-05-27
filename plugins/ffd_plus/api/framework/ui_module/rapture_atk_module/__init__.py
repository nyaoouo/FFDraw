from ff_draw.mem.utils import struct_mem_property
from nylib.utils.imgui import ctx as imgui_ctx
from .agent_module import AgentModule


class RaptureAtkModuleOffsets:
    def __init__(self):
        from ffd_plus.api import Api
        scanner = Api.instance.scanner
        self.agents, = scanner.find_val("48 ? ? <? ? ? ?> ba ? ? ? ? e8 ? ? ? ? 48 ? ? b2 ? 48")


class RaptureAtkModule:
    offsets: 'RaptureAtkModuleOffsets' = None

    def __init__(self, handle, address: int):
        self.handle = handle
        self.address = address
        if RaptureAtkModule.offsets is None:
            RaptureAtkModule.offsets = RaptureAtkModuleOffsets()

    agents = struct_mem_property(AgentModule)

    def render_panel(self):
        with imgui_ctx.TreeNode(f'RaptureAtkModule#{self.address:X}', push_id=True) as n, n:
            self.agents.render_panel()

    def render_game(self):
        self.agents.render_game()
