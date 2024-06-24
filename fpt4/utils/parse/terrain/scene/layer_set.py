import ctypes
import functools

from nylib.struct import set_fields_from_annotations, fctypes
from ..utils import offset_string


@set_fields_from_annotations
class LayerReference(ctypes.Structure):
    _size_ = 0X8
    layer_id: 'fctypes.c_uint32' = eval('0X0')


@set_fields_from_annotations
class LayerSet(ctypes.Structure):
    _size_ = 0X1C
    _nav_mesh_asset_path: 'fctypes.c_int32' = eval('0X0')
    layer_set_id: 'fctypes.c_uint32' = eval('0X4')
    _layer_references: 'fctypes.c_int32' = eval('0X8')
    layer_reference_count: 'fctypes.c_int32' = eval('0XC')
    territory_type_id: 'fctypes.c_uint16' = eval('0X10')
    content_finder_condition_id: 'fctypes.c_uint16' = eval('0X12')
    _name: 'fctypes.c_int32' = eval('0X14')
    _nav_mesh_ex_asset_path: 'fctypes.c_int32' = eval('0X18')

    nav_mesh_asset_path = offset_string('_navi_mesh_asset_path')
    name = offset_string('_name')
    nav_mesh_ex_asset_path = offset_string('_nav_mesh_ex_asset_path')

    @functools.cached_property
    def layer_references(self):
        return fctypes.array(LayerReference, self.layer_reference_count).from_address(ctypes.addressof(self) + self._layer_references)


@set_fields_from_annotations
class LayerSetFolder(ctypes.Structure):
    _size_ = 0X8
    _layer_sets: 'fctypes.c_int32' = eval('0X0')
    layer_set_count: 'fctypes.c_int32' = eval('0X4')

    # @functools.cached_property
    @property
    def layer_sets(self):
        return fctypes.array(LayerSet, self.layer_set_count).from_address(ctypes.addressof(self) + self._layer_sets)
