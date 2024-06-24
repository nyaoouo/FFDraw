import enum

from .utils import *


@set_fields_from_annotations
class TriggerBoxInstanceObject(InstanceObject):

    trigger_box_shape: 'fctypes.c_uint32' = eval('0X30')
    priority: 'fctypes.c_int16' = eval('0X34')
    enabled: 'fctypes.c_int8' = eval('0X36')

    @property
    def e_trigger_box_shape(self):
        return TriggerBoxShape(self.trigger_box_shape)


# @set_fields_from_annotations
class EventEffectRangeInstanceObject(TriggerBoxInstanceObject):
    pass


@set_fields_from_annotations
class EventRangeInstanceObject(TriggerBoxInstanceObject):
    is_checked_on_server: 'fctypes.c_int8' = eval('0X3C')
    is_bnpc_target: 'fctypes.c_int8' = eval('0X3D')
    is_line_check: 'fctypes.c_int8' = eval('0X3E')
    is_pc_target: 'fctypes.c_int8' = eval('0X3F')
    is_pet_target: 'fctypes.c_int8' = eval('0X40')
    is_not_out_death: 'fctypes.c_int8' = eval('0X41')
    is_akatsuki_target: 'fctypes.c_int8' = eval('0X42')


# @set_fields_from_annotations
class ClickableRangeInstanceObject(TriggerBoxInstanceObject):
    pass


@set_fields_from_annotations
class GimmickRangeInstanceObject(TriggerBoxInstanceObject):
    class GimmickType(enum.Enum):
        Fishing = 0X1
        Content = 0X2
        Room = 0X3

    gimmick_type: 'fctypes.c_uint32' = eval('0X3C')
    gimmick_key: 'fctypes.c_uint32' = eval('0X40')
    room_use_attribute: 'fctypes.c_int8' = eval('0X44')
    group_id: 'fctypes.c_uint8' = eval('0X45')
    enabled_in_dead: 'fctypes.c_int8' = eval('0X46')

    @property
    def e_gimmick_type(self):
        return self.GimmickType(self.gimmick_type)


@set_fields_from_annotations
class CollisionBoxInstanceObject(TriggerBoxInstanceObject):
    attribute_mask: 'fctypes.c_uint32' = eval('0X3C')
    attribute: 'fctypes.c_uint32' = eval('0X40')
    attribute2_mask: 'fctypes.c_uint32' = eval('0X44')
    attribute2: 'fctypes.c_uint32' = eval('0X48')
    push_player_out: 'fctypes.c_int8' = eval('0X4C')
    _collision_asset_path: 'fctypes.c_int32' = eval('0X50')
    collision_asset_path = offset_string('_collision_asset_path')


@set_fields_from_annotations
class WaterRangeInstanceObject(TriggerBoxInstanceObject):
    underwater_enabled: 'fctypes.c_int8' = eval('0X3C')
    disable_flapping: 'fctypes.c_int8' = eval('0X3D')


# @set_fields_from_annotations
class SphereCastRangeInstanceObject(TriggerBoxInstanceObject):
    pass


@set_fields_from_annotations
class ShowHideRangeInstanceObject(TriggerBoxInstanceObject):
    _layer_ids: 'fctypes.c_int32' = eval('0X3C')
    layer_id_count: 'fctypes.c_int32' = eval('0X40')

    @functools.cached_property
    def layer_ids(self):
        return (ctypes.c_uint8 * self.layer_id_count).from_address(ctypes.addressof(self) + self._layer_ids)


@set_fields_from_annotations
class PrefetchRangeInstanceObject(TriggerBoxInstanceObject):
    bound_instance_id: 'fctypes.c_uint32' = eval('0X3C')


# @set_fields_from_annotations
class RestBonusRangeInstanceObject(TriggerBoxInstanceObject):
    pass


# @set_fields_from_annotations
class DoorRangeInstanceObject(TriggerBoxInstanceObject):
    pass


@set_fields_from_annotations
class MapRangeInstanceObject(TriggerBoxInstanceObject):
    map: 'fctypes.c_uint32' = eval('0X3C')
    place_name_block: 'fctypes.c_uint32' = eval('0X40')
    place_name_spot: 'fctypes.c_uint32' = eval('0X44')
    weather: 'fctypes.c_uint32' = eval('0X48')
    bgm: 'fctypes.c_uint32' = eval('0X4C')
    game_collision_enabled: 'fctypes.c_int8' = eval('0X58')
    housing_area_id: 'fctypes.c_uint8' = eval('0X59')
    housing_block_id: 'fctypes.c_uint8' = eval('0X5A')
    rest_bonus_effective: 'fctypes.c_int8' = eval('0X5B')
    discovery_id: 'fctypes.c_uint8' = eval('0X5C')
    map_enabled: 'fctypes.c_int8' = eval('0X5D')
    place_name_enabled: 'fctypes.c_int8' = eval('0X5E')
    discovery_enabled: 'fctypes.c_int8' = eval('0X5F')
    bgm_enabled: 'fctypes.c_int8' = eval('0X60')
    weather_enabled: 'fctypes.c_int8' = eval('0X61')
    rest_bonus_enabled: 'fctypes.c_int8' = eval('0X62')
    bgm_play_zone_in_only: 'fctypes.c_int8' = eval('0X63')
    lift_enabled: 'fctypes.c_int8' = eval('0X64')
    housing_enabled: 'fctypes.c_int8' = eval('0X65')
    notification_enabled: 'fctypes.c_int8' = eval('0X66')
    unflyable_enabled: 'fctypes.c_int8' = eval('0X67')
    mount_disabled: 'fctypes.c_int8' = eval('0X68')
    race_enter__lalafell: 'fctypes.c_int8' = eval('0X69')


@set_fields_from_annotations
class ExitRangeInstanceObject(TriggerBoxInstanceObject):
    class ExitType(enum.Enum):
        ExitTypeZone = 0X1
        ExitTypeWarp = 0X2

    exit_type: 'fctypes.c_int32' = eval('0X3C')
    zone_id: 'fctypes.c_uint16' = eval('0X40')
    territory_type: 'fctypes.c_uint16' = eval('0X42')
    index: 'fctypes.c_int32' = eval('0X44')
    dest_instance_id: 'fctypes.c_uint32' = eval('0X48')
    return_instance_id: 'fctypes.c_uint32' = eval('0X4C')
    player_running_direction: 'fctypes.c_float' = eval('0X50')
    ex_data_id: 'fctypes.c_uint16' = eval('0X54')
    dest_instance_id_for_flying: 'fctypes.c_uint32' = eval('0X58')

    @property
    def e_exit_type(self):
        return self.ExitType(self.exit_type)


@set_fields_from_annotations
class FateRangeInstanceObject(TriggerBoxInstanceObject):
    fate_layout_label_id: 'fctypes.c_uint32' = eval('0X3C')


@set_fields_from_annotations
class GameContentsRangeInstanceObject(TriggerBoxInstanceObject):
    test_enabled: 'fctypes.c_int8' = eval('0X40')
