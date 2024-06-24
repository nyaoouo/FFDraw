from .scheduler import Scheduler
from .emitter import Emitter
from .particle import Particle
from .timeline import Timeline
from .binder import Binder
from .utils import *


class DrawLayerType(enum.Enum):
    Screen = 0X0
    BaseUpper = 0X1
    Base = 0X2
    BaseLower = 0X3
    InWater = 0X4
    BeforeCloud = 0X5
    BehindCloud = 0X6
    BeforeSky = 0X7
    PostUI = 0X8
    PrevUI = 0X9
    FitWater = 0XA
    Max = 0XB


class DrawOrderType(enum.Enum):
    Default = 0X0
    Reverse = 0X1
    Depth = 0X2
    Max = 0X3


class DirectionalLightSourceType(enum.Enum):
    Null = 0X0
    InLocal = 0X1
    InGame = 0X2
    Max = 0X3


class PointLightSourceType(enum.Enum):
    Null = 0X0
    CreateTimeBG = 0X1
    AlwaysBG = 0X2
    LocalVFX = 0X3
    GlobalVFX = 0X4
    Max = 0X5


class AVfx(AVfxStruct):
    version = KeyAttr.simple(b'Ver', 0, s_int32)
    is_delay_fast_particle = KeyAttr.bool(b'bDFP', False)
    is_fit_ground = KeyAttr.bool(b'bFG', False)
    is_transform_skip = KeyAttr.bool(b'bTS', False)
    is_all_stop_on_hide = KeyAttr.bool(b'bASH', False)
    can_be_clipped_out = KeyAttr.bool(b'bCBC', True)
    soft_particle_fade_range = KeyAttr.simple(b'SPFR', 0., s_float)
    sort_key_offset = KeyAttr.simple(b'SKO', 0., s_float)
    _draw_layer_type = KeyAttr.simple(b'DwLy', DrawLayerType.Base.value, s_int8)
    _draw_order_type = KeyAttr.simple(b'DwOT', 0, s_int8)
    _directional_light_source_type = KeyAttr.simple(b'DLST', 0, s_int8)
    _point_light1_source_type = KeyAttr.simple(b'PL1S', 0, s_int8)
    _point_light2_source_type = KeyAttr.simple(b'PL2S', 0, s_int8)

    draw_layer_type = enum_property(DrawLayerType, '_draw_layer_type')
    draw_order_type = enum_property(DrawOrderType, '_draw_order_type')
    directional_light_source_type = enum_property(DirectionalLightSourceType, '_directional_light_source_type')
    point_light1_source_type = enum_property(PointLightSourceType, '_point_light1_source_type')
    point_light2_source_type = enum_property(PointLightSourceType, '_point_light2_source_type')

    is_clip_own_setting = KeyAttr.simple(b'bOSt', 0, s_int8)
    near_clip_begin = KeyAttr.simple(b'NCB', 0., s_float)
    near_clip_end = KeyAttr.simple(b'NCE', 0., s_float)
    far_clip_begin = KeyAttr.simple(b'FCB', 0., s_float)
    far_clip_end = KeyAttr.simple(b'FCE', 0., s_float)

    cull_box_px = KeyAttr.simple(b'CBPx', 0., s_float)
    cull_box_py = KeyAttr.simple(b'CBPy', 0., s_float)
    cull_box_pz = KeyAttr.simple(b'CBPz', 0., s_float)
    cull_box_sx = KeyAttr.simple(b'CBSx', 0.5, s_float)
    cull_box_sy = KeyAttr.simple(b'CBSy', 0.5, s_float)
    cull_box_sz = KeyAttr.simple(b'CBSz', 0.5, s_float)

    z_bias_max_scale = KeyAttr.simple(b'ZBMs', 1., s_float)
    z_bias_max_distance = KeyAttr.simple(b'ZBMd', 0., s_float)

    is_camera_space = KeyAttr.bool(b'bCmS', False, s_int32)
    is_full_env_light = KeyAttr.bool(b'bFEL', False, s_int32)
    is_culling = KeyAttr.bool(b'bCul', False, s_int32)

    revised_px = KeyAttr.simple(b'RvPx', 0., s_float)
    revised_py = KeyAttr.simple(b'RvPy', 0., s_float)
    revised_pz = KeyAttr.simple(b'RvPz', 0., s_float)
    revised_rx = KeyAttr.simple(b'RvRx', 0., s_float)
    revised_ry = KeyAttr.simple(b'RvRy', 0., s_float)
    revised_rz = KeyAttr.simple(b'RvRz', 0., s_float)
    revised_sx = KeyAttr.simple(b'RvSx', 1., s_float)
    revised_sy = KeyAttr.simple(b'RvSy', 1., s_float)
    revised_sz = KeyAttr.simple(b'RvSz', 1., s_float)
    revised_r = KeyAttr.simple(b'RvR', 1., s_float)
    revised_g = KeyAttr.simple(b'RvG', 1., s_float)
    revised_b = KeyAttr.simple(b'RvB', 1., s_float)

    angle_fade_x_enable = KeyAttr.bool(b'AFXe', False, s_int32)
    angle_fade_y_enable = KeyAttr.bool(b'AFYe', False, s_int32)
    angle_fade_z_enable = KeyAttr.bool(b'AFZe', False, s_int32)
    angle_fade_x_inner = KeyAttr.simple(b'AFXi', 0., s_float)
    angle_fade_x_outer = KeyAttr.simple(b'AFXo', 0., s_float)
    angle_fade_y_inner = KeyAttr.simple(b'AFYi', 0., s_float)
    angle_fade_y_outer = KeyAttr.simple(b'AFYo', 0., s_float)
    angle_fade_z_inner = KeyAttr.simple(b'AFZi', 0., s_float)
    angle_fade_z_outer = KeyAttr.simple(b'AFZo', 0., s_float)

    global_fog_enable = KeyAttr.bool(b'bGFE', False, s_int32)
    fog_influence_modifier = KeyAttr.simple(b'GFIM', 1., s_float)

    last_trigger_switch = KeyAttr.bool(b'bLTS', False, s_int32)

    scheduler_list = KeyListAttr.struct(b'ScCn', b'Schd', Scheduler)
    timeline_list = KeyListAttr.struct(b'TlCn', b'TmLn', Timeline)
    emitter_list = KeyListAttr.struct(b'EmCn', b'Emit', Emitter)
    particle_list = KeyListAttr.struct(b'PrCn', b'Ptcl', Particle)
    effector_list = KeyListAttr.make(b'EfCn', b'Efct', dumb_loader, dumb_packer)
    binder_list = KeyListAttr.struct(b'BdCn', b'Bind',Binder)
    texture_list = KeyListAttr.make(b'TxCn', b'Tex', dumb_loader, dumb_packer)
    model_list = KeyListAttr.make(b'MdCn', b'Modl', dumb_loader, dumb_packer)

    @classmethod
    def load(cls, buf, offset=0, data_size=0) -> 'AVfx':
        header = binary_header(buf)
        assert header.guid == b'AVFX', 'header guid not match'
        assert header.size + BinaryHeaderStruct.size == len(buf), 'header size not match'
        return super().load(buf, BinaryHeaderStruct.size, header.size)

    def pack(self):
        return pack_binary_header(b'AVFX', super(AVfx, self).pack())
