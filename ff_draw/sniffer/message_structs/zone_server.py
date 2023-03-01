from ctypes import *

import glm

from nylib.struct import set_fields_from_annotations, fctypes
from fpt4.utils.se_string import SeString
from ff_draw.sniffer.utils.simple import pos_web_to_raw, dir_web_to_raw
from . import TypeMap, ZoneServer

type_map = TypeMap()


@set_fields_from_annotations
class ActionEffectBase(Structure):
    _size_ = 0X28
    main_target_id: 'fctypes.c_uint32' = eval('0X0')
    real_action_id: 'fctypes.c_uint32' = eval('0X8')
    response_id: 'fctypes.c_uint32' = eval('0XC')
    lock_time: 'fctypes.c_float' = eval('0X10')
    ballista_target_id: 'fctypes.c_uint32' = eval('0X14')
    request_id: 'fctypes.c_uint16' = eval('0X18')
    _facing: 'fctypes.c_uint16' = eval('0X1A')
    action_id: 'fctypes.c_uint16' = eval('0X1C')
    action_variant: 'fctypes.c_uint8' = eval('0X1E')
    action_kind: 'fctypes.c_uint8' = eval('0X1F')
    flag: 'fctypes.c_uint8' = eval('0X20')
    target_count: 'fctypes.c_uint8' = eval('0X21')

    def _pkt_fix(self, v):
        self.real_action_id += v

    @property
    def facing(self):
        return dir_web_to_raw(self._facing)


@set_fields_from_annotations
class _ActionEffect(Structure):
    _size_ = 0X8
    type: 'fctypes.c_uint8' = eval('0X0')
    arg0: 'fctypes.c_uint8' = eval('0X1')
    arg1: 'fctypes.c_uint8' = eval('0X2')
    arg2: 'fctypes.c_uint8' = eval('0X3')
    arg3: 'fctypes.c_uint8' = eval('0X4')
    flag: 'fctypes.c_uint8' = eval('0X5')
    value: 'fctypes.c_int16' = eval('0X6')


ActionEffects = fctypes.array(_ActionEffect, 8)


@type_map.set(ZoneServer.Effect)
@set_fields_from_annotations
class ActionEffect(ActionEffectBase):
    _size_ = 0X78
    effects: 'fctypes.array(ActionEffects, 1)' = eval('0X2A')
    target_ids: 'fctypes.array(fctypes.c_uint64, 1)' = eval('0X70')
    pos = glm.vec3(0, 0, 0)


@type_map.set(ZoneServer.AoeEffect8)
@set_fields_from_annotations
class ActionEffect8(ActionEffectBase):
    _size_ = 0X278
    effects: 'fctypes.array(ActionEffects, 8)' = eval('0X2A')
    target_ids: 'fctypes.array(fctypes.c_uint64, 8)' = eval('0X230')
    _pos: 'fctypes.array(fctypes.c_uint16, 3)' = eval('0X270')

    @property
    def pos(self):
        return glm.vec3(*map(pos_web_to_raw, self._pos))


@type_map.set(ZoneServer.AoeEffect16)
@set_fields_from_annotations
class ActionEffect16(ActionEffectBase):
    _size_ = 0X4B8
    effects: 'fctypes.array(ActionEffects, 16)' = eval('0X2A')
    target_ids: 'fctypes.array(fctypes.c_uint64, 16)' = eval('0X430')
    _pos: 'fctypes.array(fctypes.c_uint16, 3)' = eval('0X4B0')

    @property
    def pos(self):
        return glm.vec3(*map(pos_web_to_raw, self._pos))


@type_map.set(ZoneServer.AoeEffect24)
@set_fields_from_annotations
class ActionEffect24(ActionEffectBase):
    _size_ = 0X6F8
    effects: 'fctypes.array(ActionEffects, 24)' = eval('0X2A')
    target_ids: 'fctypes.array(fctypes.c_uint64, 24)' = eval('0X630')
    _pos: 'fctypes.array(fctypes.c_uint16, 3)' = eval('0X6F0')

    @property
    def pos(self):
        return glm.vec3(*map(pos_web_to_raw, self._pos))


