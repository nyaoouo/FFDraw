import ctypes
from ffd_plus.utils import game_version
from nylib.utils import LazyClassAttr
from ff_draw.mem.utils import struct_mem_property, direct_mem_property, bit_field_property
from ffd_plus.api.game_object_manager.game_object import GameObject
from ffd_plus.api.game_object_manager.utils import ObjectType, teri_battalion_mode
from .controller import MountController
from ...utils.mem import BitFieldData, scan_val, ClassFunction


class CharacterParamFlags(BitFieldData):
    content_flag = bit_field_property(0)
    noisy = bit_field_property(1)
    important = bit_field_property(2)
    cutscene_char = bit_field_property(3)
    active = bit_field_property(4)
    in_combat = bit_field_property(5)
    using_secondary = bit_field_property(6)
    alt_style = bit_field_property(7)
    force_display = bit_field_property(8)
    level_display = bit_field_property(9)
    no_water = bit_field_property(10)
    party_member = bit_field_property(11)
    alliance_member = bit_field_property(12)
    added_as_friend = bit_field_property(13)
    received_delete = bit_field_property(14)
    near_death = bit_field_property(15)


class CharacterOffsets:
    if game_version >= (6, 5, 0):
        model_id = 0X1AC  # uint32
        skeleton_id = 0X1B0  # uint32
        real_model_id = 0X1B4  # uint32
        real_skeleton_id = 0X1B8  # uint32

        current_hp = 0X1BC  # uint32
        max_hp = 0X1C0  # uint32
        current_mp = 0X1C4  # uint32
        max_mp = 0X1C8  # uint32
        current_gp = 0X1CC  # uint16
        max_gp = 0X1CE  # uint16
        current_cp = 0X1D0  # uint16
        max_cp = 0X1D2  # uint16
        title_id = 0X1D6  # uint16
        class_job = 0X1DA  # uint8
        level = 0X1DB  # uint8

        shield_rate = 0X1E6  # uint8
        online_status = 0X1E8  # uint8
        _battalion = 0X1E9  # uint8
        param_flag = 0X1EB  # CharacterParamFlags

        move = 0X210  # MoveController
        emote = 0X630  # EmoteController
        mount = 0X670  # MountController
        companion = 0X6D8  # CompanionController
        equip = 0X6F8  # EquipController
        ornament = 0X8A0  # OrnamentComponent
        transform = 0X918  # TransformComponent
        timeline = 0X970  # TimelineComponent
        lookat = 0XCB0  # LookAtComponent
        balloon = 0X1920  # Balloon
        bubble = 0X19A0  # Bubble
        event_handlers = 0X1A28  # EventHandler*[32]
        vfx = 0X1308  # VfxData*[14]
        alpha = 0X1B28  # float[2]
        channeling = 0X1390  # Channeling[2]
        fc_tag = 0X1B40  # uint8[8]
        first_attack_id = 0X1F0  # uint64
        main_target = 0X1B58  # uint64
        name_id = 0X1B98  # uint32
        event_name_id = 0X1B9C  # uint32
        status_name_id = 0X1BA0  # uint32
        world_id = 0X1BB0  # uint16
        home_world_id = 0X1BB2  # uint16
        mode = 0X1BB6  # uint8
        event_handlers_count = 0X1BB8  # uint8
        size_ = 0X1BD0
    else:
        model_id = 0X1B4  # uint32
        skeleton_id = 0X1B8  # uint32
        real_model_id = 0X1BC  # uint32
        real_skeleton_id = 0X1C0  # uint32

        current_hp = 0X1C4  # uint32
        max_hp = 0X1C8  # uint32
        current_mp = 0X1CC  # uint32
        max_mp = 0X1D0  # uint32
        current_gp = 0X1D4  # uint16
        max_gp = 0X1D6  # uint16
        current_cp = 0X1D8  # uint16
        max_cp = 0X1DA  # uint16
        title_id = 0X1DE  # uint16
        class_job = 0X1E2  # uint8
        level = 0X1E3  # uint8

        shield_rate = 0X1ED  # uint8
        online_status = 0X1EF  # uint8
        _battalion = 0X1F0  # uint8
        param_flag = 0X1F2  # CharacterParamFlags

        move = 0X200  # MoveController
        emote = 0X620  # EmoteController
        mount = 0X660  # MountController
        companion = 0X6C8  # CompanionController
        equip = 0X6E8  # EquipController
        ornament = 0X878  # OrnamentComponent
        transform = 0X8E0  # TransformComponent
        timeline = 0X920  # TimelineComponent
        lookat = 0XC60  # LookAtComponent
        balloon = 0X17C0  # Balloon
        bubble = 0X1840  # Bubble
        event_handlers = 0X18C8  # EventHandler*[32]
        vfx = 0X19C8  # VfxData*[14]
        alpha = 0X1A48  # float[2]
        channeling = 0X1A50  # Channeling[2]
        fc_tag = 0X1A98  # uint8[8]
        first_attack_id = 0X1AB0  # uint64
        main_target = 0X1AB8  # uint64
        name_id = 0X1B00  # uint32
        event_name_id = 0X1B04  # uint32
        status_name_id = 0X1B08  # uint32
        world_id = 0X1B1C  # uint16
        home_world_id = 0X1B1E  # uint16
        mode = 0X1B26  # uint8
        event_handlers_count = 0X1B28  # uint8
        size_ = 0X1B40

    _is_validate_ = False

    @classmethod
    def validate(cls):
        if cls._is_validate_: return cls
        from ffd_plus.api import Api
        scanner = Api.instance.scanner

        # TODO: use sigs to find offsets
        # cp_o, cp_rm_o, cp_m_o = scanner.find_val("48 ? ? <? ? ? ?> e8 (* * * *:8B 41 <?> 83 ? ? 75 ? 8B 41 <?>) 8b ? e8 ? ? ? ? 48 ? ? 74 ? f6 40 ? ? 75 ? f3")
        # cls.real_model_id = cp_o + cp_rm_o
        # cls.model_id = cp_o + cp_m_o
        # cp_rs_o, cp_s_o = scanner.find_val("e8 (* * * *:8B 41 <?> 85 ? 75 ? 8B 41 <?>) 0f ? ? 81 ? ? ? ? ? 0b")
        # cls.real_skeleton_id = cp_o + cp_rs_o
        # cls.skeleton_id = cp_o + cp_s_o

        if (val := scanner.find_val(
                "0f 84 ? ? ? ? 48 ? ? 0f 84 ? ? ? ? 66 ? ? 75 ? 0f ? ? <? ? ? ?>"
        )[0]) != cls.home_world_id: raise Exception(f'Character.offsets is not validate, require {val:X} get {cls.home_world_id:X}')
        cls._is_validate_ = True
        return cls


