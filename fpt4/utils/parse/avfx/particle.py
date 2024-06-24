from .types import *

ParticleDataMap = {
    ParticleVarietyType.Line.value: ('line_data', LineParticle),
    ParticleVarietyType.Powder.value: ('powder_data', PowderParticle),
    ParticleVarietyType.Windmill.value: ('windmill_data', WindmillParticle),
    ParticleVarietyType.Laser.value: ('laser_data', LaserParticle),
    ParticleVarietyType.Model.value: ('model_data', ModelParticle),
    ParticleVarietyType.LightModel.value: ('light_model_data', LightModelParticle),
    ParticleVarietyType.PolyLine.value: ('poly_line_data', PolyLineParticle),
    ParticleVarietyType.Quad.value: ('quad_data', QuadParticle),
    ParticleVarietyType.Polygon.value: ('polygon_data', PolygonParticle),
    ParticleVarietyType.Decal.value: ('decal_data', DecalParticle),
    ParticleVarietyType.DecalRing.value: ('decal_ring_data', DecalRingParticle),
    ParticleVarietyType.Disc.value: ('disc_data', DiscParticle),
}


class ParticleData:
    def __set_name__(self, owner, name):
        owner._attr_list.append(name)

        def load(instance, buf, off, size):
            _t = getattr(instance, '_particle_variety_type')
            if _t in ParticleDataMap:
                a, t = ParticleDataMap[_t]
                setattr(instance, a, t.load(buf, off, size))
            else:
                raise ValueError(f'Unknown type {_t}')

        def pack(instance):
            _t = getattr(instance, '_particle_variety_type')
            if _t in ParticleDataMap:
                a, t = ParticleDataMap[_t]
                if (v := getattr(instance, a)) is not None:
                    yield pack_binary_header(b'Data', t.pack(v))

        owner._guid_map[b'Data'] = type('ParticleData', (), {'load': load, 'pack': pack, 'guid': b'Data'})
        owner._attr_list.extend(n for n, _ in ParticleDataMap.values())


