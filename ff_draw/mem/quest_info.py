import ctypes
import typing

import imgui

from nylib.utils.win32 import memory as ny_mem
from .utils import direct_mem_property

if typing.TYPE_CHECKING:
    from . import XivMem


class Quest:
    class offsets:
        id = 0x8
        seq = 0xa
        flag = 0xb
        vars = 0xc
        class_job = 0x12

    def __init__(self, main: 'QuestInfo', address: int):
        self.main = main
        self.handle = main.handle
        self.address = address

    id = direct_mem_property(ctypes.c_ushort)
    seq = direct_mem_property(ctypes.c_ubyte)
    flag = direct_mem_property(ctypes.c_ubyte)
    class_job = direct_mem_property(ctypes.c_ubyte)

    @property
    def vars(self):
        return ny_mem.read_bytes(self.handle, self.address + self.offsets.vars, self.offsets.class_job - self.offsets.vars)


class QuestInfo:
    def __init__(self, main: 'XivMem'):
        self.main = main
        self.handle = main.handle
        self.p_info, = main.scanner.find_point('48 ? ? * * * * e8 ? ? ? ? c6 44 24 ? ? 0f')

    def quest(self, idx):
        return Quest(self, self.p_info + 0x10 + idx * 0x18)

    def quests(self):
        for i in range(30):
            if (q := self.quest(i)).id:
                yield q

    def is_quest_completed(self, quest_id):
        return ny_mem.read_ubyte(self.handle, self.p_info + 0x2E0 + (quest_id // 8)) & (0x80 >> (quest_id % 8)) != 0

    def render_debug(self):
        quest_sheet = self.main.main.sq_pack.sheets.quest_sheet
        try:
            for quest in self.quests():
                try:
                    quest_data = quest_sheet[quest.id | 0x10000]
                except KeyError:
                    imgui.text(f'N/A#{quest.id}[{quest.seq}]')
                else:
                    imgui.text(f'{quest_data.text}#{quest.id}[{quest.seq}]')
        except Exception as e:
            imgui.text('N/A - ' + str(e))
