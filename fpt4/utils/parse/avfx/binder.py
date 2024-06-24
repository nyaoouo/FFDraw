from .types import *


@auto_missing
class BinderRotationType(enum.Enum):
    Standard = 0X0
    Billboard = 0X1
    BillboardAxisY = 0X2
    LookAtCamera = 0X3
    CameraBillboardAxisY = 0X4


@auto_missing
class BinderVarietyType(enum.Enum):
    Point = 0X0
    Linear = 0X1
    Spline = 0X2
    Camera = 0X3


@auto_missing
class BindTargetPointType(enum.Enum):
    Origin = 0X0
    FitGround = 0X1
    DamageCircle = 0X2
    ByName = 0X3


@auto_missing
class BindPointType(enum.Enum):
    Caster = 0X0
    Target = 0X1


class BindPointProperty(AVfxStruct):
    name = KeyAttr.make(b'Name', dumb_loader, dumb_packer, b'')
    bind_point_id = KeyAttr.simple(b'BPID', 0, s_int8)
    _bind_point_type = KeyAttr.simple(b'BPT', 0, s_int8)
    bind_point_type = enum_property(BindPointType, '_bind_point_type')
    _bind_target_point_type = KeyAttr.simple(b'BPTP', 0, s_int8)
    bind_target_point_type = enum_property(BindTargetPointType, '_bind_target_point_type')
    generate_delay = KeyAttr.simple(b'GenD', 0, s_int8)
    coord_update_frame = KeyAttr.simple(b'CoUF', 0, s_int16)
    is_ring_enable = KeyAttr.simple(b'bRng', 0, s_int8)
    ring_progress_time = KeyAttr.simple(b'RnPT', 0, s_int16)
    ring_position_x = KeyAttr.simple(b'RnPX', 0., s_float)
    ring_position_y = KeyAttr.simple(b'RnPY', 0., s_float)
    ring_position_z = KeyAttr.simple(b'RnPZ', 0., s_float)
    ring_radius = KeyAttr.simple(b'RnRd', 0., s_float)
    position = KeyAttr.struct(b'Pos', Axis3Parameter)


class Binder(AVfxStruct):
    life = KeyAttr.simple(b'Life', 0, s_int16)
    is_start_to_goal_direction = KeyAttr.bool(b'bStG', False, s_int32)
    is_vfx_scale_enable = KeyAttr.bool(b'bVSc', False, s_int32)
    vfx_scale_bias = KeyAttr.simple(b'bVSb', 1., s_float)
    is_vfx_scale_depth_offset_enable = KeyAttr.bool(b'bVSd', False, s_int32)
    is_vfx_scale_interpolation_enable = KeyAttr.bool(b'bVSi', False, s_int32)
    is_transform_scale_enable = KeyAttr.bool(b'bTSc', False, s_int32)
    is_transform_scale_depth_offset_enable = KeyAttr.bool(b'bTSd', False, s_int32)
    is_transform_scale_interpolation_enable = KeyAttr.bool(b'bTSi', False, s_int32)
    is_following_target_orientation = KeyAttr.bool(b'bFTO', False, s_int32)
    is_document_scale_enable = KeyAttr.bool(b'bDSE', False, s_int32)
    is_adjust_to_screen_enable = KeyAttr.bool(b'bATS', False, s_int32)
    is_bias_exclusive_transform_scal = KeyAttr.bool(b'bBET', False, s_int32)
    _rotation_type = KeyAttr.simple(b'RoTp', 0, s_int8)
    rotation_type = enum_property(BinderRotationType, '_rotation_type')
    _binder_variety_type = KeyAttr.simple(b'BnVr', 0, s_int8)
    binder_variety_type = enum_property(BinderVarietyType, '_binder_variety_type')
    binder_property_point_start = KeyAttr.struct(b'PrpS', BindPointProperty)
    binder_property_point_relay1 = KeyAttr.struct(b'Prp1', BindPointProperty)
    binder_property_point_relay2 = KeyAttr.struct(b'Prp2', BindPointProperty)
    binder_property_point_goal = KeyAttr.struct(b'PrpG', BindPointProperty)
    data = KeyAttr.make(b'Data', dumb_loader, dumb_packer, b'')
