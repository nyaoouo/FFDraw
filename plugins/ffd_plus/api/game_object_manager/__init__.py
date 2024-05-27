import typing
import ctypes

from nylib.utils import LRU
from nylib.utils.imgui import ctx as imgui_ctx
from ff_draw.mem.utils import struct_mem_property, direct_mem_property
from ffd_plus.api.utils.commons import ItemArr, Pointer
from ffd_plus.api.utils.commons.game import is_entity_id_valid
from .game_object import GameObject
from .character import Character
from .character.battle_chara import BattleChara

if typing.TYPE_CHECKING:
    from .. import Api


class GameObjectManagerOffsets:
    update_priority_index = 0x0
    update_draw = 0x4
    stop_drawing = 0x8
    draw_limit = 0xc
    ground_index = 0x10

    def __init__(self, mgr: 'GameObjectManager'):
        scanner = mgr.api.scanner
        self.game_objects_max_size, = scanner.find_val("81 bf ? ? ? ? <? ? ? ?> 72 ? 44 89 b7")
        self.game_objects = ((self.ground_index + 2) + 7) & ~7
        self.game_objects_common_id_sorted = self.game_objects + self.game_objects_max_size * 8
        self.game_objects_entity_id_sorted = self.game_objects_common_id_sorted + self.game_objects_max_size * 8
        self.common_id_sorted_size = self.game_objects_entity_id_sorted + self.game_objects_max_size * 8
        self.entity_id_sorted_size = self.common_id_sorted_size + 4


class GameObjectManager:
    instance: 'GameObjectManager' = None
    offsets: 'GameObjectManagerOffsets' = None

    def __init__(self, api: 'Api'):
        assert GameObjectManager.instance is None, "GameObjectManager already initialized"
        GameObjectManager.instance = self
        self.api = api
        self.handle = api.handle
        self.address, = api.scanner.find_val("48 ? ? * * * * 80 63 ? ? e8")

        if GameObjectManager.offsets is None:
            GameObjectManager.offsets = GameObjectManagerOffsets(self)

        GameObject.offsets, Character.offsets, BattleChara.offsets  # touch offsets to validate them

        self.object_by_entity_id = LRU(_maxsize=self.game_objects_max_size, _getter=self.get_object_by_entity_id, _validate=lambda id_, e: e.entity_id == id_ if e else False)
        self.object_by_common_id = LRU(_maxsize=self.game_objects_max_size, _getter=self.get_object_by_common_id, _validate=lambda id_, e: e.common_id == id_ if e else False)

    update_priority_index = direct_mem_property(ctypes.c_uint32)
    update_draw = direct_mem_property(ctypes.c_int8)
    stop_drawing = direct_mem_property(ctypes.c_uint32)
    draw_limit = direct_mem_property(ctypes.c_uint32)
    ground_index = direct_mem_property(ctypes.c_uint16)
    game_objects = struct_mem_property(ItemArr[Pointer[GameObject], 8])
    game_objects_common_id_sorted = struct_mem_property(ItemArr[Pointer[GameObject], 8])
    game_objects_entity_id_sorted = struct_mem_property(ItemArr[Pointer[GameObject], 8])
    game_objects_max_size = property(lambda self: self.offsets.game_objects_max_size)
    common_id_sorted_size = direct_mem_property(ctypes.c_uint32)
    entity_id_sorted_size = direct_mem_property(ctypes.c_uint32)

    def get_object_by_entity_id(self, entity_id: int):
        if not is_entity_id_valid(entity_id): return None
        left = 0
        right = self.entity_id_sorted_size - 1
        tbl = self.game_objects_entity_id_sorted
        while left <= right:
            if not (o := tbl[idx := (left + right) // 2].content):
                # error occurred, maybe just game update
                return
            e_id = o.entity_id
            if not is_entity_id_valid(e_id):
                continue
            elif e_id < entity_id:
                left = idx + 1
            elif e_id > entity_id:
                right = idx - 1
            else:
                return o

    def get_object_by_common_id(self, common_id):
        if not common_id: return None
        left = 0
        right = self.common_id_sorted_size - 1
        tbl = self.game_objects_common_id_sorted
        while left <= right:
            if not (o := tbl[idx := (left + right) // 2].content):
                # error occurred, maybe just game update
                return
            c_id = o.common_id
            if not c_id:
                continue
            elif c_id < common_id:
                left = idx + 1
            elif c_id > common_id:
                right = idx - 1
            else:
                return o

    def render_panel(self):
        pass

    def render_game(self):
        pass
