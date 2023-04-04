import typing

import glm

from nylib.utils.win32 import memory as ny_mem, process as ny_proc
from nylib.pefile import PE
from nylib.pattern import StaticPatternSearcher
from . import utils, actor, party, network_target, packet_fix, marking, territory_info, event_module, quest_info

if typing.TYPE_CHECKING:
    from ff_draw.main import FFDraw


class XivMem:
    def __init__(self, main: 'FFDraw', pid: int):
        self.main = main
        self.pid = pid
        self.handle = ny_proc.open_process(pid)
        self.base_module = ny_proc.get_base_module(self.handle)
        file_name = self.base_module.filename.decode(self.main.path_encoding)
        self.scanner = StaticPatternSearcher(PE(file_name, fast_load=True), self.base_module.lpBaseOfDll)
        self.hwnd = utils.get_hwnd(self.pid)
        self.game_version, self.game_build_date = utils.get_game_version_info(file_name)
        self.screen_address = self.scanner.find_point('48 ? ? * * * * e8 ? ? ? ? 42 ? ? ? 39 05')[0] + 0x1b4
        self.replay_flag_address = self.scanner.find_point('84 1d * * * * 74 ? 80 3d')[0]
        self._a_p_framework = self.scanner.find_point('48 ? ? * * * * 41 39 b1')[0]
        self.actor_table = actor.ActorTable(self)
        self.party = party.PartyManager(self)
        self.network_target = network_target.NetworkInfo(self)
        self.packet_fix = packet_fix.PacketFix(self)
        self.marking = marking.MarkingController(self)
        self.territory_info = territory_info.TerritoryInfo(self)
        self.event_module = event_module.EventModule(self)
        self.quest_info = quest_info.QuestInfo(self)

    def load_screen(self):
        buf = ny_mem.read_bytes(self.handle, self.screen_address, 0x48)
        return glm.mat4.from_bytes(bytes(buf[:0x40])), glm.vec2.from_bytes(bytes(buf[0x40:]))

    @property
    def p_framework(self):
        return ny_mem.read_address(self.handle, self._a_p_framework)

    @property
    def is_in_replay(self):
        return (ny_mem.read_ubyte(self.handle, self.replay_flag_address) & 0b100) > 0
