import ctypes
import functools
import logging
import typing

from nylib.struct import set_fields_from_annotations, fctypes
from .layer_set import LayerSetFolder
from .sg_timeline import SGTimelineFolder
from .sg_settings import SGSettings
from .housing_settings import HousingSettings
from ..layer_group import LayerGroup
from ..utils import find_binary_by_chunk_id, offset_string

if typing.TYPE_CHECKING:
    from fpt4.utils.sqpack import SqPack


@set_fields_from_annotations
class SceneSettings(ctypes.Structure):
    is_partial_output: 'fctypes.c_int8' = eval('0X0')
    contains_layer_set_ref: 'fctypes.c_int8' = eval('0X1')
    is_dungeon: 'fctypes.c_int8' = eval('0X2')
    exists_grass_data: 'fctypes.c_int8' = eval('0X3')
    _terrain_asset_path: 'fctypes.c_int32' = eval('0X4')
    env_set_attr_references: 'fctypes.c_int32' = eval('0X8')
    env_set_attr_reference__count: 'fctypes.c_int32' = eval('0XC')
    sunrise_angle: 'fctypes.c_int32' = eval('0X10')
    sky_visibility_path: 'fctypes.c_int32' = eval('0X14')
    camera_far_clip_distance: 'fctypes.c_float' = eval('0X18')
    main_light_orbit_curve: 'fctypes.c_float' = eval('0X1C')
    main_light_orbit_clamp: 'fctypes.c_float' = eval('0X20')
    shadow_far_distance: 'fctypes.c_float' = eval('0X24')
    shadow_distance_fade: 'fctypes.c_float' = eval('0X28')
    bg_sky_visibility: 'fctypes.c_float' = eval('0X2C')
    bg_material_color: 'fctypes.c_int32' = eval('0X30')
    light_clip_aabb_path: 'fctypes.c_int32' = eval('0X34')
    terrain_occlusion_rain_enabled: 'fctypes.c_int8' = eval('0X38')
    terrain_occlusion_dust_enabled: 'fctypes.c_int8' = eval('0X39')
    constant_time_mode_enabled: 'fctypes.c_int8' = eval('0X3A')
    constant_time: 'fctypes.c_float' = eval('0X3C')
    level_weather_table: 'fctypes.c_int32' = eval('0X40')
    sky_horizon: 'fctypes.c_float' = eval('0X44')
    waving_anime_time_scale: 'fctypes.c_float' = eval('0X48')
    is_underwater: 'fctypes.c_int8' = eval('0X4C')
    is_all_celestial_sphere: 'fctypes.c_int8' = eval('0X4D')
    shadow_distance_scale_in_flying: 'fctypes.c_float' = eval('0X50')
    terrain_asset_path = offset_string('_terrain_asset_path')


@set_fields_from_annotations
class Scene(ctypes.Structure):
    LV_SCENE = b'LVB1'
    SG_SCENE = b'SGB1'
    path = None

    @classmethod
    def lv_scene(cls, sq_pack: 'SqPack', territory_id: int):
        return cls.get(sq_pack, b'bg/%s.lvb' % sq_pack.sheets.territory_type_sheet[territory_id].lvb.encode(), cls.LV_SCENE)

    @classmethod
    def get(cls, sq_pack: 'SqPack', path, file_id: bytes) -> 'Scene|None':
        k = '__cached_scene_' + file_id.decode()
        if (c := getattr(sq_pack, k, None)) is None: setattr(sq_pack, k, c := {})
        if path not in c:
            try:
                buf = memoryview(sq_pack.pack.get_file(path).data_buffer)
            except FileNotFoundError:
                _logger.warning(f'file not found {path}')
                c[path] = res = None
            else:
                c[path] = res = cls.from_buffer(find_binary_by_chunk_id(buf, b'SCN1', file_id))
                res.path = path
            return res
        return c[path]

    _layer_groups: 'fctypes.c_int32' = eval('0X0')
    layer_group_count: 'fctypes.c_int32' = eval('0X4')
    _settings: 'fctypes.c_int32' = eval('0X8')
    _layer_set_folder: 'fctypes.c_int32' = eval('0XC')
    _sg_timeline_folder: 'fctypes.c_int32' = eval('0X10')
    _lgb_asset_paths: 'fctypes.c_int32' = eval('0X14')
    lgb_asset_path_count: 'fctypes.c_int32' = eval('0X18')
    sg_door_settings: 'fctypes.c_int32' = eval('0X1C')
    _sg_settings: 'fctypes.c_int32' = eval('0X20')
    sg_rotation_settings: 'fctypes.c_int32' = eval('0X24')
    sg_random_timeline_settings: 'fctypes.c_int32' = eval('0X28')
    _housing_settings: 'fctypes.c_int32' = eval('0X2C')
    sg_clock_settings: 'fctypes.c_int32' = eval('0X30')

    @functools.cached_property
    def setting(self):
        return SceneSettings.from_address(ctypes.addressof(self) + self._settings)

    @functools.cached_property
    def lgb_asset_paths(self):
        p_offset = ctypes.addressof(self) + self._lgb_asset_paths
        return [ctypes.cast(p_offset + o, ctypes.c_char_p).value for o in (ctypes.c_int32 * self.lgb_asset_path_count).from_address(p_offset)]

    @functools.cached_property
    def layer_groups(self):
        return fctypes.array(LayerGroup, self.layer_group_count).from_address(ctypes.addressof(self) + self._layer_groups)

    @functools.cached_property
    def layer_sets(self):
        return LayerSetFolder.from_address(ctypes.addressof(self) + self._layer_set_folder).layer_sets

    @functools.cached_property
    def sg_timelines(self):
        return SGTimelineFolder.from_address(ctypes.addressof(self) + self._sg_timeline_folder).sg_timelines

    @functools.cached_property
    def sg_settings(self):
        return SGSettings.from_address(ctypes.addressof(self) + self._sg_settings)

    @functools.cached_property
    def housing_settings(self):
        return HousingSettings.from_address(ctypes.addressof(self) + self._housing_settings)


_logger = logging.getLogger('LayerGroup')
