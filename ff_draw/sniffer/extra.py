import ctypes
import dataclasses
import logging
import time
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


class PingResFinder:
    logger = logging.getLogger('PingResFinder')

    def __init__(self, sniffer: 'Sniffer'):
        self.sniffer = sniffer
        sniffer.on_zone_client_message[enums.ZoneClient.PingReq].append(self.on_ping_req)
        sniffer.on_zone_server_message.any_call.append(self.find_ping_res)

        self.last_ping_pre = b''
        self.last_ping_at = 0
        self.ping_res_size = ctypes.sizeof(zone_server.PingRes)

    def uninstall(self):
        self.sniffer.on_zone_client_message[enums.ZoneClient.PingReq].remove(self.on_ping_req)
        self.sniffer.on_zone_server_message.any_call.remove(self.find_ping_res)

    def find_ping_res(self, msg: message.NetworkMessage):
        raw = msg.raw_message.raw_data[0x10:]
        pno = msg.proto_no
        if not isinstance(pno, int): return
        if len(raw) != self.ping_res_size: return
        if raw[:4] != self.last_ping_pre: return
        if time.time() - self.last_ping_at > 1: return
        self.logger.debug(f'found ping res {pno}')
        self.sniffer._zone_server_pno_map[pno] = enums.ZoneServer.PingRes
        self.sniffer.zone_server_pno['PingRes'] = [pno]
        self.uninstall()

    def on_ping_req(self, msg: message.NetworkMessage):
        self.last_ping_pre = msg.raw_message.raw_data[0x10:][:4]
        self.last_ping_at = time.time()


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
        # sniffer.on_zone_server_message[enums.ZoneServer.EffectResult4].append(self.on_effect_result)
        # sniffer.on_zone_server_message[enums.ZoneServer.EffectResult8].append(self.on_effect_result)
        # sniffer.on_zone_server_message[enums.ZoneServer.EffectResult16].append(self.on_effect_result)
        sniffer.on_actor_control[enums.ActorControlId.PlayActionTimeLine].append(self.on_actor_control_play_action_timeline)
        sniffer.on_actor_control[enums.ActorControlId.EventDirector].append(self.on_actor_control_event_director)

        self.ping_res_finder = PingResFinder(sniffer)

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
        # move to packet define to apply fix, like other packets
        # if msg.id == enums.ActorControlId.SetLockOn:
        #     msg.args[0] += self.sniffer.packet_fix.value
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
