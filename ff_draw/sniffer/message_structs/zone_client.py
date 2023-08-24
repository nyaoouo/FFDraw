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
    dir: 'fctypes.c_float' = eval('0X0')
    flag: 'fctypes.c_uint16' = eval('0X4')
    flag_2: 'fctypes.c_uint8' = eval('0X6')
    _pos: 'fctypes.array(fctypes.c_float, 3)' = eval('0X8')

    @property
    def pos(self):
        return glm.vec3(*self._pos)
