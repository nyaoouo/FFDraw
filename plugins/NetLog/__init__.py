import imgui

from ff_draw.plugins import FFDrawPlugin
from ff_draw.sniffer.utils import message
from ff_draw.sniffer.enums import ZoneServer, ActorControlId
from nylib.utils.imgui import ctx as imgui_ctx
from . import net_log_imgui

actor_controls = ZoneServer.ActorControl, ZoneServer.ActorControlSelf, ZoneServer.ActorControlTarget


class NetLog(FFDrawPlugin):
    def __init__(self, main):
        super().__init__(main)
        self.nl = net_log_imgui.NetLogger(self.main.sq_pack, self.get_actor)
        self.actor_cache = {}
        self.main.sniffer.on_zone_server_message.any(self.on_zone_server_message)
        self.main.sniffer.on_zone_client_message.any(self.on_zone_client_message)
        self.main.sniffer.on_chat_server_message.any(self.on_chat_server_message)
        self.main.sniffer.on_chat_client_message.any(self.on_chat_client_message)
        self.main.sniffer.on_actor_control.any(self.on_actor_control_message)

    def on_unload(self):
        self.main.sniffer.on_zone_server_message.unhook_any(self.on_zone_server_message)
        self.main.sniffer.on_zone_client_message.unhook_any(self.on_zone_client_message)
        self.main.sniffer.on_chat_server_message.unhook_any(self.on_chat_server_message)
        self.main.sniffer.on_chat_client_message.unhook_any(self.on_chat_client_message)
        self.main.sniffer.on_actor_control.unhook_any(self.on_actor_control_message)

    def on_zone_server_message(self, msg: message.NetworkMessage):
        if msg.proto_no in actor_controls: return  # process in on_actor_control_message
        key = msg.proto_no if isinstance(msg.proto_no, int) else msg.proto_no.name
        self.nl.append_data(net_log_imgui.ZoneServerIpc(self.nl, msg.raw_message.bundle_header.timestamp_ms, msg.header.source_id, key, msg.message))

    def on_zone_client_message(self, msg: message.NetworkMessage):
        key = msg.proto_no if isinstance(msg.proto_no, int) else msg.proto_no.name
        self.nl.append_data(net_log_imgui.ZoneClientIpc(self.nl, msg.raw_message.bundle_header.timestamp_ms, msg.header.source_id, key, msg.message))

    def on_chat_server_message(self, msg: message.NetworkMessage):
        key = msg.proto_no if isinstance(msg.proto_no, int) else msg.proto_no.name
        self.nl.append_data(net_log_imgui.ChatServerIpc(self.nl, msg.raw_message.bundle_header.timestamp_ms, msg.header.source_id, key, msg.message))

    def on_chat_client_message(self, msg: message.NetworkMessage):
        key = msg.proto_no if isinstance(msg.proto_no, int) else msg.proto_no.name
        self.nl.append_data(net_log_imgui.ChatClientIpc(self.nl, msg.raw_message.bundle_header.timestamp_ms, msg.header.source_id, key, msg.message))

    def on_actor_control_message(self, msg: message.ActorControlMessage):
        try:
            key = ActorControlId(msg.id).name
        except ValueError:
            key = msg.id
        self.nl.append_data(net_log_imgui.ActorControlIpc(
            self.nl, msg.raw_msg.raw_message.bundle_header.timestamp_ms,
            msg.source_id, key, msg.param or msg.args, target_id=msg.target_id,
        ))

    def reset(self):
        self.nl = net_log_imgui.NetLogger(self.main.sq_pack, self.get_actor)
        self.actor_cache = {}

    def _get_actor(self, actor_id):
        if actor_id in self.actor_cache:
            actor = self.actor_cache[actor_id]
            try:
                if actor.id == actor_id: return actor
            except:  # maybe memory is free, or actor change
                pass
        if actor := self.main.mem.actor_table.get_actor_by_id(actor_id):
            self.actor_cache[actor_id] = actor
        return actor

    def get_actor(self, actor_id):
        if not actor_id or actor_id == 0xe0000000: return None
        if actor := self._get_actor(actor_id):
            return net_log_imgui.ActorDef(actor_id, actor.base_id, actor.name)
        return net_log_imgui.ActorDef(actor_id, 0, '?')

    def draw_panel(self):
        if imgui.button('Reset'): self.reset()
        with imgui_ctx.Child('NL', 0, 0):
            self.nl.render()
