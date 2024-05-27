import ctypes

import imgui

from nylib.utils.imgui import ctx as imgui_ctx
from ff_draw.mem.utils import direct_mem_property, struct_mem_property
from ffd_plus.api.utils.commons import ItemArr
from ffd_plus.utils import game_version
from .utils import is_entity_id_valid


class Status:
    class offsets:
        status_id = 0x0
        param = 0x2
        remain = 0x4
        source_id = 0x8

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    status_id = direct_mem_property(ctypes.c_uint16)
    param = direct_mem_property(ctypes.c_int16)
    remain = direct_mem_property(ctypes.c_float)
    source_id = direct_mem_property(ctypes.c_uint32)


class StatusManager:
    class offsets:
        character = 0x0  # Character*
        status = 0x8  # Status[30]

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    @property
    def character(self):
        if addr := self.handle.read_address(self.address + self.offsets.character):
            from ffd_plus.api.game_object_manager.character import Character
            return Character(self.handle, addr)

    if game_version >= (6, 5, 0):
        status = struct_mem_property(ItemArr[Status, 12, 60])
    else:
        status = struct_mem_property(ItemArr[Status, 12, 30])

    def find_status(self, status_id, source_id=0):
        if is_entity_id_valid(source_id):
            for s in self.status:
                if s.status_id == status_id and s.source_id == source_id:
                    return s
        else:
            for s in self.status:
                if s.status_id == status_id:
                    return s

    def __iter__(self):
        for s in self.status:
            if s.status_id:
                yield s

    def render_panel(self):
        with imgui_ctx.TreeNode(f'StatusManager#{self.address:X}', push_id=True) as n, n:
            for i, s in enumerate(self.status):
                if s.status_id:
                    imgui.text(f'[{i}] status {s.status_id}[{s.param}] from {s.source_id:x} remain {s.remain}s')
