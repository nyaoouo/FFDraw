import ctypes
import typing

from .types import *
from nylib.struct import set_fields_from_annotations, fctypes
from nylib.utils.serialize import struct_to_dict


@set_fields_from_annotations
class ClipParameter(ctypes.Structure):
    uid: fctypes.c_int32
    ints: fctypes.c_int32 * 4
    floats: fctypes.c_float * 4
    strings: (fctypes.c_char * 32) * 4

    @classmethod
    def load(cls, b, o, s):
        return cls.from_buffer_copy(b, o)

    def pack(self):
        return bytes(self)

    def _serialize_(self):
        return struct_to_dict(self)

    def _dif_(self, other: 'ClipParameter'):
        if type(self) != type(other):
            yield '_type_', self.__class__, type(other)
            return
        if self.uid != other.uid:
            yield 'uid', self.uid, other.uid
        for i in range(4):
            if self.strings[i] != other.strings[i]:
                yield f'{i}.string', self.strings[i], other.strings[i]
            if self.ints[i] != other.ints[i]:
                yield f'{i}.int', self.ints[i], other.ints[i]
            if self.floats[i] != other.floats[i]:
                yield f'{i}.floats', self.floats[i], other.floats[i]


class TimelineItem(AVfxStruct):
    emitter_no = KeyAttr.simple(b'EmNo', 0, s_int8)
    clip_no = KeyAttr.simple(b'ClNo', 0, s_int8)
    effector_no = KeyAttr.simple(b'EfNo', 0, s_int8)
    binder_no = KeyAttr.simple(b'BdNo', 0, s_int8)
    start_time = KeyAttr.simple(b'StTm', 0, s_int16)
    end_time = KeyAttr.simple(b'EdTm', 0, s_int16)
    is_enable = KeyAttr.bool(b'bEna', False, s_int32)
    platform = KeyAttr.simple(b'Plfm', 0, s_int32)


class Timeline(AVfxStruct):
    loop_point_start = KeyAttr.simple(b'LpSt', 0, s_int16)
    loop_point_goal = KeyAttr.simple(b'LpEd', 0, s_int16)
    binder_no = KeyAttr.simple(b'BnNo', 0, s_int8)
    items = KeyListAttr.struct(b'TICn', b'Item', TimelineItem)
    clips = KeyListAttr.struct(b'CpCn', b'Clip', ClipParameter)
