import dataclasses
from .enum import *
from ..utils import *


@dataclasses.dataclass
class FunctionCurveKey(DataClassImpl):
    time: int
    function: int
    param_a: float
    param_b: float
    value: float
    struct = struct.Struct(b'2h3f')


@dataclasses.dataclass
class ColorFunctionCurveKey(DataClassImpl):
    time: int
    function: int
    r: float
    g: float
    b: float
    struct = struct.Struct(b'2h3f')


class FunctionCurve(AVfxStruct):
    # keys_cnt = KeyAttr.make(b'KeyC', dumb_loader, dumb_packer, b'')
    # keys = KeyAttr.make(b'Keys', dumb_loader, dumb_packer, b'')
    keys = KeyNativeList.make(b'KeyC', b'Keys', FunctionCurveKey.struct, FunctionCurveKey, s_int8)
    _random_type = KeyAttr.simple(b'RanT', 0, s_int8)
    random_type = enum_property(RandomType, '_random_type')
    behavior_prev = KeyAttr.simple(b'BvPr', 0, s_int8)
    behavior_post = KeyAttr.simple(b'BvPo', 0, s_int8)


class Value(AVfxStruct):
    _random_type = KeyAttr.simple(b'Type', 0, s_int8)
    random_type = enum_property(RandomType, '_random_type')
    parameter = KeyAttr.simple(b'Val', 0, s_float)
    parameter_random = KeyAttr.simple(b'ValR', 0, s_float)


class RgbFunctionCurve(AVfxStruct):
    behavior_prev = KeyAttr.simple(b'BvPr', 0, s_int8)
    behavior_post = KeyAttr.simple(b'BvPo', 0, s_int8)
    # keys_cnt = KeyAttr.make(b'KeyC', dumb_loader, dumb_packer, b'')
    # keys = KeyAttr.make(b'Keys', dumb_loader, dumb_packer, b'')
    keys = KeyNativeList.make(b'KeyC', b'Keys', ColorFunctionCurveKey.struct, ColorFunctionCurveKey, s_int8)


class ColorFunctionCurve(AVfxStruct):
    rgb = KeyAttr.struct(b'RGB', RgbFunctionCurve)
    a = KeyAttr.struct(b'A', FunctionCurve)
    r_scale = KeyAttr.struct(b'SclR', FunctionCurve)
    g_scale = KeyAttr.struct(b'SclG', FunctionCurve)
    b_scale = KeyAttr.struct(b'SclB', FunctionCurve)
    a_scale = KeyAttr.struct(b'SclA', FunctionCurve)
    brightness = KeyAttr.struct(b'Bri', FunctionCurve)
    r_random = KeyAttr.struct(b'RanR', FunctionCurve)
    g_random = KeyAttr.struct(b'RanG', FunctionCurve)
    b_random = KeyAttr.struct(b'RanB', FunctionCurve)
    a_random = KeyAttr.struct(b'RanA', FunctionCurve)
    brightness_random = KeyAttr.struct(b'RBri', FunctionCurve)


class ValueFunctionCurve:
    curve: FunctionCurve = None
    random_curve: FunctionCurve = None

    def _dif_(self, other):
        if type(other) != ValueFunctionCurve:
            yield '_type_', self.__class__, type(other)
            return
        for p, v1, v2 in dif(self.curve, other.curve):
            yield concat_path('curve', p), v1, v2
        for p, v1, v2 in dif(self.random_curve, other.random_curve):
            yield concat_path('random_curve', p), v1, v2

    def _serialize_(self):
        return {'curve': serialize(self.curve), 'random_curve': serialize(self.random_curve)}


