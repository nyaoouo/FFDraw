import typing
import glm
from nylib.utils.win32 import memory as ny_mem

if typing.TYPE_CHECKING:
    from . import XivMem


class Party:
    def __init__(self, main: 'XivMem'):
        self.main = main
        self.handle = main.handle
        self.real_party_address = main.scanner.find_point('48 ? ? * * * * 48 89 74 24 ? b2')[0]
        self.replay_party_address = self.real_party_address + main.scanner.find_val('74 ? f6 05 ? ? ? ? ? 48 ? ? * * * * 75')[0]

    @property
    def party_address(self):
        return self.replay_party_address if self.main.is_in_replay else self.real_party_address
