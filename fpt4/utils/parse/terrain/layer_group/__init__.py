import ctypes
import functools
import logging
import typing

from nylib.struct import set_fields_from_annotations, fctypes
from .utils import AssetType
from .instance_object import get_instance_object_from_addr
from ..utils import find_binary_by_chunk_id, offset_string

if typing.TYPE_CHECKING:
    from fpt4.utils.sqpack import SqPack


@set_fields_from_annotations
class OBSetEnableReferenced(ctypes.Structure):
    _size_ = 0XC
    asset_type: 'fctypes.c_uint32' = eval('0X0')
    instance_id: 'fctypes.c_uint32' = eval('0X4')
    ob_set_enable: 'fctypes.c_int8' = eval('0X8')
    ob_set_emissive_enable: 'fctypes.c_int8' = eval('0X9')

    @property
    def e_asset_type(self):
        return AssetType(self.asset_type)


@set_fields_from_annotations
class OBSetReferenced(ctypes.Structure):
    # Common::DevEnv::Generated::OBSetReferenced
    _size_ = 0XC

    asset_type: 'fctypes.c_uint32' = eval('0X0')
    instance_id: 'fctypes.c_uint32' = eval('0X4')
    _ob_set_asset_path: 'fctypes.c_int32' = eval('0X8')

    @property
    def e_asset_type(self):
        return AssetType(self.asset_type)

    ob_set_asset_path = offset_string('_ob_set_asset_path')


@set_fields_from_annotations
class Layer(ctypes.Structure):
    _size_ = 0X34
    layer_id: 'fctypes.c_uint32' = eval('0X0')
    _name: 'fctypes.c_int32' = eval('0X4')
    _instance_objects: 'fctypes.c_int32' = eval('0X8')
    instance_object_count: 'fctypes.c_int32' = eval('0XC')
    tool_mode_visible: 'fctypes.c_int8' = eval('0X10')
    tool_mode_read_only: 'fctypes.c_int8' = eval('0X11')
    is_bush_layer: 'fctypes.c_int8' = eval('0X12')
    ps3_visible: 'fctypes.c_int8' = eval('0X13')
    layer_set_ref: 'fctypes.c_int32' = eval('0X14')
    festival_id: 'fctypes.c_uint16' = eval('0X18')
    festival_phase_id: 'fctypes.c_uint16' = eval('0X1A')
    is_temporary: 'fctypes.c_int8' = eval('0X1C')
    is_housing: 'fctypes.c_int8' = eval('0X1D')
    version_mask: 'fctypes.c_uint16' = eval('0X1E')
    housing_area_id: 'fctypes.c_uint8' = eval('0X20')
    reserved1: 'fctypes.c_uint8' = eval('0X21')
    reserved2: 'fctypes.c_uint16' = eval('0X22')
    _ob_set_referenced_list: 'fctypes.c_int32' = eval('0X24')
    ob_set_referenced_list_count: 'fctypes.c_int32' = eval('0X28')
    _ob_set_enable_referenced_list: 'fctypes.c_int32' = eval('0X2C')
    ob_set_enable_referenced_list_count: 'fctypes.c_int32' = eval('0X30')

    name = offset_string('_name')

    @functools.cached_property
    def instance_objects(self):
        p_offset = ctypes.addressof(self) + self._instance_objects
        return [
            get_instance_object_from_addr(p_offset + o)
            for o in (ctypes.c_int32 * self.instance_object_count).from_address(p_offset)
        ]

    @functools.cached_property
    def ob_set_referenced_list(self):
        return fctypes.array(OBSetReferenced, self.ob_set_referenced_list_count).from_address(
            ctypes.addressof(self) + self._ob_set_referenced_list
        )

    @functools.cached_property
    def ob_set_enable_referenced_list(self):
        return fctypes.array(OBSetReferenced, self.ob_set_enable_referenced_list_count).from_address(
            ctypes.addressof(self) + self._ob_set_enable_referenced_list
        )


@set_fields_from_annotations
class LayerGroup(ctypes.Structure):
    _size_ = 0X10
    layer_group_id: 'fctypes.c_uint32' = eval('0X0')
    _name: 'fctypes.c_int32' = eval('0X4')
    _layers: 'fctypes.c_int32' = eval('0X8')
    layer_count: 'fctypes.c_int32' = eval('0XC')

    name = offset_string('_name')
    path = None

    @classmethod
    def get(cls, sq_pack: 'SqPack', path) -> 'LayerGroup|None':
        if (c := getattr(sq_pack, '__cached_layer_group', None)) is None:
            setattr(sq_pack, '__cached_layer_group', c := {})
        if path not in c:
            try:
                buf = memoryview(sq_pack.pack.get_file(path).data_buffer)
            except FileNotFoundError:
                _logger.warning(f'file not found {path}')
                c[path] = res = None
            else:
                c[path] = res = cls.from_buffer(find_binary_by_chunk_id(buf, b'LGP1', b'LGB1'))
                res.path = path
            return res
        return c[path]

    @functools.cached_property
    def layers(self):
        p_offset = ctypes.addressof(self) + self._layers
        return [Layer.from_address(p_offset + o) for o in (ctypes.c_int32 * self.layer_count).from_address(p_offset)]

_logger = logging.getLogger('LayerGroup')
