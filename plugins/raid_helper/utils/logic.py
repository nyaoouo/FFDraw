import math
import time
import typing

import glm
from ff_draw.main import FFDraw
from ff_draw.mem.actor import Actor
from .party_role import make as make_role_rule

if typing.TYPE_CHECKING:
    from .. import RaidHelper

main = FFDraw.instance
raid_helper: 'RaidHelper|None' = None


def is_class_job_in_category(class_job_category: int):
    class_job_map = main.sq_pack.sheets.class_job_category_sheet[class_job_category].class_job

    def func(class_job_id: int) -> bool:
        return class_job_map[class_job_id]

    func.__name__ = f'is_class_job_in_category_{class_job_category}'
    return func


is_class_job_dps = is_class_job_in_category(131)
is_class_job_tank = is_class_job_in_category(156)
is_class_job_healer = is_class_job_in_category(157)
is_class_job_range = is_class_job_in_category(87)
is_class_job_physic_dps = is_class_job_in_category(158)
is_class_job_magic_dps = is_class_job_in_category(159)


def get_me():
    return main.mem.actor_table.me


def is_me_id(id: int):
    if me := get_me():
        return id == me.id
    return False


def find_actor_by_base_id(*base_id) -> 'typing.Iterator[NActor]':
    _base_id = set(base_id)
    for a in main.mem.actor_table:
        if a.base_id in _base_id:
            yield NActor(a)


def iter_main_party(alive=True, exclude_id=None):
    if (p_list := main.mem.party.party_list).party_size:
        for member in p_list:
            if member.id != exclude_id and (not alive or member.current_hp) and (actor := main.mem.actor_table.get_actor_by_id(member.id)):
                yield NActor(actor)
    elif me := get_me():
        if exclude_id != me.id and (not alive or me.current_hp):
            yield NActor(me)


def sleep(sec):
    if sec > 0: time.sleep(sec)


def assert_status(actor: 'NActor', status_id, until_remain, source_id=0):
    time.sleep(1)
    if not (remain := actor.update().status.find_status_remain(status_id, source_id=source_id)):
        return False
    sleep(remain - until_remain)
    return actor.update().status.has_status(status_id, source_id=source_id)


# TODO fix
degree_names = {
    0: '北',
    1: '東北偏北',
    2: '東北',
    3: '東北偏東',
    4: '東',
    5: '東南偏東',
    6: '東南',
    7: '東南偏南',
    8: '南',
    9: '西南偏南',
    10: '西南',
    11: '西南偏西',
    12: '西',
    13: '西北偏西',
    14: '西北',
    15: '西北偏北',
    16: '北',
}


def degree_to_name(angle):
    return degree_names[((angle % 360 // 11.25) + 1) // 2]


def radian_to_name(rad):
    return degree_names[((rad % math.pi / 2 // (math.pi / 16)) + 1) // 2]


def get_actor_by_dis(source_actor: Actor | glm.vec3 | glm.vec2, idx, alive=True):
    it = iter_main_party(alive, source_actor.id) if isinstance(source_actor, Actor) else iter_main_party(alive)
    if isinstance(source_actor, Actor):
        source_pos = source_actor.pos.xz
    elif isinstance(source_actor, glm.vec3):
        source_pos = source_actor.xz
    else:
        source_pos = source_actor
    if actors := sorted(it, key=lambda a: glm.distance(source_pos, a.pos.xz)):
        return actors[idx % len(actors)]


way_mark_names = ['A', 'B', 'C', 'D', '1', '2', '3', '4', ]


def iter_way_mark():
    for n, wm in zip(way_mark_names, main.mem.marking.way_marks):
        if wm.is_enable:
            yield n, wm


def glm_nearest(p: glm.vec3, tg: typing.Iterable[glm.vec3]):
    return min(tg, key=lambda _p: abs(glm.distance(p, _p)))


def nearest_way_mark(p: glm.vec3):
    return min(iter_way_mark(), key=lambda wm: glm.distance(wm.pos, p))


def point_name(p: glm.vec3, offset: glm.vec3 = None):
    if offset is not None:
        p = p - offset
    try:
        return nearest_way_mark(p)
    except ValueError:
        return radian_to_name(glm.polar(p).y)


class NActor(Actor):
    def __init__(self, actor: Actor):
        super().__init__(actor.handle, actor.address)
        self.__id = actor.id
        self.__name = actor.name

    def __str__(self):
        return f'{self.__name}#{self.__id:X}'

    def update(self):
        if a := main.mem.actor_table.get_actor_by_id(self.__id):
            self.address = a.address
        else:
            raise KeyError(f'{self} is not exists')
        return self

    @classmethod
    def by_id(cls, aid):
        if a := main.mem.actor_table.get_actor_by_id(aid):
            return cls(a)
        raise KeyError(f'actor {aid:X} is not exists')


def role_idx(actor_id):
    return raid_helper.party_role.role_map.get(actor_id, 99)


def role_key(rule: list | str, actor_id):
    """
    usage: actors.sort(key=lambda a: raid_utils.role_key(rule, a.id))
    rule: 'h1tdh2', 'thd' order of role, use `make_role_rule` to precompile
    """
    if isinstance(rule, str):
        rule = make_role_rule(rule)
    idx = role_idx(actor_id)
    if idx == 99: return 99
    return rule[idx]
