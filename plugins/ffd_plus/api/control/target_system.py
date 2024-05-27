import ctypes

import imgui

from nylib.utils.imgui import ctx as imgui_ctx
from ff_draw.mem.utils import struct_mem_property, direct_mem_property
from ffd_plus.api.utils.commons import CharArr
from ffd_plus.api.utils.mem import ClassFunction, scan_straight
from ffd_plus.api.game_object_manager import GameObject, GameObjectManager


class TargetSystem:
    class offsets:
        current_target = 0x80
        mouse_over_target = 0xD0
        mouse_click_target = 0xD8
        ui_over_target = 0xE0
        mouse_nearest_target = 0xE8
        focus_target = 0xF8

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    current_target = struct_mem_property(GameObject, is_pointer=True)
    mouse_over_target = struct_mem_property(GameObject, is_pointer=True)
    mouse_click_target = struct_mem_property(GameObject, is_pointer=True)
    ui_over_target = struct_mem_property(GameObject, is_pointer=True)
    mouse_nearest_target = struct_mem_property(GameObject, is_pointer=True)
    focus_target = struct_mem_property(GameObject, is_pointer=True)

    _talk_to_npc = ClassFunction(scan_straight(
        "48 89 5c 24 ? 48 89 6c 24 ? 56 48 ? ? ? 48 ? ? 41 ? ? ? 48"
    ), 'c_void_p', 'c_void_p', 'c_uint8')

    def talk_to_npc(self, target: GameObject | int, check_sight: bool = True):
        if isinstance(target, int):
            if (target := GameObjectManager.instance.get_object_by_common_id(target)) is None:
                raise ValueError(f"Cannot find entity with common_id {target:X}")
        return self._talk_to_npc(self.address, target.address, int(check_sight))

    def render_panel(self):
        pass
