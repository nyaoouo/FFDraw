import ctypes
import typing

import glm

from nylib.utils import LazyClassAttr
from ff_draw.mem.utils import struct_mem_property, bit_field_property, direct_mem_property, glm_mem_property
from ffd_plus.api.utils.commons import CharArr
from ffd_plus.api.utils.mem import BitFieldData, ClassFunction, scan_val, scan_straight
from ffd_plus.api.utils.commons.game import is_entity_id_valid
from ffd_plus.utils import game_version
from .utils import ObjectType, is_enemy, ObjectCategory

if typing.TYPE_CHECKING:
    from .character import Character
    from .character.battle_chara import BattleChara
    from .character.companion_chara import CompanionChara
    from .character.ornament_chara import OrnamentChara


class GameObjectInvisibleFlag(BitFieldData):
    owner = bit_field_property(0)
    party = bit_field_property(1)
    others = bit_field_property(2)
    all = bit_field_property(0, 3)


class GameObjectFlags(BitFieldData):
    if game_version >= (6, 5, 0):
        can_select_default = bit_field_property(0)
        can_select = bit_field_property(1)
        is_target_with_radius = bit_field_property(2)
        loaded = bit_field_property(3)
        event_loaded = bit_field_property(4)
        model_loaded = bit_field_property(5)
        data_loaded = bit_field_property(6)
        model_created = bit_field_property(7)
        name_loaded = bit_field_property(8)
    else:
        can_select_default = bit_field_property(0)
        can_select = bit_field_property(1)
        loaded = bit_field_property(2)
        event_loaded = bit_field_property(3)
        model_loaded = bit_field_property(4)
        data_loaded = bit_field_property(5)
        model_created = bit_field_property(6)
        name_loaded = bit_field_property(7)


class GameObjectOffsets:
    name = 0x30  # char[64]
    invisible_flag = 0x70  # GameObjectInvisibleFlag
    entity_id = 0x74  # uint32
    layout_id = 0x78  # uint32
    bind_id = 0x7C  # uint32
    base_id = 0x80  # uint32
    owner_id = 0x84  # uint32
    index = 0x88  # uint16
    owner_index = 0x8A  # uint16
    type = 0x8C  # uint8
    category = 0x8D  # uint8
    sex = 0x8E  # uint8
    priority = 0x8F  # uint8
    distance = 0x90  # uint8
    invisible_group = 0x93  # uint8
    flags = 0x95  # GameObjectFlags
    pos = 0xB0  # vec3
    facing = 0xC0  # float
    scale = 0xC4  # float
    vfx_scale = 0xC8  # float
    radius = 0xD0  # float
    draw_object_offset = 0xE0  # vec3
    draw_object_facing = 0xF0  # float
    content_id = 0xF4  # uint32
    fate_id = 0xF8  # uint32
    draw_object = 0x100  # DrawObject*
    shared_group = 0x108  # SharedGroup*
    icon_id = 0x110  # uint32
    hide_flag = 0x114  # uint32
    name_pos = 0x120  # vec3
    camera_look_at = 0x130  # vec3
    target_pos = 0x140  # vec3
    map_icon_id = 0x150  # uint32
    lua_game_object = 0x158  # LuaGameObject*
    event_handler = 0x160  # EventHandler*

    _is_validate_ = False

    @classmethod
    def validate(cls):
        if cls._is_validate_: return cls
        from ffd_plus.api import Api
        if game_version >= (6, 5, 0):
            if Api.instance.scanner.find_val(  # flags
                    "74 (*:0C <?> 88 81 <? ? ? ?>) a8 ? 75 ? f3"
            ) != [4, cls.flags + 3]: raise Exception('GameObject.offsets is not validate')
        else:
            if Api.instance.scanner.find_val(  # flags
                    "74 (*:0C <?> 88 81 <? ? ? ?>) a8 ? 75 ? f3"
            ) != [2, cls.flags + 3]: raise Exception('GameObject.offsets is not validate')
        if Api.instance.scanner.find_val(  # event_handler
                "4c 39 b7 <? ? ? ?> 75 ? 48 89 b7 ? ? ? ? eb"
        )[0] != 0x160: raise Exception('GameObject.offsets is not validate')
        cls._is_validate_ = True
        return cls


def get_control():
    from ffd_plus.api.control import Control
    return Control.instance


