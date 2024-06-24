import ctypes
import enum
from .utils import *


class ModelCollisionType(enum.Enum):
    Null = 0X0
    Replace = 0X1
    TYPE_Box = 0X2


@set_fields_from_annotations
class ModelCollisionConfig(ctypes.Structure):
    # Common::DevEnv::Generated::ModelCollisionConfig

    collision_attribute_mask: 'fctypes.c_uint32' = eval('0X0')
    collision_attribute: 'fctypes.c_uint32' = eval('0X4')
    collision_attribute2_mask: 'fctypes.c_uint32' = eval('0X8')
    collision_attribute2: 'fctypes.c_uint32' = eval('0XC')
    collision_box_shape: 'fctypes.c_uint32' = eval('0X10')
    _collision_box_transformation: 'fctypes.array(fctypes.array(fctypes.c_float,3),3)' = eval('0X14')
    aabb_min_x: 'fctypes.c_float' = eval('0X38')
    aabb_min_y: 'fctypes.c_float' = eval('0X3C')
    aabb_min_z: 'fctypes.c_float' = eval('0X40')
    aabb_max_x: 'fctypes.c_float' = eval('0X44')
    aabb_max_y: 'fctypes.c_float' = eval('0X48')
    aabb_max_z: 'fctypes.c_float' = eval('0X4C')

    @property
    def e_collision_box_shape(self):
        return TriggerBoxShape(self.collision_box_shape)

    @functools.cached_property
    def collision_box_transformation(self):
        return Transformation.from_ctypes(self._collision_box_transformation)


@set_fields_from_annotations
class BGInstanceObject(InstanceObject):
    _asset_path: 'fctypes.c_int32' = eval('0X30')
    _collision_asset_path: 'fctypes.c_int32' = eval('0X34')
    collision_type: 'fctypes.c_int32' = eval('0X38')
    attribute_mask: 'fctypes.c_uint32' = eval('0X3C')
    attribute: 'fctypes.c_uint32' = eval('0X40')
    attribute2_mask: 'fctypes.c_uint32' = eval('0X44')
    attribute2: 'fctypes.c_uint32' = eval('0X48')
    _collision_config: 'fctypes.c_int32' = eval('0X4C')
    is_visible: 'fctypes.c_int8' = eval('0X50')
    render_shadow_enabled: 'fctypes.c_uint8' = eval('0X51')
    render_light_shadow_enabled: 'fctypes.c_uint8' = eval('0X52')
    render_model_clip_range: 'fctypes.c_float' = eval('0X54')
    bounding_sphere_radius: 'fctypes.c_float' = eval('0X58')

    collision_asset_path = offset_string('_collision_asset_path')
    asset_path = offset_string('_asset_path')

    @property
    def e_collision_type(self):
        return ModelCollisionType(self.collision_type)

    @property
    def collision_config(self):
        return ModelCollisionConfig.from_address(ctypes.addressof(self) + self._collision_config)
