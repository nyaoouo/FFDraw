from ff_draw.mem.utils import struct_mem_property
from nylib.utils.imgui import ctx as imgui_ctx


class PronounModule:
    class offsets:
        pass

    def __init__(self, handle, address: int):
        self.handle = handle
        self.address = address

    def render_panel(self):
        with imgui_ctx.TreeNode(f'PronounModule#{self.address:X}', push_id=True) as n, n:
            pass

    def render_game(self):
        pass
