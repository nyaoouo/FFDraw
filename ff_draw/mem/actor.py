import typing
import glm
from nylib.utils.win32 import memory as ny_mem

if typing.TYPE_CHECKING:
    from . import XivMem


def is_invalid_actor_id(aid):
    return not aid or aid == 0xe0000000


class Offsets:
    name = 0x30
    id = 0x74
    e_npc_id = 0x80
    actor_type = 0x8c
    status_flag = 0x94
    pos = 0xA0
    draw_object = 0xF0
    hide_flag = 0x104
    pc_target_id = 0xC60
    b_npc_target_id = 0x1A68


class Offsets630(Offsets):
    status_flag = 0x95
    pos = 0xB0
    draw_object = 0x100
    hide_flag = 0x114
    pc_target_id = 0xC80
    b_npc_target_id = 0x1A88


class Actor:
    def __init__(self, mgr: 'ActorTable', offsets, handle, address):
        self.mgr = mgr
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

    @property
    def can_select(self):
        if ny_mem.read_byte(self.handle, self.address + self.offsets.status_flag) & 0b110 != 0b110: return False
        return ny_mem.read_uint(self.handle, self.address + self.offsets.hide_flag) >> 11 == 0

    @property
    def is_visible(self):
        p_draw_object = ny_mem.read_address(self.handle, self.address + self.offsets.draw_object)
        return ny_mem.read_byte(self.handle, p_draw_object + 0x88) & 1


class ActorTable:
    cache: dict[int, Actor]

    def __init__(self, main: 'XivMem'):
        self.main = main
        self.handle = main.handle
        self.base_address = main.scanner.find_point('4c ? ? * * * * 89 ac cb')[0]
        self.sorted_table_address = self.base_address + main.scanner.find_val('4e ? ? ? * * * * 41 ? ? ? 3b ? 73')[0]
        self.sorted_count_address = self.base_address + main.scanner.find_val('44 ? ? * * * * 45 ? ? 41 ? ? ? 48 ? ? 78')[0]
        self.me_ptr = main.scanner.find_point('48 ? ? * * * * 49 39 87')[0]
        if main.game_version >= (6, 3, 0):
            self.actor_offset = Offsets630
        else:
            self.actor_offset = Offsets

    def __getitem__(self, item):  # by sorted idx
        if item < self.sorted_length:
            return self.get_actor_by_sorted_idx(item)

    def __iter__(self):  # by sorted idx
        for i in range(self.sorted_length):
            if a := self.get_actor_by_sorted_idx(i):
                yield a

    def __len__(self):
        return self.sorted_length

    def get_actor_by_sorted_idx(self, idx):
        if a_ptr := ny_mem.read_uint64(self.handle, self.sorted_table_address + 8 * idx):
            return Actor(self, self.actor_offset, self.handle, a_ptr)

    def get_actor_by_idx(self, idx):
        if a_ptr := ny_mem.read_uint64(self.handle, self.base_address + 8 * idx):
            return Actor(self, self.actor_offset, self.handle, a_ptr)

    def iter_actor_by_type(self, actor_type: int):
        for actor in self:
            atype = actor.id >> 28
            if atype == actor_type:
                yield actor
            elif atype < actor_type:
                continue
            else:
                break

    def get_actor_by_id(self, actor_id):
        left = 0
        right = self.sorted_length - 1
        while left <= right:
            if not (a := self.get_actor_by_sorted_idx(idx := (left + right) // 2)):
                # error occurred, maybe just game update
                return
            aid = a.id
            if aid < actor_id:
                left = idx + 1
            elif aid > actor_id:
                right = idx - 1
            else:
                return a

    @property
    def sorted_length(self):
        return ny_mem.read_int(self.handle, self.sorted_count_address)

    @property
    def me(self):
        if a_ptr := ny_mem.read_uint64(self.handle, self.me_ptr):
            return Actor(self, self.actor_offset, self.handle, a_ptr)
