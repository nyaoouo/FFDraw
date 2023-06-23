import dataclasses
import logging
import typing

from . import enums
from .utils import message
from .message_structs import zone_server, actor_control

if typing.TYPE_CHECKING:
    from .sniffer_main import Sniffer

RESTART_EVENT_DIRECTOR = {
    actor_control.EventDirectorType.Start.value,
    actor_control.EventDirectorType.Restart.value,
    actor_control.EventDirectorType.PvpReady.value,
}


class SnifferExtra:
    logger = logging.getLogger('SnifferExtra')

    def __init__(self, sniffer: 'Sniffer'):
        self.sniffer = sniffer

        sniffer.on_zone_server_message[enums.ZoneServer.ActorControl].append(self._on_actor_control)
        sniffer.on_zone_server_message[enums.ZoneServer.ActorControlSelf].append(self._on_actor_control_self)
        sniffer.on_zone_server_message[enums.ZoneServer.ActorControlTarget].append(self._on_actor_control_target)
        sniffer.on_zone_server_message[enums.ZoneServer.Effect].append(sniffer.on_action_effect)
        sniffer.on_zone_server_message[enums.ZoneServer.AoeEffect8].append(sniffer.on_action_effect)
        sniffer.on_zone_server_message[enums.ZoneServer.AoeEffect16].append(sniffer.on_action_effect)
        sniffer.on_zone_server_message[enums.ZoneServer.AoeEffect24].append(sniffer.on_action_effect)
        sniffer.on_zone_server_message[enums.ZoneServer.AoeEffect32].append(sniffer.on_action_effect)
        sniffer.on_zone_server_message[enums.ZoneServer.RsvString].append(self.on_rsv_string)
        sniffer.on_zone_server_message[enums.ZoneServer.StartActionTimelineMulti].append(self.on_play_action_timeline_muliti)
        sniffer.on_zone_server_message[enums.ZoneServer.EffectResult].append(self.on_effect_result)
        sniffer.on_zone_server_message[enums.ZoneServer.EffectResult4].append(self.on_effect_result)
        sniffer.on_zone_server_message[enums.ZoneServer.EffectResult8].append(self.on_effect_result)
        sniffer.on_zone_server_message[enums.ZoneServer.EffectResult16].append(self.on_effect_result)
        sniffer.on_actor_control[enums.ActorControlId.PlayActionTimeLine].append(self.on_actor_control_play_action_timeline)
        sniffer.on_actor_control[enums.ActorControlId.EventDirector].append(self.on_actor_control_event_director)

    def on_effect_result(self, msg: message.NetworkMessage[zone_server.EffectResult]):
        for eff in msg.message:
            for i in range(eff.status_count):
                status = eff.status[i]
                self.sniffer.on_add_status_by_action(message.AddStatusByActionMessage(
                    raw_msg=msg,
                    source_id=msg.header.source_id,
                    target_id=eff.target_id,
                    status_id=status.status_id,
                    param=status.param,
                    time=status.time,
                ))

    def on_actor_control_event_director(self, msg: message.ActorControlMessage[actor_control.EventDirector]):
        if msg.param.director_id in RESTART_EVENT_DIRECTOR:
            self.sniffer.on_reset(msg)

    def on_rsv_string(self, msg: message.NetworkMessage[zone_server.RsvString]):
        k = msg.message.key
        v = msg.message.value
        self.logger.debug(f'set rsv string {k} => {v}')
        self.sniffer.main.sq_pack.exd.rsv_string[k] = v

    def on_actor_control_play_action_timeline(self, msg: message.ActorControlMessage[actor_control.PlayActionTimeLine]):
        self.sniffer.on_play_action_timeline(message.PlayActionTimelineMessage(
            raw_msg=msg,
            id=msg.source_id,
            timeline_id=msg.param.action_timeline_id,
        ))

    def on_play_action_timeline_muliti(self, msg: message.NetworkMessage[zone_server.StartActionTimelineMulti]):
        for actor_id, timeline_id in msg.message:
            self.sniffer.on_play_action_timeline(message.PlayActionTimelineMessage(
                raw_msg=msg,
                id=actor_id,
                timeline_id=timeline_id,
            ))

    def _on_all_actor_control(self, msg: message.ActorControlMessage):
        try:
            msg.id = enums.ActorControlId(msg.id)
        except ValueError:
            pass
        if msg.id == enums.ActorControlId.SetLockOn:
            msg.args[0] += self.sniffer.packet_fix.value
        if t := actor_control.type_map.get(msg.id):
            if not hasattr(t, '__field_count'):
                setattr(t, '__field_count', cnt := len(dataclasses.fields(t)))
            else:
                cnt = getattr(t, '__field_count')
            msg.param = t(*msg.args[:cnt])
        if self.sniffer.print_actor_control:
            self.sniffer.logger.debug(str(msg))
        self.sniffer.on_actor_control(msg)

    def _on_actor_control(self, msg: message.NetworkMessage[zone_server.ActorControl]):
        data = msg.message
        self._on_all_actor_control(message.ActorControlMessage(
            raw_msg=msg, source_id=msg.header.source_id, id=data.id,
            args=[data.arg0, data.arg1, data.arg2, data.arg3, 0, 0],
        ))

    def _on_actor_control_self(self, msg: message.NetworkMessage[zone_server.ActorControlSelf]):
        data = msg.message
        self._on_all_actor_control(message.ActorControlMessage(
            raw_msg=msg, source_id=msg.header.source_id, id=data.id,
            args=[data.arg0, data.arg1, data.arg2, data.arg3, data.arg4, data.arg5, ],
        ))

    def _on_actor_control_target(self, msg: message.NetworkMessage[zone_server.ActorControlTarget]):
        data = msg.message
        self._on_all_actor_control(message.ActorControlMessage(
            raw_msg=msg, source_id=msg.header.source_id, target_id=data.target_id, id=data.id,
            args=[data.arg0, data.arg1, data.arg2, data.arg3, 0, 0],
        ))