@type_map.set(ZoneServer.AoeEffect32)
@set_fields_from_annotations
class ActionEffect32(ActionEffectBase):
    _size_ = 0X6F8
    effects: 'fctypes.array(ActionEffects, 32)' = eval('0X2A')
    target_ids: 'fctypes.array(fctypes.c_uint64, 32)' = eval('0X830')
    _pos: 'fctypes.array(fctypes.c_uint16, 3)' = eval('0X930')

    @property
    def pos(self):
        return glm.vec3(*map(pos_web_to_raw, self._pos))


@type_map.set(ZoneServer.ActorCast)
@set_fields_from_annotations
class ActorCast(Structure):
    _size_ = 0X20
    action_id: 'fctypes.c_uint16' = eval('0X0')
    action_kind: 'fctypes.c_uint8' = eval('0X2')
    display_delay: 'fctypes.c_uint8' = eval('0X3')
    real_action_id: 'fctypes.c_uint32' = eval('0X4')
    cast_time: 'fctypes.c_float' = eval('0X8')
    target_id: 'fctypes.c_uint32' = eval('0XC')
    _facing: 'fctypes.c_uint16' = eval('0X10')
    can_interrupt: 'fctypes.c_uint8' = eval('0X12')
    _pos: 'fctypes.array(fctypes.c_uint16, 3)' = eval('0X18')

    def _pkt_fix(self, v):
        self.real_action_id += v

    @property
    def pos(self):
        return glm.vec3(*map(pos_web_to_raw, self._pos))

    @property
    def facing(self):
        return dir_web_to_raw(self._facing)


@type_map.set(ZoneServer.ActorControl)
@set_fields_from_annotations
class ActorControl(Structure):
    _size_ = 0X18
    id: 'fctypes.c_uint16' = eval('0X0')
    arg0: 'fctypes.c_uint32' = eval('0X4')
    arg1: 'fctypes.c_uint32' = eval('0X8')
    arg2: 'fctypes.c_uint32' = eval('0XC')
    arg3: 'fctypes.c_uint32' = eval('0X10')


@type_map.set(ZoneServer.ActorControlSelf)
@set_fields_from_annotations
class ActorControlSelf(Structure):
    _size_ = 0X20

    id: 'fctypes.c_uint16' = eval('0X0')
    arg0: 'fctypes.c_uint32' = eval('0X4')
    arg1: 'fctypes.c_uint32' = eval('0X8')
    arg2: 'fctypes.c_uint32' = eval('0XC')
    arg3: 'fctypes.c_uint32' = eval('0X10')
    arg4: 'fctypes.c_uint32' = eval('0X14')
    arg5: 'fctypes.c_uint32' = eval('0X18')


@type_map.set(ZoneServer.ActorControlTarget)
@set_fields_from_annotations
class ActorControlTarget(Structure):
    _size_ = 0X20
    id: 'fctypes.c_uint16' = eval('0X0')
    arg0: 'fctypes.c_uint32' = eval('0X4')
    arg1: 'fctypes.c_uint32' = eval('0X8')
    arg2: 'fctypes.c_uint32' = eval('0XC')
    arg3: 'fctypes.c_uint32' = eval('0X10')
    target_id: 'fctypes.c_uint64' = eval('0X18')


@type_map.set(ZoneServer.ActorDelete)
@set_fields_from_annotations
class ActorDelete(Structure):
    _size_ = 0X8

    index: 'fctypes.c_uint8' = eval('0X0')
    actor_id: 'fctypes.c_uint32' = eval('0X4')


@type_map.set(ZoneServer.ActorGauge)
@set_fields_from_annotations
class ActorGauge(Structure):
    _size_ = 0X10
    buffer: 'c_char*16' = eval('0X0')


@type_map.set(ZoneServer.UpdateHpMpGp)
@set_fields_from_annotations
class UpdateHpMpGp(Structure):
    _size_ = 0X8

    hp: 'fctypes.c_uint32' = eval('0X0')
    mp: 'fctypes.c_uint16' = eval('0X4')
    gp: 'fctypes.c_uint16' = eval('0X6')


@type_map.set(ZoneServer.ContainerItemInfo)
@set_fields_from_annotations
class UpdateHpMpGp(Structure):
    _size_ = 0X8

    hp: 'fctypes.c_uint32' = eval('0X0')
    mp: 'fctypes.c_uint16' = eval('0X4')
    gp: 'fctypes.c_uint16' = eval('0X6')


