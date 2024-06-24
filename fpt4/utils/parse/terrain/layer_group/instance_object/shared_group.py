import enum
import struct

from .utils import *


@set_fields_from_annotations
class SGOverriddenMember(ctypes.Structure):
    asset_type: 'fctypes.c_int32' = eval('0X0')
    member_id: 'fctypes.array(fctypes.c_uint8, 4)' = eval('0X4')


@set_fields_from_annotations
class SGOverriddenVFX(SGOverriddenMember):
    color_enable: 'fctypes.c_int8' = eval('0X8')
    color: 'Color' = eval('0X9')
    is_auto_play: 'fctypes.c_uint8' = eval('0XD')
    z_correct_enable: 'fctypes.c_int8' = eval('0XE')
    z_correct: 'fctypes.c_float' = eval('0X10')


@set_fields_from_annotations
class SGOverriddenLight(SGOverriddenMember):
    diffuse_color_hdri: 'ColorHDRI' = eval('0X8')
    shadow_clip_range: 'fctypes.c_float' = eval('0X10')
    specular_enabled: 'fctypes.c_int8' = eval('0X14')
    bg_shadow_enabled: 'fctypes.c_int8' = eval('0X15')
    character_shadow_enabled: 'fctypes.c_int8' = eval('0X16')
    merge_group_id: 'fctypes.c_uint16' = eval('0X18')
    diffuse_color_hdr_edited: 'fctypes.c_int8' = eval('0X1A')
    shadow_clip_range_edited: 'fctypes.c_int8' = eval('0X1B')
    specular_enabled_edited: 'fctypes.c_int8' = eval('0X1C')
    bg_shadow_enabled_edited: 'fctypes.c_int8' = eval('0X1D')
    character_shadow_enabled_edited: 'fctypes.c_int8' = eval('0X1E')
    merge_group_id_edited: 'fctypes.c_int8' = eval('0X1F')


@set_fields_from_annotations
class SGOverriddenBG(SGOverriddenMember):
    render_shadow_enabled: 'fctypes.c_uint8' = eval('0X8')
    render_light_shadow_enabled: 'fctypes.c_uint8' = eval('0X9')
    render_model_clip_range: 'fctypes.c_float' = eval('0XC')
    is_visible: 'fctypes.c_uint8' = eval('0X10')
    collision_exist: 'fctypes.c_uint8' = eval('0X11')
    nav_mesh_disable: 'fctypes.c_uint8' = eval('0X12')


@set_fields_from_annotations
class SGOverriddenSE(SGOverriddenMember):
    auto_play: 'fctypes.c_uint8' = eval('0X8')


def sg_member_type(asset_type):
    if asset_type == AssetType.BG.value:
        return SGOverriddenBG  # .from_buffer(source, offset)
    if asset_type == AssetType.VFX.value:
        return SGOverriddenVFX  # .from_buffer(source, offset)
    if asset_type == AssetType.LayLight.value:
        return SGOverriddenLight  # .from_buffer(source, offset)
    if asset_type == AssetType.Sound.value:
        return SGOverriddenSE  # .from_buffer(source, offset)
    return SGOverriddenMember  # .from_buffer(source, offset)


@set_fields_from_annotations
class MovePathSettings(ctypes.Structure):
    class Mode(enum.Enum):
        Null = 0X0
        SGAction = 0X1
        Timeline = 0X2

    class RotationType(enum.Enum):
        NoRotate = 0X0
        AllAxis = 0X1
        YAxisOnly = 0X2

    mode: 'fctypes.c_int32' = eval('0X0')
    auto_play: 'fctypes.c_int8' = eval('0X4')
    time: 'fctypes.c_uint16' = eval('0X6')
    loop: 'fctypes.c_int8' = eval('0X8')
    reverse: 'fctypes.c_int8' = eval('0X9')
    rotation: 'fctypes.c_int32' = eval('0XC')
    accelerate_time: 'fctypes.c_uint16' = eval('0X10')
    decelerate_time: 'fctypes.c_uint16' = eval('0X12')
    vertical_swing_range: 'fctypes.array(fctypes.c_float, 2)' = eval('0X14')
    horizontal_swing_range: 'fctypes.array(fctypes.c_float, 2)' = eval('0X1C')
    swing_move_speed_range: 'fctypes.array(fctypes.c_float, 2)' = eval('0X24')
    swing_rotation: 'fctypes.array(fctypes.c_float, 2)' = eval('0X2C')
    swing_rotation_speed_range: 'fctypes.array(fctypes.c_float, 2)' = eval('0X34')

    @property
    def e_mode(self):
        return self.Mode(self.mode)

    @property
    def e_rotation(self):
        return self.RotationType(self.rotation)


@set_fields_from_annotations
class SGInstanceObject(InstanceObject):
    class ColorState(enum.Enum):
        Play = 0X0
        Stop = 0X1
        Replay = 0X2
        Reset = 0X3

    class TransformState(enum.Enum):
        Play = 0X0
        Stop = 0X1
        Replay = 0X2
        Reset = 0X3

    class RotationState(enum.Enum):
        Rounding = 0X1
        Stopped = 0X2

    class DoorState(enum.Enum):
        Auto = 0X1
        Open = 0X2
        Closed = 0X3

    _asset_path: 'fctypes.c_int32' = eval('0X30')
    initial_door_state: 'fctypes.c_int32' = eval('0X34')
    _overridden_members: 'fctypes.c_int32' = eval('0X38')
    overridden_member_count: 'fctypes.c_int32' = eval('0X3C')
    initial_rotation_state: 'fctypes.c_int32' = eval('0X40')
    random_timeline_auto_play: 'fctypes.c_int8' = eval('0X44')
    random_timeline_loop_playback: 'fctypes.c_int8' = eval('0X45')
    is_collision_controllable_without_e_obj: 'fctypes.c_int8' = eval('0X46')
    disable_error_check: 'fctypes.c_int8' = eval('0X47')
    bound_client_path_instance_id: 'fctypes.c_uint32' = eval('0X48')
    _move_path_settings: 'fctypes.c_int32' = eval('0X4C')
    not_create_nav_mesh_door: 'fctypes.c_int8' = eval('0X50')
    initial_transform_state: 'fctypes.c_int32' = eval('0X54')
    initial_color_state: 'fctypes.c_int32' = eval('0X58')

    @property
    def e_initial_door_state(self):
        return self.DoorState(self.initial_door_state)

    @property
    def e_initial_rotation_state(self):
        return self.RotationState(self.initial_rotation_state)

    @property
    def e_initial_transform_state(self):
        return self.TransformState(self.initial_transform_state)

    @property
    def e_initial_color_state(self):
        return self.ColorState(self.initial_color_state)

    asset_path = offset_string('_asset_path')

    @functools.cached_property
    def overridden_members(self) -> list[SGOverriddenMember]:
        p_offset = ctypes.addressof(self) + self._overridden_members
        return [
            sg_member_type(ctypes.c_int32.from_address(a := p_offset + o).value).from_address(a)
            for o in (ctypes.c_int32 * self.overridden_member_count).from_address(p_offset)
        ]

    @property
    def move_path_settings(self):
        return MovePathSettings.from_address(ctypes.addressof(self) + self._move_path_settings)
