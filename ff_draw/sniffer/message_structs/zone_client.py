from ctypes import *

import glm

from nylib.struct import set_fields_from_annotations, fctypes
from . import TypeMap, ZoneClient

type_map = TypeMap()


@type_map.set(ZoneClient.UpdatePositionInstance)
@set_fields_from_annotations
class UpdatePositionInstance(Structure):
    _size_ = 0X24
    facing: 'fctypes.c_float' = eval('0X0')
    predicted_facing: 'fctypes.c_float' = eval('0X4')
    flag: 'fctypes.c_uint16' = eval('0X8')
    flag_2: 'fctypes.c_uint8' = eval('0XA')
    _pos: 'fctypes.array(fctypes.c_float, 3)' = eval('0XC')
    _predicted_pos: 'fctypes.array(fctypes.c_float, 3)' = eval('0X18')

    @property
    def pos(self):
        return glm.vec3(*self._pos)

    @property
    def predicted_pos(self):
        return glm.vec3(*self._predicted_pos)


@type_map.set(ZoneClient.UpdatePositionHandler)
@set_fields_from_annotations
class UpdatePositionHandler(Structure):
    _size_ = 0X24
    facing: 'fctypes.c_float' = eval('0X0')
    flag: 'fctypes.c_uint16' = eval('0X4')
    flag_2: 'fctypes.c_uint8' = eval('0X6')
    _pos: 'fctypes.array(fctypes.c_float, 3)' = eval('0X8')

    @property
    def pos(self):
        return glm.vec3(*self._pos)


@type_map.set(ZoneClient.EventStart)
@set_fields_from_annotations
class EventStart(Structure):
    _size_ = 0x10
    target_common_id: 'fctypes.c_uint64' = eval('0x0')
    handler_id: 'fctypes.c_uint32' = eval('0x8')


@type_map.set(ZoneClient.EventFinish)
@set_fields_from_annotations
class EventFinish(Structure):
    _size_ = 0x10
    handler_id: 'fctypes.c_uint32' = eval('0X0')
    scene_id: 'fctypes.c_uint16' = eval('0X4')
    error: 'fctypes.c_uint8' = eval('0X6')
    arg_cnt: 'fctypes.c_uint8' = eval('0X7')
    _args: 'fctypes.array(fctypes.c_uint32, 255)' = eval('0X8')

    @property
    def args(self):
        return self._args[:self.arg_cnt]


@type_map.set(ZoneClient.EventAction)
@set_fields_from_annotations
class EventAction(Structure):
    _size_ = 0X10

    handler_id: 'fctypes.c_uint32' = eval('0X0')
    scene_id: 'fctypes.c_uint16' = eval('0X4')
    res: 'fctypes.c_uint8' = eval('0X6')
    arg_cnt: 'fctypes.c_uint8' = eval('0X7')
    _args: 'fctypes.array(fctypes.c_uint32, 255)' = eval('0X8')

    @property
    def args(self):
        return self._args[:self.arg_cnt]


@type_map.set(ZoneClient.ClientTrigger)
@set_fields_from_annotations
class ClientTrigger(Structure):
    _size_ = 0x20
    id: 'fctypes.c_uint32' = eval('0X0')
    arg0: 'fctypes.c_uint32' = eval('0X4')
    arg1: 'fctypes.c_uint32' = eval('0X8')
    arg2: 'fctypes.c_uint32' = eval('0XC')
    arg3: 'fctypes.c_uint32' = eval('0X10')
    target_common_id: 'fctypes.c_uint64' = eval('0X18')


@type_map.set(ZoneClient.PingReq)
@set_fields_from_annotations
class PingReq(Structure):
    _size_ = 0X18
    time_ms: 'fctypes.c_uint32' = eval('0X0')


@type_map.set(ZoneClient.ActionSend)
@set_fields_from_annotations
class ActionSend(Structure):
    _size_ = 0X20

    cast_buff: 'fctypes.c_uint8' = eval('0X0')
    action_kind: 'fctypes.c_uint8' = eval('0X1')
    action_id: 'fctypes.c_uint32' = eval('0X4')
    request_id: 'fctypes.c_uint16' = eval('0X8')
    facing: 'fctypes.c_uint16' = eval('0XA')
    target_facing: 'fctypes.c_uint16' = eval('0XC')
    target_id: 'fctypes.c_uint64' = eval('0X10')
    arg: 'fctypes.c_uint32' = eval('0X18')


@type_map.set(ZoneClient.ActionSendPos)
@set_fields_from_annotations
class ActionSendPos(Structure):
    _size_ = 0X20

    cast_buff: 'fctypes.c_uint8' = eval('0X0')
    action_kind: 'fctypes.c_uint8' = eval('0X1')
    action_id: 'fctypes.c_uint32' = eval('0X4')
    request_id: 'fctypes.c_uint16' = eval('0X8')
    facing: 'fctypes.c_uint16' = eval('0XA')
    target_facing: 'fctypes.c_uint16' = eval('0XC')
    _pos: 'fctypes.array(fctypes.c_float, 3)' = eval('0X10')

    @property
    def pos(self):
        return glm.vec3(*self._pos)