class ValueFunctionCurveAttr:
    name = None

    @classmethod
    def make(cls, c_key, r_key) -> ValueFunctionCurve:
        return cls(c_key, r_key)

    def __init__(self, c_key, r_key):
        self.c_key = c_key
        self.r_key = r_key

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return None

    def __set_name__(self, owner, name):
        self.name = name

        def load_c(i, b, o, s):
            if name not in i.__dict__:
                setattr(i, name, ValueFunctionCurve())
            getattr(i, name).curve = FunctionCurve.load(b, o, s)

        def pack_c(i):
            if (c := getattr(i, name)) and c.curve:
                yield pack_binary_header(self.c_key, FunctionCurve.pack(c.curve))

        def load_r(i, b, o, s):
            if name not in i.__dict__: setattr(i, name, ValueFunctionCurve())
            getattr(i, name).random_curve = FunctionCurve.load(b, o, s)

        def pack_r(i):
            if (c := getattr(i, name)) and c.random_curve:
                yield pack_binary_header(self.r_key, FunctionCurve.pack(c.random_curve))

        owner._attr_list.append(name)
        owner._guid_map[self.c_key] = type(f'{name}_curve', (), {'load': load_c, 'pack': pack_c, 'guid': self.c_key})
        owner._guid_map[self.r_key] = type(f'{name}_random_curve', (), {'load': load_r, 'pack': pack_r, 'guid': self.r_key})


class CreateItem(AVfxStruct):
    is_enable = KeyAttr.bool(b'bEnb', False, s_int32)
    target_no = KeyAttr.simple(b'TgtB', 0, s_int32)
    create_timing = KeyAttr.simple(b'CrTm', 0, s_int32)
    create_count = KeyAttr.simple(b'CrCn', 0, s_int32)
    create_probability = KeyAttr.simple(b'CrPr', 0, s_int32)
    parameter_link = KeyAttr.simple(b'PrLk', 0, s_int32)
    by_injection_angle_x = KeyAttr.simple(b'BIAX', 0, s_float)
    by_injection_angle_Y = KeyAttr.simple(b'BIAY', 0, s_float)
    by_injection_angle_Z = KeyAttr.simple(b'BIAZ', 0, s_float)
    generate_delay = KeyAttr.simple(b'GenD', 0, s_int32)
    is_generate_delay_by_one = KeyAttr.bool(b'bGD', False, s_int32)
    influence__local_direction = KeyAttr.simple(b'LoDr', 0, s_int32)
    influence_parent_coord = KeyAttr.simple(b'PICd', 0, s_int32)
    influence_parent_color = KeyAttr.simple(b'PICo', 0, s_int32)
    influence_coord_is_scale = KeyAttr.bool(b'ICbS', False, s_int32)
    influence_coord_is_rotation = KeyAttr.bool(b'ICbR', False, s_int32)
    influence_coord_is_position = KeyAttr.bool(b'ICbP', False, s_int32)
    influence_coord_is_binder_rotation = KeyAttr.bool(b'ICbB', False, s_int32)
    influence_coord_unstickiness = KeyAttr.simple(b'ICSK', 0, s_float)
    influence_inherit_parent_is_velocity = KeyAttr.bool(b'IPbV', False, s_int32)
    influence_inherit_parent_is_life = KeyAttr.bool(b'IPbL', False, s_int32)
    influence_is_override_life = KeyAttr.bool(b'bOvr', False, s_int32)
    influence_override_life_value = KeyAttr.simple(b'OvrV', 0, s_int32)
    influence_override_life_random = KeyAttr.simple(b'OvrR', 0, s_int32)
    influence_start_frame = KeyAttr.simple(b'StFr', 0, s_int32)
    influence_start_frame_is_null_update = KeyAttr.bool(b'bStN', False, s_int32)


class Axis3Parameter(AVfxStruct):
    _connect_type = KeyAttr.simple(b'ACT', 0, s_int8)
    _connect_type_random = KeyAttr.simple(b'ACTR', 0, s_int8)
    connect_type = enum_property(Axis3ConnectType, '_connect_type')
    connect_type_random = enum_property(Axis3ConnectType, '_connect_type_random')
    x = KeyAttr.struct(b'X', FunctionCurve)
    y = KeyAttr.struct(b'Y', FunctionCurve)
    z = KeyAttr.struct(b'Z', FunctionCurve)
    x_random = KeyAttr.struct(b'XR', FunctionCurve)
    y_random = KeyAttr.struct(b'YR', FunctionCurve)
    z_random = KeyAttr.struct(b'ZR', FunctionCurve)


class Axis2Parameter(AVfxStruct):
    _connect_type = KeyAttr.simple(b'ACT', 0, s_int8)
    _connect_type_random = KeyAttr.simple(b'ACTR', 0, s_int8)
    connect_type = enum_property(Axis2ConnectType, '_connect_type')
    connect_type_random = enum_property(Axis2ConnectType, '_connect_type_random')
    x = KeyAttr.struct(b'X', FunctionCurve)
    y = KeyAttr.struct(b'Y', FunctionCurve)
    x_random = KeyAttr.struct(b'XR', FunctionCurve)
    y_random = KeyAttr.struct(b'YR', FunctionCurve)


