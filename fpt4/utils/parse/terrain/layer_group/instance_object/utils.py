import ctypes
import enum
import functools
import typing

from glm import vec3, make_vec3

from nylib.struct import set_fields_from_annotations, fctypes
from ..utils import AssetType
from ...utils import offset_string, Color, ColorHDRI

float_p = ctypes.POINTER(ctypes.c_float)


class TriggerBoxShape(enum.Enum):
    Box = 0X1
    Sphere = 0X2
    Cylinder = 0X3
    Board = 0X4
    Mesh = 0X5
    BoardBothSides = 0X6


class Transformation(typing.NamedTuple):
    translation: vec3
    rotation: vec3
    scale: vec3

    @classmethod
    def from_ctypes(cls, src: 'fctypes.array(fctypes.array(fctypes.c_float,3),3)'):
        return cls(
            make_vec3(ctypes.cast(src[0], float_p)),
            make_vec3(ctypes.cast(src[1], float_p)),
            make_vec3(ctypes.cast(src[2], float_p)),
        )


@set_fields_from_annotations
class RelativePositions(ctypes.Structure):
    _size_ = 0X8
    _pos: 'fctypes.c_int32' = eval('0X0')
    pos_count: 'fctypes.c_int32' = eval('0X4')

    @functools.cached_property
    def pos(self):
        return (ctypes.c_uint8 * self.pos_count).from_address(ctypes.addressof(self) + self._pos)


@set_fields_from_annotations
class InstanceObject(ctypes.Structure):
    asset_type: 'fctypes.c_int32' = eval('0X0')
    instance_id: 'fctypes.c_uint32' = eval('0X4')
    _name: 'fctypes.c_int32' = eval('0X8')
    _transformation: 'fctypes.array(fctypes.array(fctypes.c_float,3),3)' = eval('0XC')

    @property
    def e_asset_type(self):
        return AssetType(self.asset_type)

    name = offset_string('_name')

    @functools.cached_property
    def transformation(self):
        return Transformation.from_ctypes(self._transformation)

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.instance_id}, asset_type={self.e_asset_type.name}, name={self.name})'
