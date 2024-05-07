import ctypes
import struct
import typing
import glm
from fpt4.utils.se_string import SeString
from nylib.utils.win32 import memory as ny_mem
from nylib.utils import LazyClassAttr
from .utils import direct_mem_property, WinAPIError, struct_mem_property, int8_arr

if typing.TYPE_CHECKING:
    from . import XivMem

status_struct = struct.Struct('HHfI')


def is_invalid_id(i):
    return i == 0 or i == 0xe0000000


class Channeling:
    class offsets:
        id = 0x0
        width = 0x1
        p_vfx = 0x8
        target_id = 0x10

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    id = direct_mem_property(ctypes.c_uint8)
    width = direct_mem_property(ctypes.c_uint8)
    target_id = direct_mem_property(ctypes.c_uint64)


class StatusManager:
    @LazyClassAttr
    def MAX_STATUS(self):
        from . import XivMem
        if XivMem.instance.game_version >= (6, 5, 0):
            return 60
        else:
            return 30

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    @property
    def actor(self):
        return Actor(self.handle, ny_mem.read_address(self.handle, self.address))

    # def __iter__(self):
    #     """id,param,remain,source_id"""
    #     try:
    #         for i in range(self.MAX_STATUS):
    #             yield status_struct.unpack(
    #                 ny_mem.read_bytes(self.handle, self.address + 8 + (i * status_struct.size), status_struct.size)
    #             )
    #     except WinAPIError:
    #         pass

    # load buffer once to speed up iteration
    def __iter__(self):
        yield from status_struct.iter_unpack(ny_mem.read_bytes(self.handle, self.address + 8, status_struct.size * self.MAX_STATUS))

    def _iter_filter(self, status_id: int, source_id=0):
        for status_id_, param, remain, source_id_ in self:
            if status_id == status_id_ and (not source_id or source_id_ == source_id):
                yield status_id_, param, remain, source_id_

    def __contains__(self, item):
        if isinstance(item, int):
            return self.has_status(item)
        elif isinstance(item, tuple):
            return self.has_status(*item)
        return False

    def has_status(self, status_id: int, source_id=0):
        for _ in self._iter_filter(status_id, source_id):
            return True
        return False

    def find_status_remain(self, status_id: int, source_id=0):
        for status_id_, param, remain, source_id_ in self._iter_filter(status_id, source_id):
            return remain
        return 0

    def find_status_param(self, status_id: int, source_id=0):
        for status_id_, param, remain, source_id_ in self._iter_filter(status_id, source_id):
            return param
        return 0

    def find_status_source(self, status_id: int):
        for status_id_, param, remain, source_id_ in self._iter_filter(status_id):
            return source_id_
        return 0


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

    @property
    def cast_location(self):
        return glm.vec3.from_bytes(bytes(ny_mem.read_bytes(self.handle, self.address + self.offsets.cast_location, 0xc)))

    current_cast_time = direct_mem_property(ctypes.c_float)
    total_cast_time = direct_mem_property(ctypes.c_float)
    used_action_id = direct_mem_property(ctypes.c_uint32)
    used_action_type = direct_mem_property(ctypes.c_uint16)


class ActorOffsets640:
    name = 0x30
    id = 0x74
    base_id = 0x80
    owner_id = 0x84
    actor_type = 0x8C
    status_flag = 0x95
    pos = 0xB0
    facing = 0xC0
    radius = 0xD0
    draw_object = 0x100
    hide_flag = 0x114
    current_hp = 0x1C4
    max_hp = 0x1C8
    current_mp = 0x1CC
    max_mp = 0x1D0
    current_gp = 0x1D4
    max_gp = 0x1D6
    current_cp = 0x1D8
    max_cp = 0x1DA
    class_job = 0x1E2
    level = 0x1E3
    model_attr = 0x1E6
    mount_id = 0x678
    pc_target_id = 0xCB0
    channeling = 0x1A50
    b_npc_target_id = 0x1AB8
    current_world = 0x1B1C
    home_world = 0x1B1E
    shield = 0x1ED
    status = 0x1B80
    cast_info = 0x1D10
    name_id = 0x1B00
    online_status = 0x1E8