@set_fields_from_annotations
class EffectResultStatus(Structure):
    _size_ = 0X10

    status_slot: 'fctypes.c_uint8' = eval('0X0')
    status_id: 'fctypes.c_uint16' = eval('0X2')
    param: 'fctypes.c_int16' = eval('0X4')
    time: 'fctypes.c_float' = eval('0X8')
    source_id: 'fctypes.c_uint32' = eval('0XC')


@set_fields_from_annotations
class _EffectResult(Structure):
    _size_ = 0X58

    response_id: 'fctypes.c_uint32' = eval('0X0')
    target_id: 'fctypes.c_uint32' = eval('0X4')
    current_hp: 'fctypes.c_uint32' = eval('0X8')
    max_hp: 'fctypes.c_uint32' = eval('0XC')
    current_mp: 'fctypes.c_uint16' = eval('0X10')
    class_job: 'fctypes.c_uint8' = eval('0X13')
    shield: 'fctypes.c_uint8' = eval('0X14')
    status_count: 'fctypes.c_uint8' = eval('0X15')
    status: 'fctypes.array(EffectResultStatus, 4)' = eval('0X18')


@type_map.set(ZoneServer.EffectResult)
@type_map.set(ZoneServer.EffectResult4)
@type_map.set(ZoneServer.EffectResult8)
@type_map.set(ZoneServer.EffectResult16)
@set_fields_from_annotations
class EffectResult(Structure):
    _size_ = 0X60
    count: 'fctypes.c_uint8' = eval('0X0')
    results: 'fctypes.array(_EffectResult, 16)' = eval('0X4')


@type_map.set(ZoneServer.MapEffect)
@set_fields_from_annotations
class MapEffect(Structure):
    _size_ = 0X10
    director_id: 'fctypes.c_uint32' = eval('0X0')
    state: 'fctypes.c_uint16' = eval('0X4')
    play_state: 'fctypes.c_uint16' = eval('0X6')
    index: 'fctypes.c_uint8' = eval('0X8')


@set_fields_from_annotations
class Status(Structure):
    _size_ = 0XC
    buff_id: 'fctypes.c_uint16' = eval('0X0')
    param: 'fctypes.c_int16' = eval('0X2')
    timer: 'fctypes.c_float' = eval('0X4')
    actor_id: 'fctypes.c_uint32' = eval('0X8')


