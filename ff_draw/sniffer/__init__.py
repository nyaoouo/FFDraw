import logging
import multiprocessing
import os
import pathlib
import typing
from nylib.utils import serialize_data, KeyRoute, BroadcastHook
from nylib.utils.win32.network import find_process_tcp_connections
from . import enums, sniffer, extra
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

    def __init__(self, main: 'FFDraw'):
        self.main = main

        self.config = self.main.config.setdefault('sniffer', {})
        self.print_packets = self.config.setdefault('print_packets', False)
        self.print_actor_control = self.config.setdefault('print_actor_control', False)
        self.sniff_promisc = self.config.setdefault('sniff_promisc', True)

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

        self.pipe, child_pipe = multiprocessing.Pipe()
        self.sniff_process = multiprocessing.Process(target=sniffer.start_sniff, args=(child_pipe, self.sniff_promisc), daemon=True)

        self.packet_fix = self.main.mem.packet_fix

        main.gui.timer.add_mission(self.update_tcp_target, 1, -1)
        main.gui.draw_update_call.add(self.update)
        self.oodles = {}
        self.buffers = {}
        self.extra = extra.SnifferExtra(self)

    def update(self, main):
        while self.pipe.poll(0):
            cmd, *args = self.pipe.recv()
            match cmd:
                case 'ask_target':
                    self.pipe.send(('set_target', self.target))
                case 'tcp_data':
                    key, is_up, data = args
                    if (_k := (key, is_up)) not in self.buffers:
                        self.buffers[_k] = buffer = GameMessageBuffer(oodle.OodleUdp)
                    else:
                        buffer = self.buffers[_k]
                    for msg in buffer.feed(data):
                        self._on_message(is_up, msg)

    def update_tcp_target(self):
        cnt = set()
        t = None
        for local_host, local_port, remote_host, remote_port in find_process_tcp_connections(self.main.mem.pid):
            if (t := (str(remote_host), remote_port)) in cnt: break
            cnt.add(t)
            t = None
        if t != self.target:
            self.buffers.clear()
            self.target = t
            self.pipe.send(('set_target', t))

    def _on_message(self, is_up, msg: message.BaseMessage):
        if msg.el_header.type != 3: return
        msg = msg.to_el(structs.IpcHeader)
        if (is_server := msg.element.timestamp_s != 10):  # is server
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
                    data._pkt_fix(self.packet_fix.value)
        try:
            evt = message.NetworkMessage(proto_no=pno, raw_message=msg, header=msg.el_header, message=data)
            if self.print_packets:
                source_name = getattr(self.main.mem.actor_table.get_actor_by_id(evt.header.source_id), 'name', None)
                self.logger.debug(f'{"Zone" if is_server else "Chat"}{"Client" if is_up else "Server"}[{pno}] {source_name}#{evt.header.source_id:x} {serialize_data(data)}')
            call(evt)
        except Exception as e:
            self.logger.error('error in processing network message', exc_info=e)

    def start(self):
        self.sniff_process.start()
