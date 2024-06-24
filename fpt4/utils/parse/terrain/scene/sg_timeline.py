import ctypes
import enum
import functools

from nylib.struct import set_fields_from_annotations, fctypes
from ..utils import offset_string


class CollisionState(enum.Enum):
    NoChange = 0X0
    On = 0X1
    Off = 0X2


@set_fields_from_annotations
class SGActorBinder(ctypes.Structure):
    _size_ = 0X8
    actor_type: 'fctypes.c_uint32' = eval('0X0')
    instance_id: 'fctypes.c_uint32' = eval('0X4')


@set_fields_from_annotations
class SGTimeline(ctypes.Structure):
    # Common::DevEnv::Generated::SGTimeline_t
    _size_ = 0X2C

    member_id: 'fctypes.c_uint32' = eval('0X0')
    _name: 'fctypes.c_int32' = eval('0X4')
    _binders: 'fctypes.c_int32' = eval('0X8')
    binder_count: 'fctypes.c_int32' = eval('0XC')
    _binary_asset_path: 'fctypes.c_int32' = eval('0X10')
    _binary: 'fctypes.c_int32' = eval('0X14')
    binary_count: 'fctypes.c_int32' = eval('0X18')
    timeline_id: 'fctypes.c_uint32' = eval('0X1C')
    auto_play: 'fctypes.c_int8' = eval('0X20')
    loop_playback: 'fctypes.c_int8' = eval('0X21')
    collision_state: 'fctypes.c_uint32' = eval('0X24')

    name = offset_string('_name')
    binary_asset_path = offset_string('_binary_asset_path')

    @property
    def e_collision_state(self):
        return CollisionState(self.collision_state)

    @functools.cached_property
    def binders(self):
        return fctypes.array(SGActorBinder, self.binder_count).from_address(ctypes.addressof(self) + self._binders)

    @functools.cached_property
    def binary(self):
        return fctypes.array(ctypes.c_uint8, self.binary_count).from_address(ctypes.addressof(self) + self._binary)


@set_fields_from_annotations
class SGTimelineFolder(ctypes.Structure):
    _size_ = 0X8

    _sg_timelines: 'fctypes.c_int32' = eval('0X0')
    sg_timeline_count: 'fctypes.c_int32' = eval('0X4')

    @property
    def sg_timelines(self):
        return fctypes.array(SGTimeline, self.sg_timeline_count).from_address(ctypes.addressof(self) + self._sg_timelines)
