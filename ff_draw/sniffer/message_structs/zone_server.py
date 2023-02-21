from ctypes import *

import glm

from nylib.struct import set_fields_from_annotations, fctypes
from ff_draw.sniffer.utils.simple import pos_web_to_raw, dir_web_to_raw
from . import TypeMap, ZoneServer

type_map = TypeMap()


@set_fields_from_annotations
class ActionEffectBase(Structure):
    _size_ = 0X28
    main_target_id: 'fctypes.c_uint32' = eval('0X0')
    real_action_id: 'fctypes.c_uint32' = eval('0X8')
    response_id: 'fctypes.c_uint32' = eval('0XC')
    lock_time: 'fctypes.c_float' = eval('0X10')
    ballista_target_id: 'fctypes.c_uint32' = eval('0X14')
    request_id: 'fctypes.c_uint16' = eval('0X18')
    _facing: 'fctypes.c_uint16' = eval('0X1A')
    action_id: 'fctypes.c_uint16' = eval('0X1C')
    action_variant: 'fctypes.c_uint8' = eval('0X1E')
    action_kind: 'fctypes.c_uint8' = eval('0X1F')
    flag: 'fctypes.c_uint8' = eval('0X20')
    target_count: 'fctypes.c_uint8' = eval('0X21')

    def _pkt_fix(self, v):
        self.real_action_id += v

    @property
    def facing(self):
        return dir_web_to_raw(self._facing)


@set_fields_from_annotations
class ActionEffect(Structure):
    _size_ = 0X8
    type: 'fctypes.c_uint8' = eval('0X0')
    arg0: 'fctypes.c_uint8' = eval('0X1')
    arg1: 'fctypes.c_uint8' = eval('0X2')
    arg2: 'fctypes.c_uint8' = eval('0X3')
    arg3: 'fctypes.c_uint8' = eval('0X4')
    flag: 'fctypes.c_uint8' = eval('0X5')
    value: 'fctypes.c_int16' = eval('0X6')


ActionEffects = fctypes.array(ActionEffect, 8)


@type_map.set(ZoneServer.Effect)
@set_fields_from_annotations
class ActionEffect(ActionEffectBase):
    _size_ = 0X78
    effects: 'fctypes.array(ActionEffects, 1)' = eval('0X2A')
    target_ids: 'fctypes.array(fctyes.c_uint64, 1)' = eval('0X70')
    pos = glm.vec3(0, 0, 0)


@type_map.set(ZoneServer.AoeEffect8)
@set_fields_from_annotations
class ActionEffect8(ActionEffectBase):
    _size_ = 0X278
    effects: 'fctypes.array(ActionEffects, 8)' = eval('0X2A')
    target_ids: 'fctypes.array(fctyes.c_uint64, 8)' = eval('0X230')
    _pos: 'fctypes.array(fctypes.c_uint16, 3)' = eval('0X270')

    @property
    def pos(self):
        return glm.vec3(*map(pos_web_to_raw, self._pos))


@type_map.set(ZoneServer.AoeEffect16)
@set_fields_from_annotations
class ActionEffect16(ActionEffectBase):
    _size_ = 0X4B8
    effects: 'fctypes.array(ActionEffects, 16)' = eval('0X2A')
    target_ids: 'fctypes.array(fctyes.c_uint64, 16)' = eval('0X430')
    _pos: 'fctypes.array(fctypes.c_uint16, 3)' = eval('0X4B0')

    @property
    def pos(self):
        return glm.vec3(*map(pos_web_to_raw, self._pos))


@type_map.set(ZoneServer.AoeEffect24)
@set_fields_from_annotations
class ActionEffect24(ActionEffectBase):
    _size_ = 0X6F8
    effects: 'fctypes.array(ActionEffects, 24)' = eval('0X2A')
    target_ids: 'fctypes.array(fctyes.c_uint64, 24)' = eval('0X630')
    _pos: 'fctypes.array(fctypes.c_uint16, 3)' = eval('0X6F0')

    @property
    def pos(self):
        return glm.vec3(*map(pos_web_to_raw, self._pos))


@type_map.set(ZoneServer.AoeEffect32)
@set_fields_from_annotations
class ActionEffect32(ActionEffectBase):
    _size_ = 0X6F8
    effects: 'fctypes.array(ActionEffects, 32)' = eval('0X2A')
    target_ids: 'fctypes.array(fctyes.c_uint64, 32)' = eval('0X830')
    _pos: 'fctypes.array(fctypes.c_uint16, 3)' = eval('0X930')

    @property
    def pos(self):
        return glm.vec3(*map(pos_web_to_raw, self._pos))


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


@type_map.set(ZoneServer.ActorDelete)
@set_fields_from_annotations
class ActorDelete(Structure):
    _size_ = 0X8

    index: 'fctypes.c_uint8' = eval('0X0')
    actor_id: 'fctypes.c_uint32' = eval('0X4')


@type_map.set(ZoneServer.ActorGauge)
@set_fields_from_annotations
class ActorGauge(Structure):
    _size_ = 0X10
    buffer: 'c_char*16' = eval('0X0')
