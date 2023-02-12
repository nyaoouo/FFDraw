import typing
import glm
from nylib.utils.win32 import memory as ny_mem

if typing.TYPE_CHECKING:
    from . import XivMem


class MemberOffset:
    id = 0x1a8


class Member:
    def __init__(self, party: 'Party', address):
        self.party = party
        self.handle = party.handle
        self.address = address
        self.offsets = MemberOffset

    @property
    def id(self):
        return ny_mem.read_uint(self.handle, self.address + self.offsets.id)


class PartyOffset:
    members = 0
    party_size = 0x3d5c


class Party:
    def __init__(self, mgr: 'PartyManager', address):
        self.mgr = mgr
        self.handle = mgr.main.handle
        self.address = address
        self.offsets = PartyOffset
        self.members = [Member(self, self.address + self.offsets.members + i * 0x230) for i in range(28)]

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
        self.real_party = Party(self, real_party_address)
        self.replay_party = Party(self, replay_party_address)

    @property
    def party_list(self):
        return self.replay_party if self.main.is_in_replay else self.real_party
