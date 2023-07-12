import ctypes
import typing

import glm
import imgui

from nylib.utils.imgui import ctx as imgui_ctx
from nylib.utils.win32 import memory as ny_mem
from .utils import direct_mem_property

if typing.TYPE_CHECKING:
    from . import XivMem


class MoveControllerSelf:
    class offsets:
        vector = 0x10
        camera_facing = 0X2C
        camera_speed_min = 0x30
        camera_speed_max = 0x34
        camera_move_rate = 0x38
        is_moving = 0x3C
        is_rotating = 0x3D
        want_jump = 0X40
        current_move_speed = 0x44
        current_rotate_speed = 0x48

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    @property
    def vector(self):
        return glm.vec3.from_bytes(bytes(ny_mem.read_bytes(self.handle, self.address + self.offsets.vector, 0xc)))

    camera_facing = direct_mem_property(ctypes.c_float)
    camera_speed_min = direct_mem_property(ctypes.c_float)
    camera_speed_max = direct_mem_property(ctypes.c_float)
    camera_move_rate = direct_mem_property(ctypes.c_float)
    is_moving = direct_mem_property(ctypes.c_uint8)
    is_rotating = direct_mem_property(ctypes.c_uint8)
    want_jump = direct_mem_property(ctypes.c_uint8)
    current_move_speed = direct_mem_property(ctypes.c_float)
    current_rotate_speed = direct_mem_property(ctypes.c_float)

    def render_debug(self):
        vec = self.vector
        imgui.text(f'vector: {vec.x:.2f}, {vec.y:.2f}, {vec.z:.2f}')
        imgui.text(f'camera_facing: {self.camera_facing:.2f}')
        imgui.text(f'camera_speed_min: {self.camera_speed_min:.2f}')
        imgui.text(f'camera_speed_max: {self.camera_speed_max:.2f}')
        imgui.text(f'camera_move_rate: {self.camera_move_rate:.2f}')
        imgui.text(f'is_moving: {self.is_moving}')
        imgui.text(f'is_rotating: {self.is_rotating}')
        imgui.text(f'want_jump: {self.want_jump}')
        imgui.text(f'current_move_speed: {self.current_move_speed:.2f}')
        imgui.text(f'current_rotate_speed: {self.current_rotate_speed:.2f}')


class MoveController:
    class offsets:
        self_controller = 0x10

    def __init__(self, main: 'XivMem'):
        self.main = main
        self.handle = main.handle
        self.address, = main.scanner.find_point('48 ? ? * * * * c6 40 ? ? e8 ? ? ? ? f3')

    @property
    def self_controller(self):
        return MoveControllerSelf(self.handle, self.address + self.offsets.self_controller)

    def render_debug(self):
        with imgui_ctx.TreeNode('self_controller') as n, n:
            self.self_controller.render_debug()
