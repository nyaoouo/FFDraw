import ctypes

import glm
import time
import typing
import imgui

from nylib.utils.win32 import memory as ny_mem
from nylib.utils.imgui import ctx as imgui_ctx
from ff_draw.mem.utils import direct_mem_property, glm_mem_property, struct_mem_property
from ffd_plus.api.utils.mem import ClassFunction, StaticFunction, scan_val, scan_straight
from ffd_plus.api.utils.commons.game import RecastInfo
from ffd_plus.api.control import Control
from ffd_plus.api.ui import UiManager
from ffd_plus.api.game_main import GameMain
from ffd_plus.api.condition_manager import ConditionManager
from ffd_plus.api.utils import sq_pack
from ffd_plus.api.utils.commons import ItemArr
from .utils import *

if typing.TYPE_CHECKING:
    from .. import Api


class CastInfo:
    class offsets:
        request_id = 0x0
        real_action_id = 0x4
        action_kind = 0x8
        action_id = 0xC
        timer = 0x10
        time_max = 0x14
        target_id = 0x18
        ground_target = 0x20
        facing = 0x30

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    request_id = direct_mem_property(ctypes.c_uint32)
    real_action_id = direct_mem_property(ctypes.c_uint32)
    action_kind = direct_mem_property(ctypes.c_int32)
    action_id = direct_mem_property(ctypes.c_int32)
    timer = direct_mem_property(ctypes.c_float)  # count up
    time_max = direct_mem_property(ctypes.c_float)
    target_id = direct_mem_property(ctypes.c_uint64)
    ground_target = glm_mem_property(glm.vec3)
    facing = direct_mem_property(ctypes.c_float)

    @property
    def remaining(self):
        return max(0, self.time_max - self.timer)


class ComboInfo:
    class offsets:
        timer = 0x0
        last_action = 0x4

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    timer = direct_mem_property(ctypes.c_float)  # count down
    last_action = direct_mem_property(ctypes.c_int32)


class ActionStack:
    class offsets:
        occupied = 0x0
        action_kind = 0x4
        action_id = 0x8
        target_id = 0x10
        type = 0x18
        type_arg = 0x1C

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    occupied = direct_mem_property(ctypes.c_int8)
    action_kind = direct_mem_property(ctypes.c_int32)
    action_id = direct_mem_property(ctypes.c_int32)
    target_id = direct_mem_property(ctypes.c_uint64)
    type = direct_mem_property(ctypes.c_int32)
    type_arg = direct_mem_property(ctypes.c_int32)

    def set(self, action_id, action_kind=ActionKind.normal, target_id=0xe0000000):
        self.action_id = action_id
        self.action_kind = action_kind
        self.target_id = target_id
        self.occupied = 1


