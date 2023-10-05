import datetime

import imgui

from ff_draw.plugins import FFDrawPlugin
from ff_draw.sniffer.utils import message
from ff_draw.sniffer.enums import ZoneServer, ActorControlId, ZoneClient
from nylib.utils.imgui import ctx as imgui_ctx, dumb_button_style
from . import net_log_imgui

actor_controls = ZoneServer.ActorControl, ZoneServer.ActorControlSelf, ZoneServer.ActorControlTarget


class NetLog(FFDrawPlugin):
    def __init__(self, main):
        super().__init__(main)
        self.nls = [(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), net_log_imgui.NetLogger(self.main.sq_pack, self.get_actor))]
        self.display_nl = 0
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
        if msg.proto_no == ZoneServer.ActorMove or msg.proto_no == ZoneServer.ActorSetPos:
            actor = self.get_actor(msg.header.source_id)
            actor.pos = msg.message.pos
            actor.facing = msg.message.facing
        if msg.proto_no == ZoneServer.PingRes:
            return #  don't record pings
        key = msg.proto_no if isinstance(msg.proto_no, int) else msg.proto_no.name
        self.nl.append_data(net_log_imgui.ZoneServerIpc(self.nl, msg.raw_message.bundle_header.timestamp_ms, msg.header.source_id, key, msg.message))

    def on_zone_client_message(self, msg: message.NetworkMessage):
        if msg.proto_no == ZoneClient.UpdatePositionHandler or msg.proto_no == ZoneClient.UpdatePositionInstance:
            actor = self.get_actor(msg.header.source_id)
            actor.pos = msg.message.pos
            actor.facing = msg.message.facing
            return  # don't record send change pos packet, because it's too many
        if msg.proto_no == ZoneClient.PingReq:
            return  # don't record pings
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
        self.nls.append((datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), net_log_imgui.NetLogger(self.main.sq_pack, self.get_actor)))
        self.display_nl = len(self.nls) - 1
        self.actor_cache.clear()

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
            return net_log_imgui.ActorDef(actor_id, actor.base_id, actor.name, actor.pos, actor.facing)
        return net_log_imgui.ActorDef(actor_id, 0, '?')

    @property
    def nl(self):
        return self.nls[-1][1]

    def draw_panel(self):

        style = imgui.get_style()

        imgui.columns(2, 'NetLog', False)
        imgui.set_column_width(0, imgui.calc_text_size('2000-01-01 00:00:00')[0] + style.window_padding[0] * 6)
        with imgui_ctx.Child('History', 0, 0, border=False):
            main_height = imgui.get_window_height() - style.window_padding[1] * 4 - imgui.get_text_line_height_with_spacing()
            with imgui_ctx.Child('HistoryMain', 0, main_height, border=True):
                for i, (t, nl) in enumerate(self.nls):
                    if i == self.display_nl:
                        with imgui_ctx.StyleColor(imgui.COLOR_BUTTON, 0, 0, 0, 0), imgui_ctx.StyleColor(imgui.COLOR_TEXT, 0, 1, 0, 1), dumb_button_style():
                            imgui.button(f'{t}##sel_{i}', -1)
                    else:
                        if imgui.button(f'{t}##sel_{i}', -1):
                            self.display_nl = i
            if imgui.button('Reset', -1): self.reset()
        imgui.next_column()
        with imgui_ctx.Child('NL', 0, 0):
            self.nls[self.display_nl][1].render()
        imgui.next_column()
        imgui.columns(1, 'NetLog')