class Character(GameObject):
    offsets = LazyClassAttr(CharacterOffsets.validate)

    model_id = direct_mem_property(ctypes.c_uint32)
    skeleton_id = direct_mem_property(ctypes.c_uint32)
    real_model_id = direct_mem_property(ctypes.c_uint32)
    real_skeleton_id = direct_mem_property(ctypes.c_uint32)
    current_hp = direct_mem_property(ctypes.c_uint32)
    max_hp = direct_mem_property(ctypes.c_uint32)
    current_mp = direct_mem_property(ctypes.c_uint32)
    max_mp = direct_mem_property(ctypes.c_uint32)
    current_gp = direct_mem_property(ctypes.c_uint16)
    max_gp = direct_mem_property(ctypes.c_uint16)
    current_cp = direct_mem_property(ctypes.c_uint16)
    max_cp = direct_mem_property(ctypes.c_uint16)
    title_id = direct_mem_property(ctypes.c_uint16)
    class_job = direct_mem_property(ctypes.c_uint8)
    level = direct_mem_property(ctypes.c_uint8)
    shield_rate = direct_mem_property(ctypes.c_uint8)
    online_status = direct_mem_property(ctypes.c_uint8)
    mount = struct_mem_property(MountController)
    _battalion = direct_mem_property(ctypes.c_uint8)
    param_flag = struct_mem_property(CharacterParamFlags)
    current_shield = property(lambda self: self.shield_rate * self.max_hp // 100)
    world_id = direct_mem_property(ctypes.c_uint16)
    home_world_id = direct_mem_property(ctypes.c_uint16)
    mode = direct_mem_property(ctypes.c_uint8)

    set_fly = ClassFunction(scan_val("e8 * * * * ba ? ? ? ? 48 89 7c 24 ? 48 ? ? ? ? ? ? 45 ? ? 45"), 'c_void_p')

    @property
    def battalion(self):
        match teri_battalion_mode():
            case 1:
                match self.type:
                    case ObjectType.Player:
                        return 0
                    case ObjectType.BattleNpc:
                        return self._battalion
            case 4 | 6:
                return self._battalion
        return 0

    is_dead = property(lambda self: self.mode == 2)

    def cast_character(self):
        return self
