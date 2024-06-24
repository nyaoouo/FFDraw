import ctypes
import enum
import functools
import struct

from nylib.struct import set_fields_from_annotations, fctypes
from ..utils import offset_string, Color, ColorHDRI


class SGActionType(enum.Enum):
    Null = 0X0
    Door = 0X1
    Rotation = 0X2
    RandomTimeline = 0X3
    Clock = 0X4
    Transform = 0X5
    Color = 0X6


@set_fields_from_annotations
class SGAction(ctypes.Structure):
    sg_action_type: 'fctypes.c_int32' = eval('0X0')
    enabled: 'fctypes.c_int8' = eval('0X4')

    @property
    def e_sg_action_type(self):
        return SGActionType(self.sg_action_type)


@set_fields_from_annotations
class SGActionClock(SGAction):
    hour_hand_instance_id: 'fctypes.c_uint8' = eval('0X10')
    minute_hand_instance_id: 'fctypes.c_uint8' = eval('0X11')


@set_fields_from_annotations
class SGActionColor(SGAction):
    @set_fields_from_annotations
    class Item(SGAction):
        class CurveType(enum.Enum):
            Linear = 0X0
            Spline = 0X1

        class BlinkType(enum.Enum):
            SineCurve = 0X0
            Random = 0X1

        enabled: 'fctypes.c_int8' = eval('0X0')
        color_enabled: 'fctypes.c_int8' = eval('0X1')
        color_start: 'ColorHDRI' = eval('0X4')
        color_end: 'ColorHDRI' = eval('0XC')
        power_enabled: 'fctypes.c_int8' = eval('0X14')
        power_start: 'fctypes.c_float' = eval('0X18')
        power_end: 'fctypes.c_float' = eval('0X1C')
        time: 'fctypes.c_uint32' = eval('0X20')
        curve: 'fctypes.c_int32' = eval('0X24')
        blink_enabled: 'fctypes.c_int8' = eval('0X28')
        blink_amplitude: 'fctypes.c_float' = eval('0X2C')
        blink_speed: 'fctypes.c_float' = eval('0X30')
        blink_type: 'fctypes.c_int32' = eval('0X34')
        blink_sync: 'fctypes.c_int8' = eval('0X38')

        @property
        def e_curve(self):
            return self.CurveType(self.curve)

        @property
        def e_blink_type(self):
            return self.BlinkType(self.blink_type)

    _target_sg_member_ids: 'fctypes.c_int32' = eval('0X10')
    target_sg_member_id_count: 'fctypes.c_int32' = eval('0X14')
    loop: 'fctypes.c_int8' = eval('0X18')
    _emissive: 'fctypes.c_int32' = eval('0X20')
    _light: 'fctypes.c_int32' = eval('0X24')

    @functools.cached_property
    def target_sg_member_ids(self):
        return fctypes.array(ctypes.c_uint8, self.target_sg_member_id_count).from_address(ctypes.addressof(self) + self._target_sg_member_ids)

    @functools.cached_property
    def emissive(self):
        return self.Item.from_address(ctypes.addressof(self) + self._emissive)

    @functools.cached_property
    def light(self):
        return self.Item.from_address(ctypes.addressof(self) + self._light)


@set_fields_from_annotations
class SGActionRandomTimeline(SGAction):
    @set_fields_from_annotations
    class Item(ctypes.Structure):
        _size_ = 0X2
        timeline_id: 'fctypes.c_uint8' = eval('0X0')
        probability: 'fctypes.c_uint8' = eval('0X1')

    _random_timeline_items: 'fctypes.c_int32' = eval('0X10')
    random_timeline_item_count: 'fctypes.c_int32' = eval('0X14')

    @functools.cached_property
    def random_timeline_items(self):
        return fctypes.array(self.Item, self.random_timeline_item_count).from_address(ctypes.addressof(self) + self._random_timeline_items)


@set_fields_from_annotations
class SGActionRotation(SGAction):
    class RotationAxis(enum.Enum):
        X = 0X0
        Y = 0X1
        Z = 0X2

    bg_instance_id: 'fctypes.c_uint8' = eval('0X10')
    rotation_axis: 'fctypes.c_int32' = eval('0X14')
    round_time: 'fctypes.c_float' = eval('0X18')
    start_end_time: 'fctypes.c_float' = eval('0X1C')
    vfx_instance_id: 'fctypes.c_uint8' = eval('0X20')
    vfx_rotation_with_bg: 'fctypes.c_int8' = eval('0X21')
    sound_at_starting: 'fctypes.c_uint8' = eval('0X22')
    sound_at_rounding: 'fctypes.c_uint8' = eval('0X23')
    sound_at_stopping: 'fctypes.c_uint8' = eval('0X24')
    vfx_instance_id2: 'fctypes.c_uint8' = eval('0X25')
    vfx_rotation_with_bg2: 'fctypes.c_int8' = eval('0X26')

    @property
    def e_rotation_axis(self):
        return self.RotationAxis(self.rotation_axis)