class TextureUvSet(AVfxStruct):
    _texture_calculate_uv_type = KeyAttr.simple(b'CUvT', 0, s_int8)
    texture_calculate_uv_type = enum_property(TextureCalculateUvType, '_texture_calculate_uv_type')
    scale = KeyAttr.struct(b'Scl', Axis2Parameter)
    scroll = KeyAttr.struct(b'Scr', Axis2Parameter)
    rotation = ValueFunctionCurveAttr.make(b'Rot', b'RotR')


class TextureProperty_Color1(AVfxStruct):
    is_enable = KeyAttr.simple(b'bEna', 0, s_int8)
    is_use_screen_copy = KeyAttr.simple(b'bUSC', 0, s_int8)
    is_color_to_alpha = KeyAttr.simple(b'bC2A', 0, s_int8)
    is_prev_frame_screen_copy = KeyAttr.simple(b'bPFC', 0, s_int8)
    uv_set_no = KeyAttr.simple(b'UvSN', 0, s_int8)

    _texture_filter_type = KeyAttr.simple(b'TFT', 0, s_int8)
    _texture_border_u_type = KeyAttr.simple(b'TBUT', 0, s_int8)
    _texture_border_v_type = KeyAttr.simple(b'TBVT', 0, s_int8)
    _texture_calculate_color_type = KeyAttr.simple(b'TCCT', 0, s_int8)
    _texture_calculate_alpha_type = KeyAttr.simple(b'TCAT', 0, s_int8)

    texture_filter_type = enum_property(TextureFilterType, '_texture_filter_type')
    texture_border_u_type = enum_property(TextureBorderType, '_texture_border_u_type')
    texture_border_v_type = enum_property(TextureBorderType, '_texture_border_v_type')
    texture_calculate_color_type = enum_property(TextureCalculateColorType, '_texture_calculate_color_type')
    texture_calculate_alpha_type = enum_property(TextureCalculateAlphaType, '_texture_calculate_alpha_type')
    texture_no = ValueFunctionCurveAttr.make(b'TxN', b'TxNR')

    # TODO: b'TLst'
    t_list = KeyAttr.make(b'TLst', dumb_loader, dumb_packer, b'')


class TextureProperty_Color2(AVfxStruct):
    texture_no = KeyAttr.simple(b'TxNo', 0, s_int8)
    is_enable = KeyAttr.simple(b'bEna', 0, s_int8)
    is_use_screen_copy = KeyAttr.simple(b'bUSC', 0, s_int8)
    is_color_to_alpha = KeyAttr.simple(b'bC2A', 0, s_int8)
    is_prev_frame_screen_copy = KeyAttr.simple(b'bPFC', 0, s_int8)
    uv_set_no = KeyAttr.simple(b'UvSN', 0, s_int8)

    _texture_filter_type = KeyAttr.simple(b'TFT', 0, s_int8)
    _texture_border_u_type = KeyAttr.simple(b'TBUT', 0, s_int8)
    _texture_border_v_type = KeyAttr.simple(b'TBVT', 0, s_int8)
    _texture_calculate_color_type = KeyAttr.simple(b'TCCT', 0, s_int8)
    _texture_calculate_alpha_type = KeyAttr.simple(b'TCAT', 0, s_int8)

    texture_filter_type = enum_property(TextureFilterType, '_texture_filter_type')
    texture_border_u_type = enum_property(TextureBorderType, '_texture_border_u_type')
    texture_border_v_type = enum_property(TextureBorderType, '_texture_border_v_type')
    texture_calculate_color_type = enum_property(TextureCalculateColorType, '_texture_calculate_color_type')
    texture_calculate_alpha_type = enum_property(TextureCalculateAlphaType, '_texture_calculate_alpha_type')