@set_fields_from_annotations
class CommonSpawn(Structure):
    _size_ = 0X268
    main_target: 'fctypes.c_uint64' = eval('0X0')
    head_gear_model: 'fctypes.c_uint64' = eval('0X8')
    main_weapon_model: 'fctypes.c_uint64' = eval('0X10')
    sub_weapon_model: 'fctypes.c_uint64' = eval('0X18')
    first_attack_id: 'fctypes.c_uint64' = eval('0X28')
    npc_id: 'fctypes.c_uint32' = eval('0X30')
    name_id: 'fctypes.c_uint32' = eval('0X34')
    layout_id: 'fctypes.c_uint32' = eval('0X38')
    obj_type_data: 'fctypes.c_uint32' = eval('0X3C')
    content_id: 'fctypes.c_uint32' = eval('0X40')
    owner_id: 'fctypes.c_uint32' = eval('0X44')
    channeling_target: 'fctypes.c_uint32' = eval('0X48')
    max_hp: 'fctypes.c_uint32' = eval('0X4C')
    current_hp: 'fctypes.c_uint32' = eval('0X50')
    flag: 'fctypes.c_uint32' = eval('0X54')
    fate_id: 'fctypes.c_uint16' = eval('0X58')
    current_mp: 'fctypes.c_uint16' = eval('0X5A')
    max_mp: 'fctypes.c_uint16' = eval('0X5C')
    normal_ai: 'fctypes.c_uint16' = eval('0X5E')
    model_chara_id: 'fctypes.c_uint16' = eval('0X60')
    facing: 'fctypes.c_uint16' = eval('0X62')
    mount_id: 'fctypes.c_uint16' = eval('0X64')
    companion: 'fctypes.c_uint16' = eval('0X66')
    ornament: 'fctypes.c_uint16' = eval('0X68')
    index: 'fctypes.c_uint8' = eval('0X6A')
    mode: 'fctypes.c_uint8' = eval('0X6B')
    mode_args: 'fctypes.c_uint8' = eval('0X6C')
    obj_kind: 'fctypes.c_uint8' = eval('0X6D')
    obj_type: 'fctypes.c_uint8' = eval('0X6E')
    voice: 'fctypes.c_uint8' = eval('0X6F')
    enable_head_gear: 'fctypes.c_uint8' = eval('0X70')
    channeling: 'fctypes.c_uint8' = eval('0X71')
    battalion_type: 'fctypes.c_uint8' = eval('0X72')
    level: 'fctypes.c_uint8' = eval('0X73')
    class_job: 'fctypes.c_uint8' = eval('0X74')
    permission_invisibility: 'fctypes.c_uint8' = eval('0X75')
    invisibility_group: 'fctypes.c_uint8' = eval('0X76')
    first_attack_type: 'fctypes.c_uint8' = eval('0X77')
    mount_head_gear: 'fctypes.c_uint8' = eval('0X78')
    mount_body_gear: 'fctypes.c_uint8' = eval('0X79')
    mount_leg_gear: 'fctypes.c_uint8' = eval('0X7A')
    mount_stain: 'fctypes.c_uint8' = eval('0X7B')
    class_job_loop_vfx: 'fctypes.c_uint8' = eval('0X7C')
    content_work1: 'fctypes.c_uint8' = eval('0X7D')
    content_work2: 'fctypes.c_uint8' = eval('0X7E')
    model_scale: 'fctypes.c_uint8' = eval('0X7F')
    model_state: 'fctypes.c_uint8' = eval('0X80')
    model_attr: 'fctypes.c_uint8' = eval('0X81')
    model_overlay: 'fctypes.c_uint8' = eval('0X82')
    status: 'fctypes.array(Status, 30)' = eval('0X84')
    _pos: 'fctypes.array(fctypes.c_float, 3)' = eval('0X1EC')
    gears: 'fctypes.array(fctypes.c_uint32, 10)' = eval('0X1F8')
    __name: 'fctypes.array(fctypes.c_char, 32)' = eval('0X220')
    customize: 'fctypes.array(fctypes.c_uint8, 26)' = eval('0X240')
    __fc_tag: 'fctypes.array(fctypes.c_char, 7)' = eval('0X25A')

    @property
    def pos(self):
        return glm.vec3(*self._pos)

    @property
    def name(self) -> str:
        return self.__name.decode('utf-8', 'ignore')

    @property
    def fc_tag(self) -> str:
        return self.__fc_tag.decode('utf-8', 'ignore')


@type_map.set(ZoneServer.NpcSpawn)
@set_fields_from_annotations
class NpcSpawn(Structure):
    _size_ = 0X280
    bind_id: 'fctypes.c_uint32' = eval('0X0')
    trigger_id: 'fctypes.c_uint32' = eval('0X4')
    active_type: 'fctypes.c_uint8' = eval('0X8')
    rank: 'fctypes.c_uint8' = eval('0X9')
    link_reply: 'fctypes.c_uint8' = eval('0XA')
    link_count_limit: 'fctypes.c_uint8' = eval('0XB')
    link_group: 'fctypes.c_uint8' = eval('0XC')
    link_range: 'fctypes.c_uint8' = eval('0XD')
    link_family: 'fctypes.c_uint8' = eval('0XE')
    link_parent: 'fctypes.c_uint8' = eval('0XF')
    create_common: 'CommonSpawn' = eval('0X10')
    parts_state: 'fctypes.array(fctypes.c_uint8, 6)' = eval('0X278')


@type_map.set(ZoneServer.NpcSpawn2)
@set_fields_from_annotations
class NpcSpawn2(NpcSpawn):
    _size_ = 0X3F0
    expand_status: 'fctypes.array(Status, 30)' = eval('0X284')


