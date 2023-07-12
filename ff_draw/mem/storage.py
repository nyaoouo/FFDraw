import ctypes
import typing

import imgui

from nylib.utils.imgui import ctx as imgui_ctx
from nylib.utils.win32 import memory as ny_mem
from .utils import direct_mem_property

if typing.TYPE_CHECKING:
    from . import XivMem


class Item:
    class offsets:
        storage_id = 0
        container_idx = 0x4
        is_alias = 0x6
        item_id = 0x8
        quantity = 0xc
        spiritbond = 0x10
        durability = 0x12
        flags = 0x14
        signature_id = 0x18
        materia_type = 0x20
        materia_grade = 0x2a
        stain = 0x2f
        glamour_id = 0x30

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    storage_id = direct_mem_property(ctypes.c_uint32)
    container_idx = direct_mem_property(ctypes.c_uint16)
    is_alias = direct_mem_property(ctypes.c_ubyte)
    item_id = direct_mem_property(ctypes.c_uint32)
    quantity = direct_mem_property(ctypes.c_uint32)
    spiritbond = direct_mem_property(ctypes.c_uint16)
    durability = direct_mem_property(ctypes.c_uint16)
    flags = direct_mem_property(ctypes.c_uint8)
    signature_id = direct_mem_property(ctypes.c_uint64)
    stain = direct_mem_property(ctypes.c_uint8)
    glamour_id = direct_mem_property(ctypes.c_uint32)

    def materia_type(self, idx: int):
        assert idx < 5
        return ny_mem.read_ushort(self.handle, self.address + self.offsets.materia_type + idx * 2)

    def materia_grade(self, idx: int):
        assert idx < 5
        return ny_mem.read_ubyte(self.handle, self.address + self.offsets.materia_grade + idx)

    def materials(self):
        for i in range(5):
            if (t := self.materia_type(i)) != 0:
                yield t, self.materia_grade(i)

    def render_debug(self):
        imgui.text(f'item_id: {self.item_id}')
        imgui.text(f'quantity: {self.quantity}')


class Storage:
    class offsets:
        storage_id = 0x8
        max_count = 0xc
        is_synced = 0x10

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    storage_id = direct_mem_property(ctypes.c_uint32)
    max_count = direct_mem_property(ctypes.c_uint32)
    is_synced = direct_mem_property(ctypes.c_ubyte)

    @property
    def p_items(self):
        return ny_mem.read_address(self.handle, self.address)

    def __bool__(self):
        return self.p_items != 0

    def __getitem__(self, item):
        assert isinstance(item, int)
        if (p_items := self.p_items) == 0: raise IndexError('Storage is not valid')
        return Item(self.handle, p_items + item * 0x38)

    def __iter__(self):
        if (p_items := self.p_items) == 0: return
        for i in range(self.max_count):
            if (item := Item(self.handle, p_items + i * 0x38)).item_id:
                yield item

    def __len__(self):
        if (p_items := self.p_items) == 0: return 0
        return sum(1 for i in range(self.max_count) if Item(self.handle, p_items + i * 0x38).item_id)

    def render_debug(self):
        if (p_items := self.p_items) == 0: return
        for i in range(self.max_count):
            if (item := Item(self.handle, p_items + i * 0x38)).item_id:
                with imgui_ctx.TreeNode(f'Item-{i}') as n, n:
                    item.render_debug()


class StorageManager:
    def __init__(self, main: 'XivMem'):
        self.main = main
        self.address, = main.scanner.find_point('48 ? ? * * * * 8b ? 66 89 5c 24 ?')
        self.handle = main.handle

    @property
    def p_storage(self):
        return ny_mem.read_address(self.handle, self.address + 0x1E08)

    def __getitem__(self, item):
        assert isinstance(item, int)
        if (p_storage := self.p_storage) == 0: raise IndexError('StorageManager is not valid')
        return Storage(self.handle, p_storage + item * 0x18)

    def __iter__(self):
        if (p_storage := self.p_storage) == 0: return
        for i in range(74):
            yield Storage(self.handle, p_storage + i * 0x18)

    def render_debug(self):
        for storage in self:
            with imgui_ctx.TreeNode(f'Storage-{storage.storage_id}') as n, n:
                storage.render_debug()