class TextureProperty_Normal(AVfxStruct):
    texture_no = KeyAttr.simple(b'TxNo', 0, s_int8)
    is_enable = KeyAttr.simple(b'bEna', 0, s_int8)
    uv_set_no = KeyAttr.simple(b'UvSN', 0, s_int8)
    normal_power = KeyAttr.struct(b'NPow', FunctionCurve)

    _texture_filter_type = KeyAttr.simple(b'TFT', 0, s_int8)
    _texture_border_u_type = KeyAttr.simple(b'TBUT', 0, s_int8)
    _texture_border_v_type = KeyAttr.simple(b'TBVT', 0, s_int8)

    texture_filter_type = enum_property(TextureFilterType, '_texture_filter_type')
    texture_border_u_type = enum_property(TextureBorderType, '_texture_border_u_type')
    texture_border_v_type = enum_property(TextureBorderType, '_texture_border_v_type')


class TextureProperty_Reflection(AVfxStruct):
    texture_no = KeyAttr.simple(b'TxNo', 0, s_int8)
    is_enable = KeyAttr.simple(b'bEna', 0, s_int8)
    is_use_screen_copy = KeyAttr.simple(b'bUSC', 0, s_int8)
    reflection_rate = KeyAttr.struct(b'Rate', FunctionCurve)

    _texture_filter_type = KeyAttr.simple(b'TFT', 0, s_int8)
    _texture_calculate_color_type = KeyAttr.simple(b'TCCT', 0, s_int8)

    texture_filter_type = enum_property(TextureFilterType, '_texture_filter_type')
    texture_calculate_color_type = enum_property(TextureCalculateColorType, '_texture_calculate_color_type')


class TextureProperty_Distortion(AVfxStruct):
    texture_no = KeyAttr.simple(b'TxNo', 0, s_int8)
    is_enable = KeyAttr.simple(b'bEna', 0, s_int8)
    is_target_uv1 = KeyAttr.simple(b'bT1', 0, s_int8)
    is_target_uv2 = KeyAttr.simple(b'bT2', 0, s_int8)
    is_target_uv3 = KeyAttr.simple(b'bT3', 0, s_int8)
    is_target_uv4 = KeyAttr.simple(b'bT4', 0, s_int8)
    uv_set_no = KeyAttr.simple(b'UvSN', 0, s_int8)
    distortion_power = KeyAttr.struct(b'DPow', FunctionCurve)

    _texture_filter_type = KeyAttr.simple(b'TFT', 0, s_int8)
    _texture_border_u_type = KeyAttr.simple(b'TBUT', 0, s_int8)
    _texture_border_v_type = KeyAttr.simple(b'TBVT', 0, s_int8)

    texture_filter_type = enum_property(TextureFilterType, '_texture_filter_type')
    texture_border_u_type = enum_property(TextureBorderType, '_texture_border_u_type')
    texture_border_v_type = enum_property(TextureBorderType, '_texture_border_v_type')


class TextureProperty_Palette(AVfxStruct):
    texture_no = KeyAttr.simple(b'TxNo', 0, s_int8)
    is_enable = KeyAttr.simple(b'bEna', 0, s_int8)
    palette_offset = ValueFunctionCurveAttr.make(b'POff', b'POfR')

    _texture_filter_type = KeyAttr.simple(b'TFT', 0, s_int8)
    _texture_border_type = KeyAttr.simple(b'TBT', 0, s_int8)

    texture_filter_type = enum_property(TextureFilterType, '_texture_filter_type')
    texture_border_type = enum_property(TextureBorderType, '_texture_border_type')


class LineParticle(AVfxStruct):
    _line_create_type = KeyAttr.simple(b'LnCT', 0, s_int8)
    line_create_type = enum_property(LineCreateType, '_line_create_type')
    length = ValueFunctionCurveAttr.make(b'Len', b'LenR')
    color_begin = KeyAttr.struct(b'ColB', ColorFunctionCurve)
    color_end = KeyAttr.struct(b'ColE', ColorFunctionCurve)


class PowderParticle(AVfxStruct):
    is_lighting = KeyAttr.simple(b'bLgt', 0, s_int8)
    _directional_light_type = KeyAttr.simple(b'LgtT', 0, s_int8)
    directional_light_type = enum_property(DirectionalLightType, '_directional_light_type')
    center_offset = KeyAttr.simple(b'CnOf', 0., s_float)


class WindmillParticle(AVfxStruct):
    _windmill_uv_type = KeyAttr.simple(b'WUvT', 0, s_int8)
    windmill_uv_type = enum_property(DirectionalLightType, '_windmill_uv_type')


