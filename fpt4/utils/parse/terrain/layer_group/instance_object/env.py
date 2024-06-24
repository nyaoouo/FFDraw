import enum

from .utils import *


@set_fields_from_annotations
class EnvLocationInstanceObject(InstanceObject):
    _sh_ambient_light_asset_path: 'fctypes.c_int32' = eval('0X30')
    _env_map_asset_path: 'fctypes.c_int32' = eval('0X34')
    sh_ambient_light_asset_path = offset_string('_sh_ambient_light_asset_path')
    env_map_asset_path = offset_string('_env_map_asset_path')


@set_fields_from_annotations
class EnvSetInstanceObject(InstanceObject):
    class Shape(enum.Enum):
        Ellipsoid = 0X1
        Cuboid = 0X2
        Cylinder = 0X3

    _asset_path: 'fctypes.c_int32' = eval('0X30')
    bound_instance_id: 'fctypes.c_uint32' = eval('0X34')
    shape: 'fctypes.c_int32' = eval('0X38')
    is_env_map_shooting_point: 'fctypes.c_int8' = eval('0X3C')
    priority: 'fctypes.c_uint8' = eval('0X3D')
    effective_range: 'fctypes.c_float' = eval('0X40')
    interpolation_time: 'fctypes.c_int32' = eval('0X44')
    reverb: 'fctypes.c_float' = eval('0X48')
    filter: 'fctypes.c_float' = eval('0X4C')
    _sound_asset_path: 'fctypes.c_int32' = eval('0X50')

    asset_path = offset_string('_asset_path')
    sound_asset_path = offset_string('_sound_asset_path')

    @property
    def e_shape(self):
        return self.Shape(self.shape)