class GameObject:
    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    offsets = LazyClassAttr(GameObjectOffsets.validate)

    name = struct_mem_property(CharArr[64])
    visible_flag = struct_mem_property(GameObjectInvisibleFlag)
    entity_id = direct_mem_property(ctypes.c_uint32)
    layout_id = direct_mem_property(ctypes.c_uint32)
    bind_id = direct_mem_property(ctypes.c_uint32)
    base_id = direct_mem_property(ctypes.c_uint32)
    owner_id = direct_mem_property(ctypes.c_uint32)
    index = direct_mem_property(ctypes.c_uint16)
    owner_index = direct_mem_property(ctypes.c_uint16)
    type = direct_mem_property(ctypes.c_uint8)
    category = direct_mem_property(ctypes.c_uint8)
    sex = direct_mem_property(ctypes.c_uint8)
    priority = direct_mem_property(ctypes.c_uint8)
    distance = direct_mem_property(ctypes.c_uint8)
    invisible_group = direct_mem_property(ctypes.c_uint8)
    flags = struct_mem_property(GameObjectFlags)
    pos = glm_mem_property(glm.vec3)
    facing = direct_mem_property(ctypes.c_float)
    scale = direct_mem_property(ctypes.c_float)
    vfx_scale = direct_mem_property(ctypes.c_float)
    radius = direct_mem_property(ctypes.c_float)
    draw_object_offset = glm_mem_property(glm.vec3)
    draw_object_facing = direct_mem_property(ctypes.c_float)
    content_id = direct_mem_property(ctypes.c_uint32)
    fate_id = direct_mem_property(ctypes.c_uint32)
    # draw_object = direct_mem_property(ctypes.c_uint64)
    # shared_group = direct_mem_property(ctypes.c_uint64)
    icon_id = direct_mem_property(ctypes.c_uint32)
    hide_flag = direct_mem_property(ctypes.c_uint32)
    name_pos = glm_mem_property(glm.vec3)
    camera_look_at = glm_mem_property(glm.vec3)
    target_pos = glm_mem_property(glm.vec3)
    map_icon_id = direct_mem_property(ctypes.c_uint32)

    # lua_game_object = direct_mem_property(ctypes.c_uint64)
    # event_handler = direct_mem_property(ctypes.c_uint64)

    @property
    def common_id(self):
        if is_entity_id_valid(res := self.entity_id): return res
        if (res := self.layout_id) == 0 or (200 <= self.index <= 248): return self.index | 0x200000000
        return res | 0x100000000

    battalion = property(lambda self: 0)

    @property
    def is_selectable(self):
        flags = self.flags
        if not flags.can_select: return False
        if not flags.loaded: return False
        hide_flag = self.hide_flag
        if hide_flag & 0x800 != 0 and flags.model_loaded: return False
        # if hide_flag & 0xFFFFE7F7 != 0: return False # ?
        return True

    is_control = property(lambda self: get_control().control_character_id == self.entity_id)
    is_pet = property(lambda self: self.type == ObjectType.BattleNpc and self.category == ObjectCategory.Pet)
    is_buddy = property(lambda self: self.type == ObjectType.BattleNpc and self.category == ObjectCategory.Buddy)
    is_npc_ally = property(lambda self: self.type == ObjectType.BattleNpc and ((cate := self.category) == ObjectCategory.Pet or cate == ObjectCategory.Buddy or cate == 9))
    is_enemy = property(lambda self: is_enemy(self, get_control().control_character))
    is_friend = property(lambda self: not self.is_enemy)
    is_party_member = property(lambda self: bool((chara := self.cast_character()) and chara.param_flag.party_member))
    is_dead = property(lambda self: False)

    _update_draw_pos = ClassFunction(scan_val("e8 * * * * 48 ? ? ? 66 89 b8"), 'c_void_p', main_loop=True)
    _update_draw_facing = ClassFunction(scan_val("e8 * * * * 48 ? ? ? 45 ? ? 80 4f"), 'c_void_p', main_loop=True)
    _update_draw_scale = ClassFunction(scan_val("e8 * * * * 8b ? 45 ? ? 44 ? ? ? ? 25"), 'c_void_p', main_loop=True)

    def is_character(self):
        return self.index < 200

    def is_sub_character(self):
        match (t := self.type):
            case ObjectType.Mount | ObjectType.Companion | ObjectType.Ornament:
                return t

    def cast_character(self) -> 'Character|BattleChara|CompanionChara|OrnamentChara|None':
        if not self.is_character(): return None
        match self.is_sub_character():
            case None:
                from .character.battle_chara import BattleChara
                self.__type__ = BattleChara
            case ObjectType.Companion:
                from .character.companion_chara import CompanionChara
                self.__type__ = CompanionChara
            case ObjectType.Ornament:
                from .character.ornament_chara import OrnamentChara
                self.__type__ = OrnamentChara
            case _:
                from .character import Character
                self.__type__ = Character
        return self

    def cast_battle_chara(self) -> 'BattleChara|None':
        if self.is_character() and self.is_sub_character() is None:
            from .character.battle_chara import BattleChara
            self.__type__ = BattleChara
            return self

    def __str__(self):
        return f'GameObject({self.common_id:X}:{self.name.se_string})'
