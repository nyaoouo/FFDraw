import io
import typing
from nylib.utils import serialize_data
from .utils import *

if typing.TYPE_CHECKING:
    from fpt4.utils.sqpack import SqPack
    from ff_draw.sniffer.message_structs import zone_server as _zone_server, actor_control as _actor_control


def fmt_simple(data):
    if isinstance(data, dict):
        return "[" + ';'.join(f'{k}={fmt_simple(v)}' for k, v in data.items()) + "]"
    elif isinstance(data, (list, tuple)):
        return "[" + ';'.join(fmt_simple(v) for v in data) + "]"
    elif isinstance(data, int):
        return hex(data)
    elif isinstance(data, float):
        return f'{data:.2f}'
    return str(data)


class DataFormatter:
    def __init__(self):
        self._formatters = {}

    def add(self, key, *keys):
        def wrapper(func):
            self._formatters[key] = func
            for k in keys:
                self._formatters[k] = func
            return func

        return wrapper

    def fmt(self, proto_no: str, source_id: int, data, sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], *args, **kwargs):
        return self._formatters[proto_no](source_id, data, sq_pack, actor_getter, *args, **kwargs)


zone_server_fmt = DataFormatter()
actor_control_fmt = DataFormatter()
zone_client_fmt = DataFormatter()
chat_server_fmt = DataFormatter()
chat_client_fmt = DataFormatter()


def fmt_action(sq_pack: 'SqPack', action_id, action_kind=1):
    if not action_id:
        return 'None#0'
    match action_kind:
        case 1:
            try:
                name = sq_pack.sheets.action_sheet[action_id][0]
            except KeyError:
                name = f'Unknown Action'
        # todo: different action kinds
        case _:
            name = f'Action {action_kind}-{action_id}'
    return f'{name}#{action_id}'


def fmt_status(sq_pack: 'SqPack', status_id):
    if not status_id:
        return 'None#0'
    try:
        name = sq_pack.sheets.status_sheet[status_id][0]
    except KeyError:
        name = f'Unknown Status'
    return f'{name}#{status_id}'


def fmt_name(sq_pack: 'SqPack', name_id):
    if not name_id:
        return 'None#0'
    if name_id < 1000000:
        return f'{sq_pack.sheets.b_npc_name_sheet[name_id][0]}#{name_id}'
    else:
        return f'{sq_pack.sheets.e_npc_resident_sheet[name_id][0]}#{name_id}'


def fmt_lockon(sq_pack: 'SqPack', lockon_id):
    if not lockon_id:
        return 'None#0'
    try:
        name = sq_pack.sheets.lockon_sheet[lockon_id].file
    except KeyError:
        name = f'Unknown Lockon'
    return f'{name}#{lockon_id}'


def fmt_channeling(sq_pack: 'SqPack', channeling_id):
    if not channeling_id:
        return 'None#0'
    try:
        name = sq_pack.sheets.channeling_sheet[channeling_id].file
    except KeyError:
        name = f'Unknown channeling'
    return f'{name}#{channeling_id}'


@zone_server_fmt.add('Effect', 'AoeEffect8', 'AoeEffect16', 'AoeEffect24', 'AoeEffect32')
def fmt_zone_server_action_effect(source_id: int, data: '_zone_server.ActionEffect', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef]):
    cnt = 0
    targets = []
    for target_id, effects_raw in zip(data.target_ids, data.effects):
        if not target_id or target_id == 0xe0000000: break
        cnt += 1
        targets.append(actor_getter(target_id))
    return f'{actor_getter(source_id)} use {fmt_action(sq_pack, data.action_id, data.action_kind)} on {cnt} targets:' + ', '.join(map(str, targets))


@zone_server_fmt.add('ActorCast')
def fmt_zone_server_actor_cast(source_id: int, data: '_zone_server.ActorCast', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef]):
    return f'{actor_getter(source_id)} cast {fmt_action(sq_pack, data.action_id, data.action_kind)} on {actor_getter(data.target_id)} for {data.cast_time:.2f}s'


@zone_server_fmt.add('ActorDelete')
def fmt_zone_server_actor_delete(source_id: int, data: '_zone_server.ActorDelete', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef]):
    return f'{actor_getter(data.actor_id)} delete'


@zone_server_fmt.add('EffectResult', 'EffectResult4', 'EffectResult8', 'EffectResult16')
def fmt_zone_server_effect_result(source_id: int, data: '_zone_server.EffectResult', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef]):
    buf = io.StringIO(f'update status by action from {actor_getter(source_id)}: ')
    for effect_result in data:
        target = actor_getter(effect_result.target_id)
        buf.write(f'{target} ->(')
        for i, status in enumerate(effect_result.iter_status()):
            if i: buf.write(', ')
            buf.write(f"{fmt_status(sq_pack, status.status_id)}<{status.param}>[{status.time:.2f}s]")
        buf.write(') ')
    return buf.getvalue()


@zone_server_fmt.add('MapEffect')
def fmt_zone_server_map_effect(source_id: int, data: '_zone_server.MapEffect', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef]):
    return f'map effect: director_id={data.director_id:#X}, state={data.state:#X}, play_state={data.play_state:#X}, index={data.index:#X}'


@zone_server_fmt.add('NpcSpawn', 'NpcSpawn2', 'ObjectSpawn', 'PlayerSpawn')
def fmt_zone_server_actor_spawn(source_id: int, data, sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef]):
    return f'actor spawn: {actor_getter(source_id)}'


@zone_server_fmt.add('StartActionTimelineMulti')
def fmt_zone_server_start_action_timeline_multi(source_id: int, data: '_zone_server.StartActionTimelineMulti', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef]):
    buf = io.StringIO(f'start action timeline: ')
    for actor_id, timeline_id in data:
        buf.write(f'{actor_getter(actor_id)}->{timeline_id};')
    return buf.getvalue()


