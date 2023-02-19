from ctypes import *

import glm

from nylib.struct import set_fields_from_annotations, fctypes
from ff_draw.sniffer.utils.simple import pos_web_to_raw, dir_web_to_raw
from . import TypeMap, ZoneServer

type_map = TypeMap()


@type_map.set(ZoneServer.ActorCast)
@set_fields_from_annotations
class ActorCast(Structure):
    _size_ = 0X20
    action_id: 'fctypes.c_uint16' = eval('0X0')
    action_kind: 'fctypes.c_uint8' = eval('0X2')
    display_delay: 'fctypes.c_uint8' = eval('0X3')
    real_action_id: 'fctypes.c_uint32' = eval('0X4')
    cast_time: 'fctypes.c_float' = eval('0X8')
    target_id: 'fctypes.c_uint32' = eval('0XC')
    _facing: 'fctypes.c_uint16' = eval('0X10')
    can_interrupt: 'fctypes.c_uint8' = eval('0X12')
    _pos: 'fctypes.array(fctypes.c_uint16, 3)' = eval('0X18')

    def _pkt_fix(self, v):
        self.real_action_id += v

    @property
    def pos(self):
        return glm.vec3(*map(pos_web_to_raw, self._pos))

    @property
    def facing(self):
        return dir_web_to_raw(self._facing)


@type_map.set(ZoneServer.ActorControl)
@set_fields_from_annotations
class ActorControl(Structure):
    _size_ = 0X18
    id: 'fctypes.c_uint16' = eval('0X0')
    arg0: 'fctypes.c_uint32' = eval('0X4')
    arg1: 'fctypes.c_uint32' = eval('0X8')
    arg2: 'fctypes.c_uint32' = eval('0XC')
    arg3: 'fctypes.c_uint32' = eval('0X10')


@type_map.set(ZoneServer.ActorControlSelf)
@set_fields_from_annotations
class ActorControlSelf(Structure):
    _size_ = 0X20

    id: 'fctypes.c_uint16' = eval('0X0')
    arg0: 'fctypes.c_uint32' = eval('0X4')
    arg1: 'fctypes.c_uint32' = eval('0X8')
    arg2: 'fctypes.c_uint32' = eval('0XC')
    arg3: 'fctypes.c_uint32' = eval('0X10')
    arg4: 'fctypes.c_uint32' = eval('0X14')
    arg5: 'fctypes.c_uint32' = eval('0X18')


@type_map.set(ZoneServer.ActorControlTarget)
@set_fields_from_annotations
class ActorControlTarget(Structure):
    _size_ = 0X20
    id: 'fctypes.c_uint16' = eval('0X0')
    arg0: 'fctypes.c_uint32' = eval('0X4')
    arg1: 'fctypes.c_uint32' = eval('0X8')
    arg2: 'fctypes.c_uint32' = eval('0XC')
    arg3: 'fctypes.c_uint32' = eval('0X10')
    target_id: 'fctypes.c_uint64' = eval('0X18')
