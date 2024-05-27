import struct
import typing

import glm

from nylib.utils.imgui import ctx as imgui_ctx
from nylib.utils.win32 import memory as ny_mem
from ...utils.mem import ClassFunction, scan_val

if typing.TYPE_CHECKING:
    from .. import Framework


class BgCollisionModule:
    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    _ray_cast = ClassFunction(scan_val("e8 * * * * 84 ? 0f 84 ? ? ? ? 48 83 7b"), 'c_bool', 'c_void_p', 'c_size_t', 'c_char_p', 'c_char_p', 'c_float', 'c_uint', 'c_char_p')

    def ray_cast(self, area: glm.vec3, facing: glm.vec3, length: float, flag, mask, cmp):
        with ny_mem.RemoteMemory(self.handle, 0xa0) as rm:
            if self._ray_cast(rm.address, area.to_bytes(), facing.to_bytes(), length, flag, struct.pack('QQ', mask, cmp)):
                return glm.vec3.from_bytes(bytes(ny_mem.read_bytes(self.handle, rm.address, 12)))

    def render_panel(self):
        with imgui_ctx.TreeNode(f'BgCollisionModule#{self.address:X}') as n, n, imgui_ctx.ImguiId('BgCollisionModule'):
            pass

    def render_game(self):
        pass
