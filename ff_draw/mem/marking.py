import enum
import typing
import glm
import imgui

from nylib.utils.imgui import ctx as imgui_ctx
from nylib.utils.win32 import memory as ny_mem

if typing.TYPE_CHECKING:
    from . import XivMem


class HeadMarkType(enum.Enum):
    Attack1 = 1
    Attack2 = 2
    Attack3 = 3
    Attack4 = 4
    Attack5 = 5
    Bind1 = 6
    Bind2 = 7
    Bind3 = 8
    Stop1 = 9
    Stop2 = 10
    Square = 11
    Circle = 12
    Cross = 13
    Triangle = 14
    Attack6 = 15
    Attack7 = 16
    Attack8 = 17


class WayMarkType(enum.Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    One = 4
    Two = 5
    Three = 6
    Four = 7


class WayMark:
    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    @property
    def pos(self):
        return glm.vec3.from_bytes(bytes(ny_mem.read_bytes(self.handle, self.address, 0xc)))

    @property
    def is_enable(self):
        return ny_mem.read_byte(self.handle, self.address + 0x1c) != 0


class MarkingController:
    def __init__(self, main: 'XivMem'):
        self.main = main
        self.handle = main.handle
        self.address = main.scanner.find_point('48 8D ? * * * * 41 B0 ? E8 ? ? ? ? 85 C0')[0]
        self._way_marks = [WayMark(self.handle, self.address + (0x1b0 if main.game_version < (6, 4, 0) else 0x1e0) + (i * 0x20)) for i in range(8)]

        self.fp_request_head_mark = main.scanner.find_address('48 89 5C 24 ? 48 89 6C 24 ? 57 48 83 EC ? 8D 42 ? 49 8B E8')
        self.fp_request_way_mark = main.scanner.find_address('48 89 6C 24 ? 48 89 74 24 ? 57 48 83 EC ? 8B F2 49 8B E8')
        self.fp_request_clear_way_mark = main.scanner.find_address('48 89 74 24 ? 57 48 83 EC ? 8B F2 48 8B F9 83 FA ? 72 ?')
        self.fp_request_clear_all_way_mark = main.scanner.find_address('41 55 48 83 EC ? 4C 8B E9 E8 ? ? ? ? 84 C0')

    def head_mark_target(self, mark_type: int | HeadMarkType):
        if isinstance(mark_type, HeadMarkType): mark_type = mark_type.value
        res = ny_mem.read_uint64(self.handle, self.address + 0x10 + (mark_type - 1) * 8)
        if res == 0xe0000000: return 0
        return res

    def way_mark(self, mark_type: int | WayMarkType):
        if isinstance(mark_type, WayMarkType): mark_type = mark_type.value
        return self._way_marks[mark_type]

    def request_head_mark(self, mark_type: int | HeadMarkType, target_id):
        if isinstance(mark_type, HeadMarkType): mark_type = mark_type.value
        res = self.main.call_native_once_game_main(self.fp_request_head_mark, 'c_uint8', ('c_void_p', 'c_uint', 'c_uint64'), (
            self.address, mark_type, target_id
        ))
        assert res == 0, f'Failed to request head mark {mark_type}: {res=}'

    def request_way_mark(self, mark_type: int | WayMarkType, pos: glm.vec3):
        if isinstance(mark_type, WayMarkType): mark_type = mark_type.value
        res = self.main.call_once_game_main(f'''
from ctypes import *
vec=(c_float * 3)({pos.x},{pos.y},{pos.z})
res=CFUNCTYPE(c_uint8,c_void_p,c_uint,c_void_p)({self.fp_request_way_mark})({self.address},{mark_type},byref(vec))
''')
        assert res == 0, f'Failed to request way mark {mark_type}: {res=}'

    def request_clear_way_mark(self, mark_type: int | WayMarkType):
        if isinstance(mark_type, WayMarkType): mark_type = mark_type.value
        res = self.main.call_native_once_game_main(self.fp_request_clear_way_mark, 'c_uint8', ('c_void_p', 'c_uint'), (
            self.address, mark_type
        ))
        assert res == 0, f'Failed to request clear way mark {mark_type}: {res=}'

    def request_clear_all_way_mark(self):
        res = self.main.call_native_once_game_main(self.fp_request_clear_all_way_mark, 'c_uint8', ('c_void_p',), (self.address,))
        assert res == 0, f'Failed to request clear all way mark: {res=}'

    def render_debug(self):
        with imgui_ctx.TreeNode('Head Mark') as n, n:
            for head_mark_type in HeadMarkType:
                t_id = self.head_mark_target(head_mark_type)
                imgui.text(f'{head_mark_type.name}: {t_id:x}')
        with imgui_ctx.TreeNode('Way Mark') as n, n:
            for way_mark_type in WayMarkType:
                if (way_mark := self.way_mark(way_mark_type)).is_enable:
                    pos = way_mark.pos
                    imgui.text(f'{way_mark_type.name}: {pos.x:.2f}, {pos.y:.2f}, {pos.z:.2f}')
                else:
                    imgui.text(f'{way_mark_type.name}: -')