class ActionManager:
    instance: 'ActionManager' = None

    class offsets:
        lock_timer = 0x8
        buddy_action_timer = 0x10
        pet_action_timer = 0x14
        pet_action_counter = 0x18
        cast_info = 0x20
        combo_info = 0x60
        stack = 0x80
        recast = 0x174

    def __init__(self, api: 'Api'):
        assert ActionManager.instance is None, "ActionManager already initialized"
        ActionManager.instance = self
        self.api = api
        self.handle = api.handle
        self.address, = api.scanner.find_val("48 ? ? <* * * *> 48 89 5c 24 ? 4c ? ? c6 44 24")

    lock_timer = direct_mem_property(ctypes.c_float)
    buddy_action_timer = direct_mem_property(ctypes.c_float)
    pet_action_timer = direct_mem_property(ctypes.c_float)
    pet_action_counter = direct_mem_property(ctypes.c_int32)
    cast_info = struct_mem_property(CastInfo)
    combo_info = struct_mem_property(ComboInfo)
    stack = struct_mem_property(ActionStack)
    recast = struct_mem_property(ItemArr[RecastInfo, 0x14, 80])

    _request_action = ClassFunction(scan_val("e8 <* * * *> 84 ? 74 ? 45 ? ? 89 5c 24"), 'c_int8', 'c_int32', 'c_int32', 'c_uint64', 'c_uint32', 'c_int32', 'c_int32', 'c_void_p', main_loop=True)
    _request_normal_action = ClassFunction(scan_straight("44 89 44 24 ? 89 54 24 ? 55 53 57"), 'c_int8', 'c_int32', 'c_int32', 'c_uint64', 'c_char_p', 'c_uint32', main_loop=True)
    _start_request_ground_target = ClassFunction(scan_val("e8 <* * * *> 80 7e ? ? 75 ? 48 ? ? ? ? ? ? e8"), 'c_int32', 'c_int32', 'c_int32', 'c_uint32', main_loop=True)
    get_replaced_action = ClassFunction(scan_val("e8 <* * * *> 4d ? ? 74 ? 41 ? ? ? ? 3b"), 'c_int32')
    is_action_need_replace = StaticFunction(scan_val("e8 <* * * *> 84 ? 74 ? 8b ? 48 ? ? ? ? ? ? e8 ? ? ? ? 8b ? 8b ? ? ? 8b"), 'c_int32')

    def request_action(self, action_kind, action_id, target_id=0xE0000000, arg=0, type_=0, type_arg=0):
        return self._request_action(action_kind, action_id, target_id, arg, type_, type_arg, 0)

    def request_normal_action(self, action_kind, action_id, target_id=0xE0000000, ground_target: glm.vec3 = None, arg=0):
        if ground_target is None:
            p_g = None
        else:
            p_g = ground_target.to_bytes()
        return self._request_normal_action(action_kind, action_id, target_id, p_g, arg)

    def get_recast_info_by_index(self, idx):
        if idx >= 0:
            if idx < 80:
                return self.recast[idx]
            if idx < 82:
                if (cd := self.api.framework.content_director) and (cea := cd.content_ex_action):
                    return cea.recast[idx - 80]
        return None

    def check_action(self, action_kind, action_id):
        # e8 * * * * 8b ? 85 ? 75 ? b0
        me = None
        real_action = get_real_action_id(action_kind, action_id)
        try:
            action_row = sq_pack.sheets.action_sheet[real_action]
        except KeyError as e:
            raise ValueError(f"action {real_action} not found") from e
        if action_kind == ActionKind.general:
            try:
                general_action_row = sq_pack.sheets.general_action_sheet[action_id]
            except KeyError as e:
                raise ValueError(f"general action {action_id} not found") from e
            if not UiManager.instance.is_reward_completed(general_action_row.reward):
                raise ValueError(f"general action {action_id} reward {general_action_row.reward} not completed")
        if not self.check_action_reward(action_kind, action_row.reward):
            raise ValueError(f"action {real_action} reward {action_row.reward} not completed")
        if real_action == 4:  # mount action
            if (me := me or Control.instance.control_character) is None:
                raise ValueError("control character not found")
            if (mount_id := me.mount.mount_id) != 0:  # unmount check
                try:
                    mount_row = sq_pack.sheets.mount_sheet[mount_id]
                except KeyError as e:
                    raise ValueError(f"mount {mount_id} not found") from e
                if mount_row.save_index < 0:
                    raise ValueError(f"mount {mount_id} not allow to unmout")
                if not ConditionManager.instance.check_permission(101):
                    raise ValueError(f"not allow to unmount")
        if GameMain.instance.territory_row.is_pvp_action:
            if not pvp_action_allowed(action_row):
                raise ValueError(f"action {real_action} not allowed in pvp area")
        else:
            if action_row.pvp_only:
                raise ValueError(f"action {real_action} only allowed in pvp area")

        if action_kind == ActionKind.normal and not GameMain.instance.territory_row.intended_use.enable_action:
            raise ValueError(f"normal action {real_action} not allowed in this area")
        if action_row.invalid_move:
            if not ConditionManager.instance.check_permission(1007):
                raise ValueError(f"action {real_action} not allowed scene no permission of moving")
            if not ConditionManager.instance.check_permission(1008):
                raise ValueError(f"action {real_action} not allowed scene no permission of self moving")
        # TODO ...

    def check_normal_action_reward(self, action: int | Action):
        if isinstance(action, int): action = sq_pack.sheets.action_sheet[action]
        return self.check_action_reward(ActionKind.normal, action.reward)

    def check_action_reward(self, action_kind, reward_id):
        if reward_id == 0: return True
        if (action_kind == ActionKind.normal or action_kind == ActionKind.pet) and GameMain.instance.territory_row.intended_use == 31:
            return True
        return UiManager.instance.is_reward_completed(reward_id)

    def get_recast_info_by_action(self, action_id, action_kind=ActionKind.normal):
        return self.get_recast_info_by_index(get_action_recast_index(action_kind, action_id, True))

    def start_request_ground_target(self, action_id, action_kind=ActionKind.normal):
        return self._start_request_ground_target(get_real_action_id(action_kind, action_id), action_kind, action_id, 0)

    def render_game(self):
        pass

    def render_panel(self):
        pass
