import ctypes
import typing
import glm
from nylib.utils.win32 import memory as ny_mem
from .actor import StatusManager
from .utils import direct_mem_property

if typing.TYPE_CHECKING:
    from . import XivMem


class MemberOffset:
    status = 0x0
    pos = 0x190
    character_id = 0x1a0
    id = 0x1a8
    current_hp = 0x1b4
    max_hp = 0x1b8
    current_mp = 0x1bc
    max_mp = 0x1be
    class_job = 0x205
    level = 0x206
    shield = 0x207


class Member:
    offsets = MemberOffset

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    id = direct_mem_property(ctypes.c_uint)
    character_id = direct_mem_property(ctypes.c_uint64)
    current_hp = direct_mem_property(ctypes.c_uint)
    max_hp = direct_mem_property(ctypes.c_uint)
    current_mp = direct_mem_property(ctypes.c_uint)
    class_job = direct_mem_property(ctypes.c_byte)
    level = direct_mem_property(ctypes.c_byte)
    shield = direct_mem_property(ctypes.c_ubyte)

    @property
    def pos(self):
        return glm.vec3.from_bytes(bytes(ny_mem.read_bytes(self.handle, self.address + self.offsets.pos, 0xc)))

    @property
    def status(self):
        return StatusManager(self.handle, self.address + self.offsets.status)

    # @property # has bug, status manager in party is not the same as actor
    # def actor(self):
    #     return self.status.actor


class PartyOffset:
    members = 0
    party_size = 0x3d5c


class Party:
    offsets = PartyOffset

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address
        self.members = [Member(self.handle, self.address + self.offsets.members + i * 0x230) for i in range(28)]

    def __iter__(self):
        for i in range(self.party_size):
            yield self.members[i]

    @property
    def party_size(self):
        return ny_mem.read_byte(self.handle, self.address + self.offsets.party_size)


class PartyManager:
    def __init__(self, main: 'XivMem'):
        self.main = main
        real_party_address = main.scanner.find_point('48 ? ? * * * * 48 89 74 24 ? b2')[0]
        replay_party_address = real_party_address + main.scanner.find_val('74 ? f6 05 ? ? ? ? ? 48 ? ? * * * * 75')[0]
        self.real_party = Party(self.main.handle, real_party_address)
        self.replay_party = Party(self.main.handle, replay_party_address)

    @property
    def party_list(self):
        return self.replay_party if self.main.is_in_replay else self.real_party
