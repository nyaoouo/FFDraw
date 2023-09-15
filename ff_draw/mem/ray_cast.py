import ctypes
import struct
import typing
import win32gui
import glm

from nylib.utils.win32 import memory as ny_mem

if typing.TYPE_CHECKING:
    from . import XivMem

shell = f'from ctypes import *\nres=CFUNCTYPE(c_bool,c_void_p,c_size_t,c_char_p,c_char_p,c_float,c_uint,c_char_p)(args[0])(*args[1:])'

default_mask = bytes((ctypes.c_int * 3)(0x00004000, 0x00004000, 0x0))


def trans(v4: glm.vec4): return glm.vec3(v4 / v4.w)


class RayCast:
    class Flag:
        terrain = 1 << 0
        trigger_box = 1 << 1
        exit_range = 1 << 2
        map_range = 1 << 3
        event_range = 1 << 4
        water_range = 1 << 7

    def __init__(self, main: 'XivMem'):
        self.main = main
        self.handle = main.handle
        self.p_func, = main.scanner_v2.find_val("e8 * * * * 84 ? 0f 84 ? ? ? ? 48 83 7b")
        self.off_collision_module, = main.scanner_v2.find_val("48 ? ? <? ? ? ?> f3 ? ? ? f3 ? ? ? f3 ? ? ? e8 ? ? ? ? f3 ? ? ? 48")

    @property
    def p_module(self):
        return ny_mem.read_address(self.handle, self.main.p_framework + self.off_collision_module)

    def __call__(self, area: glm.vec3, facing: glm.vec3, length: float, flag, mask, cmp):
        with ny_mem.RemoteMemory(self.handle, 0xa0) as rm:
            if self.main.call_once_game_main(
                    shell, self.p_func, self.p_module, rm.address,
                    area.to_bytes(), facing.to_bytes(), length, flag, struct.pack('QQ', mask, cmp)
            ):
                return glm.vec3.from_bytes(bytes(ny_mem.read_bytes(self.handle, rm.address, 12)))

    def screen_to_world(self, local_x, local_y, ray_distance=10000):
        mvp, (width, height) = self.main.load_screen()
        rev_mvp = glm.inverse(mvp)
        screen_pos_3d = glm.vec4(local_x / width * 2 - 1, -(local_y / height * 2 - 1), 0, 1)
        near_pos = trans(rev_mvp * screen_pos_3d)
        screen_pos_3d.z = 1
        facing = glm.normalize(trans(rev_mvp * screen_pos_3d) - near_pos)
        return self(near_pos, facing, ray_distance, self.Flag.terrain, 1 << 27 | 1 << 14, 0)

    def cursor_to_world(self):
        x, y = win32gui.GetCursorPos()
        x1, y1, x2, y2 = win32gui.GetWindowRect(self.main.hwnd)
        if not (x1 < x < x2 and y1 < y < y2): return None
        return self.screen_to_world(x - x1, y - y1)
