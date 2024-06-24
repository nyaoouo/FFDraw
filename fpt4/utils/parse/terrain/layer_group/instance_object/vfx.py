from .utils import *


@set_fields_from_annotations
class VFXInstanceObject(InstanceObject):
    _asset_path: 'fctypes.c_int32' = eval('0X30')
    soft_particle_fade_range: 'fctypes.c_float' = eval('0X34')
    color: 'Color' = eval('0X3C')
    is_auto_play: 'fctypes.c_int8' = eval('0X40')
    is_no_far_clip: 'fctypes.c_int8' = eval('0X41')
    fade_near_start: 'fctypes.c_float' = eval('0X44')
    fade_near_end: 'fctypes.c_float' = eval('0X48')
    fade_far_start: 'fctypes.c_float' = eval('0X4C')
    fade_far_end: 'fctypes.c_float' = eval('0X50')
    z_correct: 'fctypes.c_float' = eval('0X54')
    asset_path = offset_string('_asset_path')
