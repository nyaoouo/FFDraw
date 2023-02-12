import os
import glm
from win32con import PROCESS_ALL_ACCESS

from nylib.utils.win32 import memory as ny_mem, process as ny_proc, winapi as ny_winapi
from nylib.pefile import PE
from nylib.pattern import StaticPatternSearcher
from . import utils, actor, party


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
        self.replay_flag_address = self.scanner.find_point('f6 05 * * * * ? 45 ? ? 8b')[0]
        self.actor_table = actor.ActorTable(self)
        self.party = party.PartyManager(self)

    def load_screen(self):
        buf = ny_mem.read_bytes(self.handle, self.screen_address, 0x48)
        return glm.mat4.from_bytes(bytes(buf[:0x40])), glm.vec2.from_bytes(bytes(buf[0x40:]))

    @property
    def is_in_replay(self):
        return (ny_mem.read_ubyte(self.handle, self.replay_flag_address) & 0b100) > 0
