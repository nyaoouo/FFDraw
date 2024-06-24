from .utils import *

@set_fields_from_annotations
class GameInstanceObject(InstanceObject):
    base_id: 'fctypes.c_uint32' = eval('0X30')


@set_fields_from_annotations
class NPCInstanceObject(GameInstanceObject):
    pop_weather: 'fctypes.c_uint32' = eval('0X34')
    pop_time_start: 'fctypes.c_uint8' = eval('0X38')
    pop_time_end: 'fctypes.c_uint8' = eval('0X39')
    padding00: 'fctypes.array(fctypes.c_uint8, 2)' = eval('0X3A')
    move_ai: 'fctypes.c_uint32' = eval('0X3C')
    wandering_range: 'fctypes.c_uint8' = eval('0X40')
    route: 'fctypes.c_uint8' = eval('0X41')
    event_group: 'fctypes.c_uint16' = eval('0X42')




@set_fields_from_annotations
class BNpcBaseData(ctypes.Structure):
    _size_ = 0X8
    territory_range: 'fctypes.c_uint16' = eval('0X0')
    sense: 'fctypes.array(fctypes.c_uint8, 2)' = eval('0X2')
    sense_range: 'fctypes.array(fctypes.c_uint8, 2)' = eval('0X4')
    mount: 'fctypes.c_uint8' = eval('0X6')


@set_fields_from_annotations
class BNPCInstanceObject(NPCInstanceObject):
    name_id: 'fctypes.c_uint32' = eval('0X4C')
    drop_item: 'fctypes.c_uint32' = eval('0X50')
    sense_range_rate: 'fctypes.c_float' = eval('0X54')
    level: 'fctypes.c_uint16' = eval('0X58')
    active_type: 'fctypes.c_uint8' = eval('0X5A')
    pop_interval: 'fctypes.c_uint8' = eval('0X5B')
    pop_rate: 'fctypes.c_uint8' = eval('0X5C')
    pop_event: 'fctypes.c_uint8' = eval('0X5D')
    link_group: 'fctypes.c_uint8' = eval('0X5E')
    link_family: 'fctypes.c_uint8' = eval('0X5F')
    link_range: 'fctypes.c_uint8' = eval('0X60')
    link_count_limit: 'fctypes.c_uint8' = eval('0X61')
    nonpop_init_zone: 'fctypes.c_int8' = eval('0X62')
    invalid_repop: 'fctypes.c_int8' = eval('0X63')
    link_parent: 'fctypes.c_int8' = eval('0X64')
    link_override: 'fctypes.c_int8' = eval('0X65')
    link_reply: 'fctypes.c_int8' = eval('0X66')
    nonpop: 'fctypes.c_int8' = eval('0X67')
    relative_positions: 'RelativePositions' = eval('0X68')
    horizontal_pop_range: 'fctypes.c_float' = eval('0X70')
    vertical_pop_range: 'fctypes.c_float' = eval('0X74')
    _b_npc_base_data: 'fctypes.c_int32' = eval('0X78')
    repop_id: 'fctypes.c_uint8' = eval('0X7C')
    bnpc_rank_id: 'fctypes.c_uint8' = eval('0X7D')
    territory_range: 'fctypes.c_uint16' = eval('0X7E')
    bound_instance_id: 'fctypes.c_uint32' = eval('0X80')
    fate_layout_label_id: 'fctypes.c_uint32' = eval('0X84')
    normal_ai: 'fctypes.c_uint32' = eval('0X88')
    server_path_id: 'fctypes.c_uint32' = eval('0X8C')
    equipment_id: 'fctypes.c_uint32' = eval('0X90')
    customize_id: 'fctypes.c_uint32' = eval('0X94')

    @functools.cached_property
    def b_npc_base_data(self):
        return BNpcBaseData.from_address(ctypes.addressof(self) + self._b_npc_base_data)


@set_fields_from_annotations
class ENPCInstanceObject(NPCInstanceObject):
    behavior: 'fctypes.c_uint32' = eval('0X4C')
    mount_id: 'fctypes.c_uint32' = eval('0X50')
    aerial_access: 'fctypes.c_int8' = eval('0X54')
    disable_hum: 'fctypes.c_int8' = eval('0X55')


@set_fields_from_annotations
class GatheringInstanceObject(GameInstanceObject):
    pass


@set_fields_from_annotations
class AetheryteInstanceObject(GameInstanceObject):
    bound_instance_id: 'fctypes.c_uint32' = eval('0X34')


@set_fields_from_annotations
class EventInstanceObject(GameInstanceObject):
    bound_instance_id: 'fctypes.c_uint32' = eval('0X34')
    linked_instance_id: 'fctypes.c_uint32' = eval('0X38')
    aerial_access: 'fctypes.c_int8' = eval('0X3C')
    disable_error_check: 'fctypes.c_int8' = eval('0X3D')


@set_fields_from_annotations
class TreasureInstanceObject(GameInstanceObject):
    nonpop_init_zone: 'fctypes.c_int8' = eval('0X34')