@zone_server_fmt.add('RsvString')
def fmt_zone_server_rsv_string(source_id: int, data: '_zone_server.RsvString', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef]):
    return f'set rsv string: {data.key} -> {data.value}'


@zone_server_fmt.add('NpcYell')
def fmt_zone_server_npc_yell(source_id: int, data: '_zone_server.NpcYell', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef]):
    return f'{fmt_name(sq_pack, data.name_id)} yell [{data.npc_yell_id}]: {sq_pack.sheets.npc_yell_sheet[data.npc_yell_id].npc_text}'


@actor_control_fmt.add('Death')
def fmt_actor_control_death(source_id: int, data: '_actor_control.Death', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], target_id: int):
    return f'{actor_getter(source_id)} killed by {actor_getter(data.killer)}'


@actor_control_fmt.add('CancelCast')
def fmt_actor_control_cancel_cast(source_id: int, data: '_actor_control.CancelCast', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], target_id: int):
    return f'{actor_getter(source_id)} cancel cast {fmt_action(sq_pack, data.action_id, data.action_kind)}'


@actor_control_fmt.add('InterruptCast')
def fmt_actor_control_interrupt_cast(source_id: int, data: '_actor_control.InterruptCast', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], target_id: int):
    return f'{actor_getter(source_id)} interrupt cast {fmt_action(sq_pack, data.action_id, data.action_kind)}'


@actor_control_fmt.add('AddStatus')
def fmt_actor_control_add_status(source_id: int, data: '_actor_control.AddStatus', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], target_id: int):
    return f'{actor_getter(source_id)} add status {fmt_status(sq_pack, data.status_id)}<{data.param}>'


@actor_control_fmt.add('RemoveStatus')
def fmt_actor_control_remove_status(source_id: int, data: '_actor_control.RemoveStatus', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], target_id: int):
    return f'{actor_getter(source_id)} remove status {fmt_status(sq_pack, data.status_id)}<{data.param}>'


@actor_control_fmt.add('SetStatusParam')
def fmt_actor_control_set_status_param(source_id: int, data: '_actor_control.SetStatusParam', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], target_id: int):
    return f'{actor_getter(source_id)} set status {fmt_status(sq_pack, data.status_id)}<{data.param}>'


@actor_control_fmt.add('StatusEffect')
def fmt_actor_control_status_effect(source_id: int, data: '_actor_control.StatusEffect', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], target_id: int):
    if data.effect_type == 0x3:
        return f'{actor_getter(source_id)} status dot from {fmt_status(sq_pack, data.status_id)} by {data.value}'
    elif data.effect_type == 0x4:
        return f'{actor_getter(source_id)} status hot from {fmt_status(sq_pack, data.status_id)} by {data.value}'


@actor_control_fmt.add('SetLockOn')
def fmt_actor_control_set_lock_on(source_id: int, data: '_actor_control.SetLockOn', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], target_id: int):
    return f'{actor_getter(source_id)} set lock on {fmt_lockon(sq_pack, data.lockon_id)}'


@actor_control_fmt.add('SetChanneling')
def fmt_actor_control_set_channeling(source_id: int, data: '_actor_control.SetChanneling', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], target_id: int):
    return f'{actor_getter(source_id)} set channeling to {actor_getter(data.target_id)} on {fmt_channeling(sq_pack, data.channel_id)}'


@actor_control_fmt.add('RemoveChanneling')
def fmt_actor_control_remove_channeling(source_id: int, data: '_actor_control.RemoveChanneling', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], target_id: int):
    return f'{actor_getter(source_id)} remove channeling {fmt_channeling(sq_pack, data.channel_id)}'


@actor_control_fmt.add('SetModelAttr')
def fmt_actor_control_set_model_attr(source_id: int, data: '_actor_control.SetModelAttr', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], target_id: int):
    return f'{actor_getter(source_id)} set model attr to {data.value}'


@actor_control_fmt.add('SetTargetable')
def fmt_actor_control_set_targetable(source_id: int, data: '_actor_control.SetTargetable', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], target_id: int):
    if data.is_targetable:
        return f'{actor_getter(data.target_id)} is now targetable'
    else:
        return f'{actor_getter(data.target_id)} is now untargetable'


@actor_control_fmt.add('EventDirector')
def fmt_actor_control_event_director(source_id: int, data: '_actor_control.EventDirector', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], target_id: int):
    director_type = data.type
    return f'event director: handler={data.handler_id:#X} type={director_type and director_type.name}#{data.director_id} args=({data.arg0:#X}, {data.arg1:#X}, {data.arg2:#X}, {data.arg3:#X})'


@actor_control_fmt.add('SetLimitBreak')
def fmt_actor_control_set_limit_break(source_id: int, data: '_actor_control.SetLimitBreak', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], target_id: int):
    return f'update limit break max_level={data.max_level} value={data.value}'


@actor_control_fmt.add('PlayActionTimeLine')
def fmt_actor_control_play_action_time_line(source_id: int, data: '_actor_control.PlayActionTimeLine', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], target_id: int):
    return f'{actor_getter(source_id)} play action time line {data.action_timeline_id}'


@actor_control_fmt.add('SetActorTimeLine')
def fmt_actor_control_set_actor_time_line(source_id: int, data: '_actor_control.SetActorTimeLine', sq_pack: 'SqPack', actor_getter: typing.Callable[[int], ActorDef], target_id: int):
    return f'{actor_getter(data.target_id)} set time line ({data.param1}, {data.param2})'