class ActorOffsets650:
    name = 0x30
    id = 0x74
    base_id = 0x80
    owner_id = 0x84
    actor_type = 0x8C
    status_flag = 0x95
    pos = 0xB0
    facing = 0xC0
    radius = 0xD0
    draw_object = 0x100
    hide_flag = 0x114
    current_hp = 0x1BC
    max_hp = 0x1C0
    current_mp = 0x1C4
    max_mp = 0x1C8
    current_gp = 0x1CC
    max_gp = 0x1CE
    current_cp = 0x1D0
    max_cp = 0x1D2
    class_job = 0x1DA
    level = 0x1DB
    model_attr = 0x1DE
    timeline_model_skin = 0xc30
    timeline_model_flag = 0xc31
    mount_id = 0x688
    pc_target_id = 0xD00
    channeling = 0x1390
    b_npc_target_id = 0x1B58
    current_world = 0x1BB0
    home_world = 0x1BB2
    shield = 0x1E6
    status = 0x1C10
    cast_info = 0x1F00
    name_id = 0x1B98
    online_status = 0x1E8

class Actor:
    offsets = ActorOffsets640

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    @property
    def name(self):
        data = ny_mem.read_bytes(self.handle, self.address + self.offsets.name, 68)
        try:
            data = data[:data.index(0)]
        except ValueError:
            pass
        if 2 in data:
            return str(SeString.from_buffer(bytearray(data)))
        return data.decode('utf-8', 'ignore')

    id = direct_mem_property(ctypes.c_uint)
    base_id = direct_mem_property(ctypes.c_uint)
    owner_id = direct_mem_property(ctypes.c_uint)

    @property
    def pos(self):
        return glm.vec3.from_bytes(bytes(ny_mem.read_bytes(self.handle, self.address + self.offsets.pos, 0xc)))

    facing = direct_mem_property(ctypes.c_float)
    radius = direct_mem_property(ctypes.c_float)
    actor_type = direct_mem_property(ctypes.c_byte)
    current_hp = direct_mem_property(ctypes.c_uint)
    max_hp = direct_mem_property(ctypes.c_uint)
    current_mp = direct_mem_property(ctypes.c_uint)
    max_mp = direct_mem_property(ctypes.c_uint)
    current_gp = direct_mem_property(ctypes.c_uint)
    max_gp = direct_mem_property(ctypes.c_uint)
    current_cp = direct_mem_property(ctypes.c_uint)
    max_cp = direct_mem_property(ctypes.c_uint)
    class_job = direct_mem_property(ctypes.c_byte)
    level = direct_mem_property(ctypes.c_byte)
    model_attr = direct_mem_property(ctypes.c_byte)
    timeline_model_skin = direct_mem_property(ctypes.c_byte)
    timeline_model_flag = struct_mem_property(int8_arr[2])
    mount_id = direct_mem_property(ctypes.c_ushort)
    current_world = direct_mem_property(ctypes.c_ushort)
    home_world = direct_mem_property(ctypes.c_ushort)
    shield = direct_mem_property(ctypes.c_ubyte)
    online_status = direct_mem_property(ctypes.c_uint)
    def target_radian(self, target: 'Actor'):
        return glm.polar(target.pos - self.pos).y

    def target_distance(self, target: 'Actor'):
        return glm.distance(self.pos, target.pos)

    def get_channeling(self, idx):
        if (c := Channeling(self.handle, self.address + self.offsets.channeling + idx * 0x18)).id:
            return c

    @property
    def target_id(self):
        try:
            return ny_mem.read_uint(self.handle, self.address + (
                self.offsets.pc_target_id if self.actor_type == 1 else self.offsets.b_npc_target_id
            ))
        except WinAPIError:
            return 0

    @property
    def can_select(self):
        try:
            if ny_mem.read_byte(self.handle, self.address + self.offsets.status_flag) & 0b110 != 0b110: return False
            return ny_mem.read_uint(self.handle, self.address + self.offsets.hide_flag) >> 11 == 0
        except WinAPIError:
            return False

    @property
    def is_visible(self):
        try:
            p_draw_object = ny_mem.read_address(self.handle, self.address + self.offsets.draw_object)
            return ny_mem.read_byte(self.handle, p_draw_object + 0x88) & 1 > 0
        except WinAPIError:
            return False

    status = struct_mem_property(StatusManager)
    cast_info = struct_mem_property(CastInfo)
    name_id = direct_mem_property(ctypes.c_uint32)