@set_fields_from_annotations
class SGActionTransform(SGAction):
    @set_fields_from_annotations
    class Item(ctypes.Structure):
        class CurveType(enum.Enum):
            CurveLinear = 0X0
            CurveSpline = 0X1
            CurveAcceleration = 0X2
            CurveDeceleration = 0X3

        class MovementType(enum.Enum):
            MovementOneWay = 0X0
            MovementRoundTrip = 0X1
            MovementRepetition = 0X2

        _size_ = 0X24

        enabled: 'fctypes.c_int8' = eval('0X0')
        offset: 'fctypes.array(fctypes.c_float,3)' = eval('0X4')
        random_rate: 'fctypes.c_float' = eval('0X10')
        time: 'fctypes.c_uint32' = eval('0X14')
        start_end_time: 'fctypes.c_uint32' = eval('0X18')
        curve_type: 'fctypes.c_int32' = eval('0X1C')
        movement_type: 'fctypes.c_int32' = eval('0X20')

        @property
        def e_curve_type(self):
            return self.CurveType(self.curve_type)

        @property
        def e_movement_type(self):
            return self.MovementType(self.movement_type)

    _size_ = 0X2C

    _target_sg_member_ids: 'fctypes.c_int32' = eval('0X10')
    target_sg_member_id_count: 'fctypes.c_int32' = eval('0X14')
    loop: 'fctypes.c_int8' = eval('0X18')
    _translation: 'fctypes.c_int32' = eval('0X20')
    _rotation: 'fctypes.c_int32' = eval('0X24')
    _scale: 'fctypes.c_int32' = eval('0X28')

    @functools.cached_property
    def target_sg_member_ids(self):
        return fctypes.array(ctypes.c_uint8, self.target_sg_member_id_count).from_address(ctypes.addressof(self) + self._target_sg_member_ids)

    @functools.cached_property
    def translation(self):
        return self.Item.from_address(ctypes.addressof(self) + self._translation)

    @functools.cached_property
    def rotation(self):
        return self.Item.from_address(ctypes.addressof(self) + self._rotation)

    @functools.cached_property
    def scale(self):
        return self.Item.from_address(ctypes.addressof(self) + self._scale)


@set_fields_from_annotations
class SGActionDoor(SGAction):
    class CurveType(enum.Enum):
        Spline = 0X1
        Linear = 0X2
        Acceleration = 0X3
        Deceleration = 0X4

    class DoorRotationAxis(enum.Enum):
        X = 0X0
        Y = 0X1
        Z = 0X2

    class OpenStyle(enum.Enum):
        Rotation = 0X0
        HorizontalSlide = 0X1
        VerticalSlide = 0X2

    # Common::DevEnv::Generated::SGActionDoor_t
    _size_ = 0X30

    door_instance_id1: 'fctypes.c_uint8' = eval('0X10')
    door_instance_id2: 'fctypes.c_uint8' = eval('0X11')
    open_style: 'fctypes.c_int32' = eval('0X14')
    time_length: 'fctypes.c_float' = eval('0X18')
    open_angle: 'fctypes.c_float' = eval('0X1C')
    open_distance: 'fctypes.c_float' = eval('0X20')
    sound_at_opening: 'fctypes.c_uint8' = eval('0X24')
    sound_at_closing: 'fctypes.c_uint8' = eval('0X25')
    door_instance_id3: 'fctypes.c_uint8' = eval('0X26')
    door_instance_id4: 'fctypes.c_uint8' = eval('0X27')
    curve_type: 'fctypes.c_int32' = eval('0X28')
    rotation_axis: 'fctypes.c_int32' = eval('0X2C')

    @property
    def e_open_style(self):
        return self.OpenStyle(self.open_style)

    @property
    def e_curve_type(self):
        return self.CurveType(self.curve_type)

    @property
    def e_rotation_axis(self):
        return self.DoorRotationAxis(self.rotation_axis)


sg_action_map = {
    SGActionType.Door.value: SGActionDoor,
    SGActionType.Rotation.value: SGActionRotation,
    SGActionType.RandomTimeline.value: SGActionRandomTimeline,
    SGActionType.Clock.value: SGActionClock,
    SGActionType.Transform.value: SGActionTransform,
    SGActionType.Color.value: SGActionColor,
}


def get_sg_action(buf, off=0) -> SGAction:
    return (sg_action_map.get(struct.unpack_from(b'I', buf, off)[0]) or SGAction).from_buffer(buf, off)


def get_sg_action_from_addr(addr) -> SGAction:
    return (sg_action_map.get(ctypes.c_int32.from_address(addr).value) or SGAction).from_address(addr)