class QuadParticle(AVfxStruct):
    scaling_scale = KeyAttr.simple(b'SS', 0, s_int32)


class PolygonParticle(AVfxStruct):
    count = ValueFunctionCurveAttr.make(b'Cnt', b'CntR')


class LaserParticle(AVfxStruct):
    length = ValueFunctionCurveAttr.make(b'Len', b'LenR')
    width = ValueFunctionCurveAttr.make(b'Wdt', b'WdtR')


class PolyLineParticle(AVfxStruct):
    _line_create_type = KeyAttr.simple(b'LnCT', 0, s_int8)
    _not_billboard_base_axis_type = KeyAttr.simple(b'NBBA', 0, s_int8)

    line_create_type = enum_property(LineCreateType, '_line_create_type')
    not_billboard_base_axis_type = enum_property(NotBillboardBaseAxisType, '_not_billboard_base_axis_type')

    tag = KeyAttr.simple(b'TagN', 0, s_uint32)
    bind_weapon_type = KeyAttr.simple(b'BWpT', 0, s_int8)
    point_count = KeyAttr.simple(b'PnC', 0, s_int8)
    point_count_center = KeyAttr.simple(b'PnCC', 0, s_int8)
    point_count_end_distortion = KeyAttr.simple(b'PnED', 0, s_int8)
    is_use_edge = KeyAttr.bool(b'bEdg', False, s_int8)
    is_not_billboard = KeyAttr.bool(b'bNtB', False, s_int8)
    is_bind_weapon = KeyAttr.bool(b'BdWp', False, s_int8)
    is_spline = KeyAttr.bool(b'bSpl', False, s_int8)
    is_local = KeyAttr.bool(b'bLcl', False, s_int8)
    is_connect_target = KeyAttr.bool(b'bCtg', False, s_int8)
    is_connect_target_reverse = KeyAttr.bool(b'bCtr', False, s_int8)
    centrifugal_force = ValueFunctionCurveAttr.make(b'CF', b'CFR')
    length = ValueFunctionCurveAttr.make(b'Len', b'LenR')
    width = ValueFunctionCurveAttr.make(b'Wd', b'WdR')
    width_begin = ValueFunctionCurveAttr.make(b'WdB', b'WdBR')
    width_center = ValueFunctionCurveAttr.make(b'WdC', b'WdCR')
    width_end = ValueFunctionCurveAttr.make(b'WdE', b'WdER')
    softness = ValueFunctionCurveAttr.make(b'Sft', b'SftR')
    point_distortion = KeyAttr.struct(b'PnDs', FunctionCurve)
    color_begin = KeyAttr.struct(b'ColB', ColorFunctionCurve)
    color_center = KeyAttr.struct(b'ColC', ColorFunctionCurve)
    color_end = KeyAttr.struct(b'ColE', ColorFunctionCurve)
    color_edge_begin = KeyAttr.struct(b'CoEB', ColorFunctionCurve)
    color_edge_center = KeyAttr.struct(b'CoEC', ColorFunctionCurve)
    color_edge_end = KeyAttr.struct(b'CoEE', ColorFunctionCurve)


class ModelParticle(AVfxStruct):
    is_lighting = KeyAttr.simple(b'bLgt', 0, s_int8)
    is_morph = KeyAttr.simple(b'bShp', 0, s_int8)
    model_no_table = KeyAttr.make(b'MdNo', dumb_loader, dumb_packer, b'')
    model_no_rand_value = KeyAttr.simple(b'MNRv', 0, s_int32)
    model_no_rand_compute_interval = KeyAttr.simple(b'MNRi', 0, s_int32)

    _fresnel_type = KeyAttr.simple(b'FrsT', 0, s_int8)
    _directional_light_type = KeyAttr.simple(b'DLT', 0, s_int8)
    _point_light_type = KeyAttr.simple(b'PLT', 0, s_int8)
    _model_no_rand_type = KeyAttr.make(
        b'MNRt',
        lambda b, o, s: RandomType.Always_Plus_Minus.value + s_int32.unpack_from(b, o)[0],
        lambda v: s_int32.pack(v - RandomType.Always_Plus_Minus.value),
        0
    )

    fresnel_type = enum_property(FresnelType, '_fresnel_type')
    directional_light_type = enum_property(DirectionalLightType, '_directional_light_type')
    point_light_type = enum_property(PointLightType, '_point_light_type')
    model_no_rand_type = enum_property(RandomType, '_model_no_rand_type')

    no_animation = KeyAttr.struct(b'NoAn', FunctionCurve)
    morph_rate = KeyAttr.struct(b'Moph', FunctionCurve)
    color_begin = KeyAttr.struct(b'ColB', ColorFunctionCurve)
    color_end = KeyAttr.struct(b'ColE', ColorFunctionCurve)
    fresnel_rotation = KeyAttr.struct(b'FrRt', Axis3Parameter)
    fresnel = ValueFunctionCurveAttr.make(b'FrC', b'FrCR')


