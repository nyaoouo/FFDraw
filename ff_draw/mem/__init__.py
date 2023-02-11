import os
import sys
import typing

import glm
from win32con import PROCESS_ALL_ACCESS

from nylib.utils.win32 import memory as ny_mem, process as ny_proc, winapi as ny_winapi
from nylib.pefile import PE
from nylib.pattern import StaticPatternSearcher
from . import utils


def is_invalid_actor_id(aid):
    return not aid or aid == 0xe0000000


class Offsets:
    name = 0x30
    id = 0x74
    e_npc_id = 0x80
    actor_type = 0x8c
    pos = 0xA0
    pc_target_id = 0xC60
    b_npc_target_id = 0x1A68


class Offsets630(Offsets):
    pos = 0xB0
    pc_target_id = 0xC80
    b_npc_target_id = 0x1A88


class Actor:
    def __init__(self, offsets, handle, address):
        self.offsets = offsets
        self.handle = handle
        self.address = address

    @property
    def name(self):
        return ny_mem.read_string(self.handle, self.address + self.offsets.name, 68)

    @property
    def id(self):
        return ny_mem.read_uint(self.handle, self.address + self.offsets.id)

    @property
    def e_npc_id(self):
        return ny_mem.read_uint(self.handle, self.address + self.offsets.e_npc_id)

    @property
    def pos(self):
        return glm.vec3.from_bytes(bytes(ny_mem.read_bytes(self.handle, self.address + self.offsets.pos, 0xc)))

    @property
    def facing(self):
        return ny_mem.read_float(self.handle, self.address + self.offsets.pos + 0x10)

    @property
    def actor_type(self):
        return ny_mem.read_byte(self.handle, self.address + self.offsets.actor_type)

    @property
    def pc_target_id(self):
        return ny_mem.read_uint(self.handle, self.address + self.offsets.pc_target_id)

    @property
    def b_npc_target_id(self):
        return ny_mem.read_uint(self.handle, self.address + self.offsets.b_npc_target_id)

    @property
    def target_id(self):
        return self.pc_target_id if self.actor_type == 1 else self.b_npc_target_id


class ActorTable:
    max_size = 424
    _cache: dict[int, Actor]

    def __init__(self, handle, address, actor_offset):
        self.handle = handle
        self.address = address
        self.actor_offset = actor_offset
        self._cache = {}

    def _set_actor_cache(self, actor: Actor):
        aid = actor.id
        if is_invalid_actor_id(aid):
            self._cache[aid] = actor

    def __getitem__(self, item):
        assert item < self.max_size
        if a_ptr := ny_mem.read_uint64(self.handle, self.address + 8 * item):
            actor = Actor(self.actor_offset, self.handle, a_ptr)
            if not is_invalid_actor_id(aid := actor.id): self._cache[aid] = actor
            return actor

    def __iter__(self):
        for i in range(self.max_size):
            if actor := self[i]:
                yield actor

    def get_actor_by_id(self, actor_id):
        if is_invalid_actor_id(actor_id):
            return None
        if (actor := self._cache.get(actor_id)) and actor.id == actor_id:
            return actor
        self._cache.pop(actor_id, None)
        for actor in self:
            if actor.id == actor_id:
                return actor

    @property
    def me(self):
        return self[0]


class XivMem:
    def __init__(self, pid: int):
        self.pid = pid
        self.handle = ny_winapi.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        self.base_module = ny_proc.get_base_module(self.handle)
        file_name = self.base_module.filename.decode(os.environ['PathEncoding'])
        self.scanner = StaticPatternSearcher(PE(file_name, fast_load=True), self.base_module.lpBaseOfDll)
        self.hwnd = utils.get_hwnd(self.pid)
        self.game_version, self.game_build_date = utils.get_game_version_info(file_name)
        self.screen_address = self.scanner.find_point('48 ? ? * * * * e8 ? ? ? ? 42 ? ? ? 39 05')[0] + 0x1b4
        self.actor_table = ActorTable(self.handle, self.scanner.find_point('4c ? ? * * * * 89 ac cb')[0], Offsets630 if self.game_version >= (6, 3, 0) else Offsets)

    def load_screen(self):
        buf = ny_mem.read_bytes(self.handle, self.screen_address, 0x48)
        return glm.mat4.from_bytes(bytes(buf[:0x40])), glm.vec2.from_bytes(bytes(buf[0x40:]))