class Particle(AVfxStruct):
    loop_point_start = KeyAttr.simple(b'LpSt', 0, s_int16)
    loop_point_goal = KeyAttr.simple(b'LpEd', 0, s_int16)
    _particle_variety_type = KeyAttr.simple(b'PrVT', 0, s_int8)
    _rotation_base_direction_type = KeyAttr.simple(b'RBDT', 0, s_int8)
    _rotation_order_type = KeyAttr.simple(b'RoOT', 0, s_int8)
    _coordinate_compute_order_type = KeyAttr.simple(b'CCOT', 0, s_int8)
    _draw_mode_type = KeyAttr.simple(b'RMT', 0, s_int8)
    _culling_type = KeyAttr.simple(b'CulT', 0, s_int8)
    _env_light_type = KeyAttr.simple(b'EnvT', 0, s_int8)
    _dir_light_type = KeyAttr.simple(b'DirT', 0, s_int8)
    _uv_precision_type = KeyAttr.simple(b'UVPT', 0, s_int8)
    _depth_offset_type = KeyAttr.simple(b'DOTy', 0, s_int8)

    particle_variety_type = enum_property(ParticleVarietyType, '_particle_variety_type')
    rotation_base_direction_type = enum_property(RotationBaseDirectionType, '_rotation_base_direction_type')
    rotation_order_type = enum_property(RotationOrderType, '_rotation_order_type')
    coordinate_compute_order_type = enum_property(CoordinateComputeOrderType, '_coordinate_compute_order_type')
    draw_mode_type = enum_property(DrawModeType, '_draw_mode_type')
    culling_type = enum_property(CullingType, '_culling_type')
    env_light_type = enum_property(EnvLightType, '_env_light_type')
    dir_light_type = enum_property(DirLightType, '_dir_light_type')
    uv_precision_type = enum_property(UvPrecisionType, '_uv_precision_type')
    depth_offset_type = enum_property(DepthOffsetType, '_depth_offset_type')

    draw_priority = KeyAttr.simple(b'DwPr', 0, s_int8)
    is_depth_test = KeyAttr.simple(b'DsDt', 0, s_int8)
    is_depth_write = KeyAttr.simple(b'DsDw', 0, s_int8)
    is_soft_particle = KeyAttr.simple(b'DsSp', 0, s_int8)
    is_apply_tone_map = KeyAttr.simple(b'bATM', 0, s_int8)
    is_apply_fog = KeyAttr.simple(b'bAFg', 0, s_int8)
    collision_type = KeyAttr.simple(b'Coll', 0, s_int8)
    skip_direct_x11 = KeyAttr.simple(b'bS11', 0, s_int8)
    clip_is_near = KeyAttr.simple(b'bNea', 0, s_int8)
    clip_is_far = KeyAttr.simple(b'bFar', 0, s_int8)
    clip_near_start = KeyAttr.simple(b'NeSt', 0, s_float)
    clip_near_end = KeyAttr.simple(b'NeEd', 0, s_float)
    clip_far_start = KeyAttr.simple(b'FaSt', 0, s_float)
    clip_far_end = KeyAttr.simple(b'FaEd', 0, s_float)
    clip_base_point = KeyAttr.simple(b'FaBP', 0, s_int8)
    depth_offset = KeyAttr.simple(b'DpOf', 0, s_float)
    texture_uv_set_list = KeyListAttr.struct(b'UvSN', b'UvSt', TextureUvSet)
    environment_apply_rate = KeyAttr.simple(b'EvAR', 0, s_int8)
    directional_light_apply_rate = KeyAttr.simple(b'DlAR', 0, s_int8)
    light_buffer_apply_rate = KeyAttr.simple(b'LBAR', 0, s_int8)  # LAAR????
    is_simple_control = KeyAttr.simple(b'bSCt', 0, s_int8)
    life = KeyAttr.struct(b'Life', Value)
    simple_parameter = KeyAttr.struct(b'Smpl', SimpleParameters)

    gravity = ValueFunctionCurveAttr.make(b'Gra', b'GraR')
    air_resistance = ValueFunctionCurveAttr.make(b'ARs', b'ARsR')
    color = KeyAttr.struct(b'Col', ColorFunctionCurve)
    # position = KeyAttr.make(b'Pos', dumb_loader, dumb_packer, b'')
    position = KeyAttr.struct(b'Pos', Axis3Parameter)
    # rotation = KeyAttr.make(b'Rot', dumb_loader, dumb_packer, b'')
    rotation = KeyAttr.struct(b'Rot', Axis3Parameter)
    # scale = KeyAttr.make(b'Scl', dumb_loader, dumb_packer, b'')
    scale = KeyAttr.struct(b'Scl', Axis3Parameter)

    velocity_rotation_x = ValueFunctionCurveAttr.make(b'VRX', b'VRXR')
    velocity_rotation_y = ValueFunctionCurveAttr.make(b'VRY', b'VRYR')
    velocity_rotation_z = ValueFunctionCurveAttr.make(b'VRZ', b'VRZR')

    texture_property_color1 = KeyAttr.struct(b'TC1', TextureProperty_Color1)
    texture_property_color2 = KeyAttr.struct(b'TC2', TextureProperty_Color2)
    texture_property_color3 = KeyAttr.struct(b'TC3', TextureProperty_Color2)
    texture_property_color4 = KeyAttr.struct(b'TC4', TextureProperty_Color2)
    texture_property_normal = KeyAttr.struct(b'TN', TextureProperty_Normal)
    texture_property_reflection = KeyAttr.struct(b'TR', TextureProperty_Reflection)
    texture_property_distortion = KeyAttr.struct(b'TD', TextureProperty_Distortion)
    texture_property_alette = KeyAttr.struct(b'TP', TextureProperty_Palette)

    # data = KeyAttr.make(b'Data', dumb_loader, dumb_packer, b'')
    data = ParticleData()
    line_data: LineParticle = None
    powder_data: PowderParticle = None
    windmill_data: WindmillParticle = None
    laser_data: LaserParticle = None
    model_data: ModelParticle = None
    light_model_data: LightModelParticle = None
    poly_line_data: PolyLineParticle = None
    quad_data: QuadParticle = None
    polygon_data: PolygonParticle = None
    decal_data: DecalParticle = None
    decal_ring_data: DecalRingParticle = None
    disc_data: DiscParticle = None