class LightModelParticle(AVfxStruct):
    model_no = KeyAttr.simple(b'MNO', 0, s_int8)


class DecalParticle(AVfxStruct):
    scaling_scale = KeyAttr.simple(b'SS', 0, s_float)


class DecalRingParticle(AVfxStruct):
    scaling_scale = KeyAttr.simple(b'SS', 0, s_float)
    ring_fan = KeyAttr.simple(b'RF', 0, s_float)
    width = ValueFunctionCurveAttr.make(b'WID', b'WIDR')


class DiscParticle(AVfxStruct):
    scaling_scale = KeyAttr.simple(b'SS', 0, s_int32)
    parts_count = KeyAttr.simple(b'PrtC', 0, s_uint8)
    parts_count_u = KeyAttr.simple(b'PCnU', 0, s_uint8)
    parts_count_v = KeyAttr.simple(b'PCnV', 0, s_uint8)
    point_interval_factor_v = KeyAttr.simple(b'PIFU', 0, s_float)
    angle = ValueFunctionCurveAttr.make(b'Ang', b'AngR')
    height_begin_inner = ValueFunctionCurveAttr.make(b'HBI', b'HBIR')
    height_end_inner = ValueFunctionCurveAttr.make(b'HEI', b'HEIR')
    height_begin_outer = ValueFunctionCurveAttr.make(b'HBO', b'HBOR')
    height_end_outer = ValueFunctionCurveAttr.make(b'HEO', b'HEOR')
    width_begin = ValueFunctionCurveAttr.make(b'WB', b'WBR')
    width_end = ValueFunctionCurveAttr.make(b'WE', b'WER')
    radius_begin = ValueFunctionCurveAttr.make(b'RB', b'RBR')
    radius_end = ValueFunctionCurveAttr.make(b'RE', b'RER')
    color_edge_inner = KeyAttr.struct(b'CEI', ColorFunctionCurve)
    color_edge_outer = KeyAttr.struct(b'CEO', ColorFunctionCurve)


