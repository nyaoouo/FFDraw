import json
import pathlib
import struct
import threading
import time

from . import enums
from .message_structs import zone_server, zone_client, chat_server, chat_client
from .utils import simple

empty_ipc = bytearray(16)


class MessageDumper:
    _ver_ = 0

    def __init__(self, file_name: pathlib.Path | str, game_build_date: str):
        if isinstance(file_name, str): file_name = pathlib.Path(file_name)
        assert not file_name.exists()
        file_name.parent.mkdir(exist_ok=True, parents=True)
        self.file_name = file_name
        self.game_build_date = game_build_date
        self.handle = open(file_name, 'wb', buffering=0)
        self.handle.write(json.dumps(self.get_header(), ensure_ascii=False).encode('utf-8') + b'\n')
        self.write_lock = threading.Lock()

    def get_header(self):
        return {
            'dumper_version': self._ver_,
            'game_build_date': self.game_build_date,
            'start_log_time': int(time.time() * 1000),
        }

    def write(self, timestamp_ms: int, is_zone: bool, is_up: bool, proto_no: int, source_id: int, data: bytes, fix_value=0):
        to_write = struct.pack(b'BBHIQI',((int(is_zone) << 1) | int(is_up)) , fix_value, proto_no, source_id, timestamp_ms, len(data)) + data
        with self.write_lock: self.handle.write(to_write)

    def close(self):
        self.handle.close()
        self.handle = None

    @classmethod
    def parse(cls, file_name: pathlib.Path | str, pno_dir: pathlib.Path | str):
        if isinstance(file_name, str): file_name = pathlib.Path(file_name)
        if isinstance(pno_dir, str): pno_dir = pathlib.Path(pno_dir)

        assert file_name.exists()
        with open(file_name, 'rb') as buf:
            header = json.loads(buf.readline().decode('utf-8'))
            assert isinstance(header, dict) and header['dumper_version'] == cls._ver_
            game_build_date = header['game_build_date']
            chat_server_pno_map = simple.load_pno_map(pno_dir / 'ChatServerIpc.csv', game_build_date, enums.ChatServer)
            chat_client_pno_map = simple.load_pno_map(pno_dir / 'ChatClientIpc.csv', game_build_date, enums.ChatClient)
            zone_server_pno_map = simple.load_pno_map(pno_dir / 'ZoneServerIpc.csv', game_build_date, enums.ZoneServer)
            zone_client_pno_map = simple.load_pno_map(pno_dir / 'ZoneClientIpc.csv', game_build_date, enums.ZoneClient)

            while True:
                if not (header_bytes := buf.read(20)): break

                scope, fix_value, proto_no, source_id, timestamp_ms, size = struct.unpack(b'BBHIQI', header_bytes)
                data = buf.read(size)

                is_zone = scope & 0b10 > 0
                is_up = scope & 0b1 > 0
                if is_zone:
                    if is_up:
                        pno_map = zone_client_pno_map
                        type_map = zone_client.type_map
                    else:
                        pno_map = zone_server_pno_map
                        type_map = zone_server.type_map
                else:
                    if is_up:
                        pno_map = chat_client_pno_map
                        type_map = chat_client.type_map
                    else:
                        pno_map = chat_server_pno_map
                        type_map = chat_server.type_map
                if proto_no in pno_map:
                    proto_no = pno_map[proto_no]
                    if t := type_map.get(proto_no):
                        data = t.from_buffer_copy(data)
                        if hasattr(t, '_pkt_fix'):
                            data._pkt_fix(fix_value)
                    proto_no = proto_no.name

                yield is_zone, is_up, proto_no, source_id, timestamp_ms, data
