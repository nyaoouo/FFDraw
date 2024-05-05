import traceback

from nylib.hook import Hook
import ctypes
import struct

mv_from_mem = ctypes.pythonapi.PyMemoryView_FromMemory
mv_from_mem.argtypes = (ctypes.c_void_p, ctypes.c_ssize_t, ctypes.c_int)
mv_from_mem.restype = ctypes.py_object


class PopRecvHook(Hook):
    def __init__(self, address, is_zone, cb):
        self.is_zone = is_zone
        self.cb = cb
        self.proto_no_to_block_recv = set()
        super().__init__(
            address, self.on_pop_recv, ctypes.c_char,
            [ctypes.c_int64, ctypes.POINTER(ctypes.c_void_p)]
        )

    def on_pop_recv(self, hook_, p_module, pkt):
        res = 0
        try:
            while (res := hook_.original(p_module, pkt)) and (ptr := pkt[2]):
                _ptr = ctypes.cast(ptr, ctypes.c_void_p).value
                _ptr += 0x20
                src_id = ctypes.c_uint.from_address(_ptr).value
                data_size = ctypes.c_uint64.from_address(_ptr + 16).value
                data_ptr = ctypes.c_void_p.from_address(_ptr + 24).value
                proto_no = ctypes.c_ushort.from_address(data_ptr + 2).value
                data = bytearray(mv_from_mem(data_ptr + 16, data_size - 16, 0x100))
                self.cb(self.is_zone, False, proto_no, src_id, data)
                if proto_no not in self.proto_no_to_block_recv: break
        except Exception:
            ctypes.windll.user32.MessageBoxW(
                0,
                f"sniffer_error (is_zone:{self.is_zone}, is_up:False)\n" + traceback.format_exc(),
                "sniffer_error", 0x10
            )
        return res


class PushSendHook(Hook):
    def __init__(self, address, is_zone, cb):
        self.is_zone = is_zone
        self.cb = cb
        self.proto_no_to_block_send = set()
        self.me_id = ctypes.c_uint32.from_address(me_id_addr)
        super().__init__(
            address, self.on_push_send, ctypes.c_char,
            [ctypes.c_int64, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_char]
        )

    def on_push_send(self, hook_, p_module, pkt, a3, a4, a5):
        try:
            ptr = ctypes.cast(pkt, ctypes.c_void_p).value
            proto_no, unk, size = struct.unpack(b'IIQ', mv_from_mem(ptr, 16, 0x100))
            self.cb(self.is_zone, True, proto_no, self.me_id.value, bytearray(mv_from_mem(ptr + 32, size, 0x100)))
            if proto_no in self.proto_no_to_block_send: return 1
        except Exception:
            ctypes.windll.user32.MessageBoxW(
                0,
                f"sniffer_error (is_zone:{self.is_zone}, is_up:True)\n" + traceback.format_exc(),
                "sniffer_error", 0x10
            )
        return hook_.original(p_module, pkt, a3, a4, a5)


class ReplayPopPacketHook(Hook):
    def __init__(self, address, cb):
        self.cb = cb
        super().__init__(
            address, self.on_replay_pop_packet, ctypes.c_size_t,
            [ctypes.c_size_t]
        )

    def on_replay_pop_packet(self, hook_, a1):
        if res := hook_.original(a1):
            try:
                proto_no, size, timestamp, src_id = struct.unpack(b'2H2I', mv_from_mem(res, 0xc, 0x100))
                self.cb(True, False, proto_no, src_id, bytearray(mv_from_mem(res + 0xc, size, 0x100)))
            except Exception:
                ctypes.windll.user32.MessageBoxW(
                    0, f"sniffer_error (replay recv)\n" + traceback.format_exc(),
                    "sniffer_error", 0x10
                )
        return res


class ReplayParsePacketHook(Hook):
    def __init__(self, address, cb):
        self.cb = cb
        super().__init__(address, self.on_replay_parse_packet, ctypes.c_void_p, [
            ctypes.c_size_t, ctypes.c_size_t, ctypes.c_size_t
        ])

    def on_replay_parse_packet(self, hook_, a1, p_header, p_data):
        try:
            proto_no, size, timestamp, src_id = struct.unpack(b'2H2I', mv_from_mem(p_header, 0xc, 0x100))
            self.cb(True, False, proto_no, src_id, bytearray(mv_from_mem(p_data, size, 0x100)))
        except Exception:
            ctypes.windll.user32.MessageBoxW(
                0, f"sniffer_error (replay recv)\n" + traceback.format_exc(),
                "sniffer_error", 0x10
            )
        return hook_.original(a1, p_header, p_data)


chat_pop_recv_packet_addr: int
zone_pop_recv_packet_addr: int
chat_push_send_packet_addr: int
zone_push_send_packet_addr: int
# replay_pop_load_packet_addr: int
replay_parse_packet_addr: int
me_id_addr: int

install = lambda cb: [
    h.install_and_enable() for h in
    (
        PopRecvHook(chat_pop_recv_packet_addr, False, cb),
        PopRecvHook(zone_pop_recv_packet_addr, True, cb),
        PushSendHook(chat_push_send_packet_addr, False, cb),
        PushSendHook(zone_push_send_packet_addr, True, cb),
        # ReplayPopPacketHook(replay_pop_load_packet_addr, cb),
        ReplayParsePacketHook(replay_parse_packet_addr, cb)
    )
]
