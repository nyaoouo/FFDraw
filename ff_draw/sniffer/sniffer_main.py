import logging
import multiprocessing
import os
import pathlib
import threading
import time
import typing
from nylib.utils import serialize_data, KeyRoute, BroadcastHook
from nylib.utils.win32.network import find_process_tcp_connections
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


class Sniffer:
    target: tuple[str, int] = None
    logger = logging.getLogger('Sniffer')
    dump: message_dump.MessageDumper | None = None

    def __init__(self, main: 'FFDraw'):
        self.main = main
        self.ipc_lock = threading.Lock()

        self.config = self.main.config.setdefault('sniffer', {})
        self.print_packets = self.config.setdefault('print_packets', False)
        self.print_actor_control = self.config.setdefault('print_actor_control', False)
        self.sniff_promisc = self.config.setdefault('sniff_promisc', True)
        self.dump_pkt = self.config.setdefault('dump_pkt', False)
        self.dump_zone_down_only = self.config.setdefault('dump_zone_down_only', True)

        pno_dir = pathlib.Path(os.environ['ExcPath']) / 'res' / 'proto_no'
        self._chat_server_pno_map = simple.load_pno_map(pno_dir / 'ChatServerIpc.csv', self.main.mem.game_build_date, enums.ChatServer)
        self._chat_client_pno_map = simple.load_pno_map(pno_dir / 'ChatClientIpc.csv', self.main.mem.game_build_date, enums.ChatClient)
        self._zone_server_pno_map = simple.load_pno_map(pno_dir / 'ZoneServerIpc.csv', self.main.mem.game_build_date, enums.ZoneServer)
        self._zone_client_pno_map = simple.load_pno_map(pno_dir / 'ZoneClientIpc.csv', self.main.mem.game_build_date, enums.ZoneClient)

        self.on_chat_server_message = KeyRoute(lambda m: m.proto_no)
        self.on_chat_client_message = KeyRoute(lambda m: m.proto_no)
        self.on_zone_server_message = KeyRoute(lambda m: m.proto_no)
        self.on_zone_client_message = KeyRoute(lambda m: m.proto_no)
        self.on_actor_control = KeyRoute(lambda m: m.id)
        self.on_action_effect = BroadcastHook()
        self.on_play_action_timeline = BroadcastHook()

        self.packet_fix = self.main.mem.packet_fix

        self.oodles = {}
        self.buffers = {}
        self.extra = extra.SnifferExtra(self)

        self.update_dump()

    def update_dump(self):
        if self.dump:
            self.dump.close()
            self.dump = None
        if self.dump_pkt:
            file_name = self.main.app_data_path / 'dump_pkt' / time.strftime("dump_%Y_%m_%d_%H_%M_%S.dmp")
            self.dump = message_dump.MessageDumper(file_name, self.main.mem.game_build_date)
            self.logger.info(f'dump packets at {file_name}')


    def _on_ipc_message(self, is_zone, is_up, msg: message.ElementMessage[structs.IpcHeader]):
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

    def start(self):
        hook_sniff.install()
