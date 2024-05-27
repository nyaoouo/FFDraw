import ctypes

import glm

from ff_draw.mem.utils import direct_mem_property, struct_mem_property, glm_mem_property
from ffd_plus.api.utils.commons.game import StatusManager
from ffd_plus.utils import game_version
from nylib.utils import LazyClassAttr
from . import Character


class CastInfo:
    class offsets:
        is_casting = 0x0
        interruptible = 0x1
        action_type = 0x2
        action_id = 0x4
        cast_target_id = 0x10
        cast_location = 0x20
        current_cast_time = 0x34
        total_cast_time = 0x38
        used_action_id = 0x40
        used_action_type = 0x44

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    is_casting = direct_mem_property(ctypes.c_uint8)
    interruptible = direct_mem_property(ctypes.c_uint8)
    action_type = direct_mem_property(ctypes.c_uint16)
    action_id = direct_mem_property(ctypes.c_uint32)
    cast_target_id = direct_mem_property(ctypes.c_uint32)
    cast_location = glm_mem_property(glm.vec3)
    current_cast_time = direct_mem_property(ctypes.c_float)
    total_cast_time = direct_mem_property(ctypes.c_float)
    used_action_id = direct_mem_property(ctypes.c_uint32)
    used_action_type = direct_mem_property(ctypes.c_uint16)


class BattleCharaOffsets:
    if game_version >= (6, 5, 0):
        status = 0x1C10
        cast_info = 0x1F00
        content_data = 0x2F70
    else:
        status = 0x1B80
        cast_info = 0x1D10
        content_data = 0x2D80

    _is_validate_ = False

    @classmethod
    def validate(cls):
        if cls._is_validate_: return cls
        from ffd_plus.api import Api
        scanner = Api.instance.scanner
        if (val := scanner.find_val(
                "48 89 81 ? ? ? ? 48 ? ? <? ? ? ?> e8 ? ? ? ? 48 ? ? ? ? ? ? e8 ? ? ? ? "
                "48 ? ? ? ? ? ? ba ? ? ? ? 41 ? ? ? ? ? e8 ? ? ? ? 48 ? ? 48 c7 87"
        )[0]) != cls.content_data: raise Exception(f'BattleChara.offsets is not validate, require {val:X} get {cls.content_data:X}')
        cls._is_validate_ = True
        return cls


class BattleChara(Character):
    offsets = LazyClassAttr(BattleCharaOffsets.validate)

    status = struct_mem_property(StatusManager)
    cast_info = struct_mem_property(CastInfo)