@type_map.set(ZoneServer.ObjectSpawn)
@set_fields_from_annotations
class ObjectSpawn(Structure):
    _size_ = 0X40

    index: 'fctypes.c_uint8' = eval('0X0')
    kind: 'fctypes.c_uint8' = eval('0X1')
    flag: 'fctypes.c_uint8' = eval('0X2')
    invisibility_group: 'fctypes.c_uint8' = eval('0X3')
    base_id: 'fctypes.c_uint32' = eval('0X4')
    id: 'fctypes.c_uint32' = eval('0X8')
    layout_id: 'fctypes.c_uint32' = eval('0XC')
    content_id: 'fctypes.c_uint32' = eval('0X10')
    owner_id: 'fctypes.c_uint32' = eval('0X14')
    bind_layout_id: 'fctypes.c_uint32' = eval('0X18')
    scale: 'fctypes.c_float' = eval('0X1C')
    shared_group_timeline_state: 'fctypes.c_uint16' = eval('0X20')
    facing: 'fctypes.c_uint16' = eval('0X22')
    fate: 'fctypes.c_uint16' = eval('0X24')
    permission_invisibility: 'fctypes.c_uint8' = eval('0X26')
    arg1: 'fctypes.c_uint8' = eval('0X27')
    arg2: 'fctypes.c_uint32' = eval('0X28')
    arg3: 'fctypes.c_uint32' = eval('0X2C')
    pos: 'fctypes.array(fctypes.c_float, 3)' = eval('0X30')


@set_fields_from_annotations
class PartyMember(Structure):
    _size_ = 0X1B8
    _name: 'fctypes.array(fctypes.c_char, 32)' = eval('0X0')
    character_id: 'fctypes.c_uint64' = eval('0X20')
    actor_id: 'fctypes.c_uint32' = eval('0X28')
    pet_id: 'fctypes.c_uint32' = eval('0X2C')
    buddy_id: 'fctypes.c_uint32' = eval('0X30')
    current_hp: 'fctypes.c_uint32' = eval('0X34')
    max_hp: 'fctypes.c_uint32' = eval('0X38')
    current_mp: 'fctypes.c_uint16' = eval('0X3C')
    max_mp: 'fctypes.c_uint16' = eval('0X3E')
    home_world_id: 'fctypes.c_uint16' = eval('0X40')
    territory_id: 'fctypes.c_uint16' = eval('0X42')
    flag: 'fctypes.c_uint8' = eval('0X44')
    class_job: 'fctypes.c_uint8' = eval('0X45')
    sex: 'fctypes.c_uint8' = eval('0X46')
    level: 'fctypes.c_uint8' = eval('0X47')
    level_sync: 'fctypes.c_uint8' = eval('0X48')
    status: 'fctypes.array(Status, 30)' = eval('0X4C')

    @property
    def name(self) -> str:
        return self._name.decode('utf-8', errors='ignore')


@type_map.set(ZoneServer.PartyUpdate)
@set_fields_from_annotations
class PartyUpdate(Structure):
    _size_ = 0XDD8
    member: 'fctypes.array(PartyMember, 8)' = eval('0X0')
    party_id: 'fctypes.c_uint64' = eval('0XDC0')
    chat_channel: 'fctypes.c_uint64' = eval('0XDC8')
    leader_index: 'fctypes.c_uint8' = eval('0XDD0')
    party_count: 'fctypes.c_uint8' = eval('0XDD1')


@type_map.set(ZoneServer.StartActionTimelineMulti)
@set_fields_from_annotations
class StartActionTimelineMulti(Structure):
    _size_ = 0X40
    ids: 'fctypes.array(fctypes.c_uint32, 10)' = eval('0X0')
    timeline_ids: 'fctypes.array(fctypes.c_uint16, 10)' = eval('0X28')

    def __iter__(self):
        for actor_id, timeline_id in zip(self.ids, self.timeline_ids):
            if not actor_id or actor_id == 0xe0000000: break
            yield actor_id, timeline_id


@type_map.set(ZoneServer.RsvString)
@set_fields_from_annotations
class RsvString(Structure):
    _size_ = 0X438

    value_length: 'fctypes.c_uint32' = eval('0X0')
    __key: 'fctypes.array(fctypes.c_char, 48)' = eval('0X4')
    __value: 'fctypes.array(fctypes.c_char, 1024)' = eval('0X34')

    @property
    def key(self) -> str:
        return self.__key.split(b'\0', 1)[0].decode('utf-8', errors='ignore')

    @property
    def value(self):
        return SeString.from_buffer(bytearray(self.__value[:self.value_length]))
