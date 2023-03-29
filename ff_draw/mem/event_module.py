import ctypes
import typing
from nylib.utils.win32 import memory as ny_mem
from .utils import direct_mem_property, read_utf8_string, StdVector

if typing.TYPE_CHECKING:
    from . import XivMem


class ContentTodo:
    class offsets:
        is_valid = 0x0
        type = 0x4
        desc = 0x8
        _is_set_finish = 0x70
        _check_finish_by_data = 0x71
        data = 0x78  # TODO: different type has different data

    def __init__(self, handle, addr):
        self.handle = handle
        self.address = addr

    is_valid = direct_mem_property(ctypes.c_bool)
    type = direct_mem_property(ctypes.c_int32)
    desc = property(lambda self: read_utf8_string(self.handle, self.address + self.offsets.desc))
    _is_set_finish = direct_mem_property(ctypes.c_bool)
    _check_finish_by_data = direct_mem_property(ctypes.c_bool)

    @property
    def is_finished(self):
        if self._check_finish_by_data:
            _type = self.type
            if _type == 0x1 or _type == 6:
                v_current = ny_mem.read_int(self.handle, self.address + self.offsets.data)
                v_max = ny_mem.read_int(self.handle, self.address + self.offsets.data + 0x4)
                return v_current >= v_max
        return self._is_set_finish


class ContentInfoOffset:
    handler_id = 0x20
    p_director_id = 0x330
    content_id = 0x338
    title = 0x350
    text1 = 0x3B8
    text2 = 0X420
    todo_list = 0x498


class ContentInfo:
    offsets = ContentInfoOffset

    def __init__(self, event_module: 'EventModule'):
        self.event_module = event_module
        self.main = event_module.main
        self.handle = event_module.main.handle

        # mov     rax, [rcx+158h]
        get_content_info_func = self.main.scanner.find_point('e8 * * * * 48 ? ? 0f 84 ? ? ? ? 8b ? ? ? 0f ? ? 44')[0]
        self._content_info_offset = ny_mem.read_int(self.handle, get_content_info_func + 3)

    @property
    def address(self):
        if p_event := self.event_module._p_event:
            return ny_mem.read_address(self.handle, p_event + self._content_info_offset)
        return 0

    handler_id = direct_mem_property(ctypes.c_uint32)
    content_id = direct_mem_property(ctypes.c_uint32)

    @property
    def title(self):
        if not (addr := self.address): raise AttributeError('ContentInfo not found')
        return read_utf8_string(self.handle, addr + self.offsets.title)

    @property
    def text1(self):
        if not (addr := self.address): raise AttributeError('ContentInfo not found')
        return read_utf8_string(self.handle, addr + self.offsets.text1)

    @property
    def text2(self):
        if not (addr := self.address): raise AttributeError('ContentInfo not found')
        return read_utf8_string(self.handle, addr + self.offsets.text2)

    @property
    def todo_list(self):
        if not (addr := self.address): raise AttributeError('ContentInfo not found')
        return StdVector(self.handle, addr + self.offsets.todo_list, ContentTodo, 0x160)


class EventModule:
    def __init__(self, main: 'XivMem'):
        self.main = main
        self.handle = main.handle
        self._a_p_event = main.scanner.find_point('48 39 1d * * * * 48 89 b4 24')[0]

        self.content_info = ContentInfo(self)

    @property
    def _p_event(self):
        return ny_mem.read_address(self.handle, self._a_p_event)
