import logging
import multiprocessing
import os
import pathlib
import queue
import sys
import threading
import time
import traceback
import typing

import imgui

from nylib.utils import serialize_data, KeyRoute, BroadcastHook
from nylib.utils.win32.network import find_process_tcp_connections
from ff_draw.utils import EvtQueue
from . import enums, extra, message_dump, hook_sniff
from .message_structs import zone_server, zone_client, chat_server, chat_client
from .utils import message, structs, simple, bundle, oodle

if typing.TYPE_CHECKING:
    from ff_draw.main import FFDraw


class GameMessageBuffer:
    def __init__(self, oodle_type: typing.Type[oodle.Oodle]):
        self.oodle = oodle_type()
        self.buffer = bytearray()

    def feed(self, data: bytes):
        self.buffer.extend(data)
        yield from bundle.decode(self.buffer, self.oodle)


class KeyRouteWithMap(KeyRoute):
    def __init__(self, get_key=lambda v: v, get_map=lambda v: v):
        super().__init__(get_key)
        self.get_map = get_map

    def __getitem__(self, item):
        return super().__getitem__(self.get_map(item))


class Sniffer:
    target: tuple[str, int] = None
    logger = logging.getLogger('Sniffer')
    dump: message_dump.MessageDumper | None = None
    instance: 'Sniffer' = None

    def __init__(self, main: 'FFDraw'):
        assert Sniffer.instance is None, 'Sniffer instance already exists'
        Sniffer.instance = self
        self.main = main
        self.ipc_lock = threading.Lock()

        self.config = self.main.config.setdefault('sniffer', {})
        self.print_packets = self.config.setdefault('print_packets', False)
        self.print_actor_control = self.config.setdefault('print_actor_control', False)
        self.sniff_promisc = self.config.setdefault('sniff_promisc', True)
        self.dump_pkt = self.config.setdefault('dump_pkt', False)
        self.dump_zone_down_only = self.config.setdefault('dump_zone_down_only', True)

        pno_dir = pathlib.Path(os.environ['ExcPath']) / 'res' / 'proto_no'

        self._chat_server_pno_map, self.chat_server_pno = simple.load_pno_map(pno_dir / 'ChatServerIpc.csv', self.main.mem.game_build_date, enums.ChatServer)
        self._chat_client_pno_map, self.chat_client_pno = simple.load_pno_map(pno_dir / 'ChatClientIpc.csv', self.main.mem.game_build_date, enums.ChatClient)
        self._zone_server_pno_map, self.zone_server_pno = simple.load_pno_map(pno_dir / 'ZoneServerIpc.csv', self.main.mem.game_build_date, enums.ZoneServer)
        self._zone_client_pno_map, self.zone_client_pno = simple.load_pno_map(pno_dir / 'ZoneClientIpc.csv', self.main.mem.game_build_date, enums.ZoneClient)
        self._chat_server_pno_map_size = len(self._chat_server_pno_map)
        self._chat_client_pno_map_size = len(self._chat_client_pno_map)
        self._zone_server_pno_map_size = len(self._zone_server_pno_map)
        self._zone_client_pno_map_size = len(self._zone_client_pno_map)

        self.on_chat_server_message = KeyRouteWithMap(lambda m: m.proto_no, lambda k: self._chat_server_pno_map.get(k, k))
        self.on_chat_client_message = KeyRouteWithMap(lambda m: m.proto_no, lambda k: self._chat_client_pno_map.get(k, k))
        self.on_zone_server_message = KeyRouteWithMap(lambda m: m.proto_no, lambda k: self._zone_server_pno_map.get(k, k))
        self.on_zone_client_message = KeyRouteWithMap(lambda m: m.proto_no, lambda k: self._zone_client_pno_map.get(k, k))
        self.on_actor_control = KeyRoute(lambda m: m.id)
        self.on_action_effect = BroadcastHook()
        self.on_add_status_by_action = BroadcastHook()
        self.on_play_action_timeline = BroadcastHook()
        self.on_reset = BroadcastHook()

        self.packet_fix = self.main.mem.packet_fix

        self.oodles = {}
        self.buffers = {}
        self.extra = extra.SnifferExtra(self)

        self.update_dump()
        self.evt_queue = EvtQueue(self._on_ipc_message)

    def update_dump(self):
        if self.dump:
            self.dump.close()
            self.dump = None
        if self.dump_pkt:
            file_name = self.main.app_data_path / 'dump_pkt' / time.strftime("dump_%Y_%m_%d_%H_%M_%S.dmp")
            self.dump = message_dump.MessageDumper(file_name, self.main.mem.game_build_date)
            self.logger.info(f'dump packets at {file_name}')

    def _on_evt_queue_timeout(self, args, time_, q):
        is_zone, is_up, msg = args
        try:
            self.logger.warning(f'parse ipc {is_zone=} {is_up=} {msg.element.proto_no=} run for {time_:.3f}s, for blocking event, please use async method\n' + ''.join(
                traceback.format_stack(sys._current_frames()[self.evt_queue.msg_loop_thread.ident])[10:]
            ))
        except Exception as e:
            self.logger.warning(f'exception when get overtime stack', exc_info=e)

    def _on_ipc_message(self, is_zone, is_up, msg):
        fix_value = None
        if self.dump and ((not self.dump_zone_down_only) or (is_zone and not is_up)):
            self.dump.write(msg.bundle_header.timestamp_ms, is_zone, is_up, msg.element.proto_no, msg.el_header.source_id, msg.raw_data[16:], fix_value := self.packet_fix.value)
        with self.ipc_lock:
            if is_zone:
                if is_up:
                    pno_map = self._zone_client_pno_map
                    call = self.on_zone_client_message
                    type_map = zone_client.type_map
                else:
                    pno_map = self._zone_server_pno_map
                    call = self.on_zone_server_message
                    type_map = zone_server.type_map
            else:
                if is_up:
                    pno_map = self._chat_client_pno_map
                    call = self.on_chat_client_message
                    type_map = chat_client.type_map
                else:
                    pno_map = self._chat_server_pno_map
                    call = self.on_chat_server_message
                    type_map = chat_server.type_map

            data = msg.raw_data
            if (pno := msg.element.proto_no) in pno_map:
                pno = pno_map[pno]
                if t := type_map.get(pno):
                    msg = msg.to_ipc(t)
                    data = msg.message
                    if hasattr(t, '_pkt_fix'):
                        data._pkt_fix(self.packet_fix.value if fix_value is None else fix_value)
            try:
                evt = message.NetworkMessage(proto_no=pno, raw_message=msg, header=msg.el_header, message=data)
                if self.print_packets:
                    source_name = getattr(self.main.mem.actor_table.get_actor_by_id(evt.header.source_id), 'name', None)
                    self.logger.debug(f'{"Zone" if is_zone else "Chat"}{"Client" if is_up else "Server"}[{pno}] {source_name}#{evt.header.source_id:x} {serialize_data(data)}')
                # self.logger.debug(f'{is_zone} {is_up} {evt.proto_no} {call.route.get(evt.proto_no)}')
                call(evt)
            except Exception as e:
                self.logger.error(f'error in processing network message {pno}', exc_info=e)

    def on_ipc_message(self, is_zone, is_up, msg: message.ElementMessage[structs.IpcHeader]):
        self.evt_queue.put(is_zone, is_up, msg)

    def start(self):
        hook_sniff.install()

    def render_panel(self):
        imgui.text(f'fix:{self.packet_fix.value}')
        imgui.text(f'load pno: chat_server[{self._chat_server_pno_map_size}] chat_client[{self._chat_client_pno_map_size}] zone_server[{self._zone_server_pno_map_size}] zone_client[{self._zone_client_pno_map_size}]')
        clicked, self.print_packets = imgui.checkbox("print_packets", self.print_packets)
        if clicked:
            self.config['print_packets'] = self.print_packets
            self.main.save_config()
        clicked, self.print_actor_control = imgui.checkbox("print_actor_control", self.print_actor_control)
        if clicked:
            self.config['print_packets'] = self.print_packets
            self.main.save_config()
        clicked, self.dump_pkt = imgui.checkbox("dump_pkt", self.dump_pkt)
        if clicked:
            self.config['dump_pkt'] = self.dump_pkt
            self.update_dump()
            self.main.save_config()
        if self.dump_pkt:
            clicked, self.dump_zone_down_only = imgui.checkbox("dump_zone_down_only", self.dump_zone_down_only)
            if clicked:
                self.config['dump_zone_down_only'] = self.dump_zone_down_only
                self.main.save_config()
        clicked, self.auto_update = imgui.checkbox("auto_update", self.auto_update)
        if clicked:
            self.config['auto_update'] = self.auto_update
            self.main.save_config()
        if self.auto_update:
            is_update, self.auto_update_host = imgui.input_text('auto_update_host', self.auto_update_host, 256)
            if is_update:
                self.config['auto_update_host'] = self.auto_update_host
                self.main.save_config()
