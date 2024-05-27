import enum
import typing

from ffd_plus.api.utils import sq_pack

if typing.TYPE_CHECKING:
    from ffd_plus.api.game_object_manager.game_object import GameObject


class ObjectType(enum.IntEnum):
    Null = 0
    Player = 1
    BattleNpc = 2
    EventNpc = 3
    Treasure = 4
    Aetheryte = 5
    Gathering = 6
    EventObj = 7
    Mount = 8
    Companion = 9
    Retainer = 10
    Area = 11
    Cutscene = 12
    Ornament = 14


class ObjectCategory(enum.IntEnum):
    Normal = 0
    Parts = 1
    Pet = 2
    Buddy = 3
    Player = 4
    BattleNpc = 5


def teri_battalion_mode():
    from ffd_plus.api.game_main import GameMain
    if t_row := GameMain.instance.territory_row:
        return t_row.battalion_mode
    return 0


def is_enemy(obj_a: 'GameObject', obj_b: 'GameObject'):
    if not obj_a or not obj_b: return False
    if not (c_a := obj_a.cast_character()) or c_a.type not in (ObjectType.Player, ObjectType.BattleNpc): return False
    if not (c_b := obj_b.cast_character()) or c_b.type not in (ObjectType.Player, ObjectType.BattleNpc): return False
    if not teri_battalion_mode(): return False
    return sq_pack.sheets.battalion_sheet[c_a.battalion].table[c_b.battalion] == 1


def is_enemy_by_base_id(obj: 'GameObject', base_id: int):
    if not (c := obj.cast_character()) or c.type not in (ObjectType.Player, ObjectType.BattleNpc): return False
    if not teri_battalion_mode(): return False
    try:
        battalion_t = sq_pack.sheets.b_npc_base_sheet[base_id].battalion
    except KeyError:
        return False
    return sq_pack.sheets.battalion_sheet[c.battalion].table[battalion_t] == 1