class SimpleParameters(AVfxStruct):
    create_area_x = KeyAttr.simple(b'CrAX', 1., s_float)
    create_area_y = KeyAttr.simple(b'CrAY', 1., s_float)
    create_area_z = KeyAttr.simple(b'CrAZ', 1., s_float)
    coord_acc_x = KeyAttr.simple(b'CAX', 1., s_float)
    coord_acc_y = KeyAttr.simple(b'CAY', 1., s_float)
    coord_acc_z = KeyAttr.simple(b'CAZ', 1., s_float)
    coord_gra_x = KeyAttr.simple(b'CGX', 0, s_float)
    coord_gra_y = KeyAttr.simple(b'CGY', 0, s_float)
    coord_gra_z = KeyAttr.simple(b'CGZ', 0, s_float)
    scale_begin_x = KeyAttr.simple(b'SBX', .1, s_float)
    scale_begin_y = KeyAttr.simple(b'SBY', .1, s_float)
    scale_end_x = KeyAttr.simple(b'SEX', .1, s_float)
    scale_end_y = KeyAttr.simple(b'SEY', .1, s_float)
    scale_curve = KeyAttr.simple(b'SC', 1., s_float)
    scale_rand_x0 = KeyAttr.simple(b'SRX0', 1., s_float)
    scale_rand_x1 = KeyAttr.simple(b'SRX1', 1., s_float)
    scale_rand_y0 = KeyAttr.simple(b'SRY0', 1., s_float)
    scale_rand_y1 = KeyAttr.simple(b'SRY1', 1., s_float)
    rot_init_x = KeyAttr.simple(b'RIX', 0, s_float)
    rot_init_y = KeyAttr.simple(b'RIY', 0, s_float)
    rot_init_z = KeyAttr.simple(b'RIZ', 0, s_float)
    rot_add_x = KeyAttr.simple(b'RAX', 0, s_float)
    rot_add_y = KeyAttr.simple(b'RAY', 0, s_float)
    rot_add_z = KeyAttr.simple(b'RAZ', 0, s_float)
    rot_base_x = KeyAttr.simple(b'RBX', 0, s_float)
    rot_base_y = KeyAttr.simple(b'RBY', 0, s_float)
    rot_base_z = KeyAttr.simple(b'RBZ', 0, s_float)
    rot_vel_x = KeyAttr.simple(b'RVX', 0, s_float)
    rot_vel_y = KeyAttr.simple(b'RVY', 0, s_float)
    rot_vel_z = KeyAttr.simple(b'RVZ', 0, s_float)
    vel_min = KeyAttr.simple(b'VMin', 0, s_float)
    vel_max = KeyAttr.simple(b'VMax', 0, s_float)
    injection_radial_dir0 = KeyAttr.simple(b'IRD0', 0, s_float)
    injection_radial_dir1 = KeyAttr.simple(b'IRD1', 180, s_float)
    flattery_rate = KeyAttr.simple(b'FltR', 1., s_float)
    flattery_speed = KeyAttr.simple(b'FltS', .1, s_float)
    pivot_x = KeyAttr.simple(b'PvtX', 0, s_float)
    pivot_y = KeyAttr.simple(b'PvtY', 0, s_float)
    line_length_min = KeyAttr.simple(b'LLin', .1, s_float)
    line_length_max = KeyAttr.simple(b'LLax', .5, s_float)
    # TODO:color_frames, colors
    color_frames = KeyAttr.make(b'Frms', dumb_loader, dumb_packer, b'')
    colors = KeyAttr.make(b'Cols', dumb_loader, dumb_packer, b'')
    create_count = KeyAttr.simple(b'CCnt', 0, s_int32)
    create_interval_count = KeyAttr.simple(b'CrIC', 1, s_int32)
    create_interval_life = KeyAttr.simple(b'CrIL', -1, s_int32)
    block_num = KeyAttr.simple(b'BlkN', 1, s_int32)

    _injection_direction_type = KeyAttr.simple(b'SIPT', 0, s_int32)
    _injection_position_type = KeyAttr.simple(b'SIDT', 0, s_int32)
    _base_direction_type = KeyAttr.simple(b'SBDT', 0, s_int32)
    injection_direction_type = enum_property(SimpleInjectionDirectionType, '_injection_direction_type')
    injection_position_type = enum_property(SimpleInjectionPositionType, '_injection_position_type')
    base_direction_type = enum_property(SimpleBaseDirectionType, '_base_direction_type')

    uv_cell_u = KeyAttr.simple(b'UvCU', 1, s_int32)
    uv_cell_v = KeyAttr.simple(b'UvCV', 1, s_int32)
    uv_interval = KeyAttr.simple(b'UvIv', 1, s_int32)
    uv_no_random = KeyAttr.simple(b'UvNR', 0, s_int32)
    uv_no_loop_count = KeyAttr.simple(b'UvLC', 0, s_int32)
    injection_model_no = KeyAttr.simple(b'IJMN', -1, s_int32)
    vertex_bind_model_no = KeyAttr.simple(b'VBMN', -1, s_int32)
    create_interval = KeyAttr.simple(b'CrI', 0, s_int32)
    create_interval_random = KeyAttr.simple(b'CrIR', 0, s_int32)
    is_new_create_after_delete = KeyAttr.bool(b'bCrN', False, s_int32)
    is_uv_reverse = KeyAttr.bool(b'bRUV', False, s_int32)
    is_scale_random_link = KeyAttr.bool(b'bSRL', True, s_int32)
    is_bind_parent = KeyAttr.bool(b'bBnP', False, s_int32)
    is_scale_by_parent = KeyAttr.bool(b'bSnP', False, s_int32)
    poly_line_tag = KeyAttr.simple(b'PolT', 0, s_int32)
