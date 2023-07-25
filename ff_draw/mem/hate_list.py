import ctypes
import typing
import imgui

from fpt4.utils.se_string import SeString
from nylib.utils.imgui import ctx as imgui_ctx
from nylib.utils.win32 import memory as ny_mem
from .utils import direct_mem_property

if typing.TYPE_CHECKING:
    from . import XivMem


class SelfHateItem:
    class offsets:
        name = 0x0
        id = 0x40
        value = 0x44

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
    value = direct_mem_property(ctypes.c_uint)

    def render_debug(self):
        imgui.text(f'[{self.id:#x}]{self.name} : {self.value}')


class SelfHateList:
    class offsets:
        _list = 0x0
        count = 0x48 * 32

    def __init__(self, mem: 'XivMem'):
        self.handle = mem.handle
        self.address, = mem.scanner.find_point("48 ? ? * * * * e8 ? ? ? ? 84 ? 75 ? 48 ? ? ? 66 83 b8")
        self._list = tuple(SelfHateItem(self.handle, self.address + self.offsets._list + i * 0x48) for i in range(32))

    @property
    def list(self):
        return self._list[:self.count]

    count = direct_mem_property(ctypes.c_uint32)

    def render_debug(self):
        imgui.text(f'count: {self.count}')
        for i, item in enumerate(self.list):
            imgui.text(f'[{i}]')
            imgui.same_line()
            item.render_debug()


class TargetHateItem:
    class offsets:
        id = 0x0
        value = 0x4

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    id = direct_mem_property(ctypes.c_uint)
    value = direct_mem_property(ctypes.c_uint)

    def render_debug(self):
        imgui.text(f'[{self.id:#x}] : {self.value}')


class TargetHateList:
    class offsets:
        _list = 0x0
        count = 0x8 * 32
        target_id = count + 0x4

    def __init__(self, mem: 'XivMem'):
        self.handle = mem.handle
        self.address, = mem.scanner.find_point("48 ? ? * * * * e8 ? ? ? ? 48 ? ? ? ? ? ? e8 ? ? ? ? 48 ? ? ? ? ? ? e8 ? ? ? ? 48 ? ? ? ? ? ? e8 ? ? ? ? 80 bb")
        self._list = tuple(TargetHateItem(self.handle, self.address + self.offsets._list + i * 8) for i in range(32))

    @property
    def list(self):
        return self._list[:self.count]

    count = direct_mem_property(ctypes.c_uint32)
    target_id = direct_mem_property(ctypes.c_uint32)

    def render_debug(self):
        imgui.text(f'target_id: {self.target_id:#x}')
        imgui.text(f'count: {self.count}')
        for i, item in enumerate(self.list):
            imgui.text(f'[{i}]')
            imgui.same_line()
            item.render_debug()


class HateList:
    def __init__(self, mem: 'XivMem'):
        self.self = SelfHateList(mem)
        self.target = TargetHateList(mem)

    def render_debug(self):
        with imgui_ctx.TreeNode('self') as n, n:
            self.self.render_debug()
        with imgui_ctx.TreeNode('target') as n, n:
            self.target.render_debug()
