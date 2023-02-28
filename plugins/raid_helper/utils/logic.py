import math
import time
import typing

import glm
from ff_draw.main import FFDraw
from ff_draw.mem.actor import Actor

main = FFDraw.instance


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
            if member.id != exclude_id and (not alive or member.current_hp) and (actor := member.actor):
                yield NActor(actor)
    elif me := get_me():
        if exclude_id != me.id and (not alive or me.current_hp):
            yield me


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


def get_actor_by_dis(source_actor: Actor, idx, alive=True):
    source_pos = source_actor.pos.xz
    if actors := sorted(iter_main_party(alive, source_actor.id), key=lambda a: glm.distance(source_pos, a.pos.xz)):
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

    def update(self):
        if a := main.mem.actor_table.get_actor_by_id(self.__id):
            self.address = a.address
        else:
            raise KeyError(f'{self.__name}#{self.__id:X} is not exists')
        return self

    @classmethod
    def by_id(cls, aid):
        return cls(main.mem.actor_table.get_actor_by_id(aid))