class ActorTable:
    cache: dict[int, Actor]

    def __init__(self, main: 'XivMem'):
        self.main = main
        self.handle = main.handle
        self.base_address = main.scanner.find_point('4c ? ? * * * * 89 ac cb')[0]
        self.sorted_table_address = self.base_address + main.scanner.find_val('4e ? ? ? * * * * 41 ? ? ? 3b ? 73 ? 44')[0]
        self.sorted_count_address = self.base_address + main.scanner.find_val('44 ? ? * * * * 45 ? ? 41 ? ? ? 48 ? ? 78')[0]
        self.me_ptr = main.scanner.find_point('48 ? ? * * * * 49 39 87')[0]

        if main.game_version >= (6, 5, 0):
            Actor.offsets = ActorOffsets650
        else:
            Actor.offsets = ActorOffsets640

        self.table_size = main.scanner.find_val('81 bf ? ? ? ? * * * * 72 ? 44 89 b7')[0]
        self.use_brute_search = False

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
            return Actor(self.handle, a_ptr)

    def get_actor_by_idx(self, idx):
        if a_ptr := ny_mem.read_uint64(self.handle, self.base_address + 8 * idx):
            return Actor(self.handle, a_ptr)

    def iter_actor_by_type(self, actor_type: int):
        for actor in self:
            atype = actor.id >> 28
            if atype == actor_type:
                yield actor
            elif atype < actor_type:
                continue
            else:
                break

    def _get_actor_by_id_brute(self, actor_id):
        for i in range(self.table_size):
            if (a := self.get_actor_by_idx(i)) and a.id == actor_id:
                return a

    def _get_actor_by_id_bisect(self, actor_id):
        if is_invalid_id(actor_id):
            return None
        left = 0
        right = self.sorted_length - 1
        while left <= right:
            if not (a := self.get_actor_by_sorted_idx(idx := (left + right) // 2)):
                # error occurred, maybe just game update
                return
            aid = a.id
            if not aid:
                continue
            elif aid < actor_id:
                left = idx + 1
            elif aid > actor_id:
                right = idx - 1
            else:
                return a

    def get_actor_by_id(self, actor_id) -> Actor | None:
        return (self._get_actor_by_id_brute if self.use_brute_search else self._get_actor_by_id_bisect)(actor_id)

    @property
    def sorted_length(self):
        return ny_mem.read_int(self.handle, self.sorted_count_address)

    @property
    def me(self):
        if a_ptr := ny_mem.read_uint64(self.handle, self.me_ptr):
            return Actor(self.handle, a_ptr)


class Targets:
    def __init__(self, main: 'XivMem'):
        self.main = main
        self.handle = main.handle
        self.address, = self.main.scanner.find_point("48 8B 05 * * * * 48 8D 0D ? ? ? ? FF 50 ? 48 85 DB")

    @property
    def current(self):
        if actor_ptr := ny_mem.read_ulonglong(self.handle, self.address + 0x80):
            return Actor(self.handle, actor_ptr)

    @current.setter
    def current(self, actor: Actor):
        ny_mem.write_ulonglong(self.handle, self.address + 0x80, actor.address)

    @property
    def mouse_over(self):
        if actor_ptr := ny_mem.read_ulonglong(self.handle, self.address + 0xD0):
            return Actor(self.handle, actor_ptr)

    @mouse_over.setter
    def mouse_over(self, actor: Actor):
        ny_mem.write_ulonglong(self.handle, self.address + 0xD0, actor.address)

    @property
    def focus(self):
        if actor_ptr := ny_mem.read_ulonglong(self.handle, self.address + 0xF8):
            return Actor(self.handle, actor_ptr)

    @focus.setter
    def focus(self, actor: Actor):
        ny_mem.write_ulonglong(self.handle, self.address + 0xF8, actor.address)
