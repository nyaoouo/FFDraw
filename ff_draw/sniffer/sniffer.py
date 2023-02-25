import bisect
import ipaddress
import logging
import multiprocessing.connection
import threading
import typing

import numpy as np  # use to avoid warning in subprocess
from nylib.logging import install
from nylib.utils import wait_until

if typing.TYPE_CHECKING:
    from scapy.all import AsyncSniffer


class TcpBuffer:
    def __init__(self):
        self.buffer = bytearray()
        self._buffer = bytearray()
        self.is_init = False
        self.end_seq = None
        self.to_put = []

    def put(self, seq, is_push, data):
        if not self.is_init:
            self.is_init = True
            self.end_seq = seq + len(data)
            if is_push:
                self.buffer = bytearray(data)
                return True
            else:
                self._buffer = bytearray(data)
                return False

        bisect.insort(self.to_put, (seq, is_push, data))
        has_push = False
        must_push = sum(len(data) for seq, is_push, data in self.to_put) > 1024 * 1024 * 5
        while self.to_put:
            seq, is_push, data = self.to_put.pop(0)
            if seq < self.end_seq:
                continue
            if seq > self.end_seq:
                if must_push:
                    self.buffer.clear()
                    self._buffer.clear()
                    must_push = False
                else:
                    self.to_put.insert(0, (seq, is_push, data))
                    break
            self._buffer.extend(data)
            self.end_seq = seq + len(data)
            if is_push:
                self.buffer.extend(self._buffer)
                self._buffer.clear()
                has_push = True
        return has_push

    def __bool__(self):
        return bool(self.buffer or self._buffer or self.to_put)

    def __str__(self):
        return f'(buffer({len(self.buffer)}) _buffer({len(self._buffer)}) end={self.end_seq} to_put={[seq for seq, is_push, data in self.to_put]})'


def _sniffer_stop(sniff: 'AsyncSniffer'):
    try:
        wait_until(hasattr, 10, .1, sniff, 'stop_cb')
    except TimeoutError:
        SniffRunner.logger.warning('sniffer cant stop: no stop_cb found, a thread may be hangup')
    else:
        sniff.stop()


class SniffRunner:
    target: tuple[str, int] = None
    logger = logging.getLogger('SniffRunner')
    sniff: 'AsyncSniffer | None' = None

    def __init__(self, pipe: multiprocessing.connection.Connection):
        self.buffers = {}
        self.pipe = pipe

    def on_target_change(self, t: tuple[str, int] | None):
        from scapy.all import AsyncSniffer
        if self.sniff:
            if hasattr(self.sniff, 'stop_cb'):
                self.sniff.stop()
            else:
                threading.Thread(target=_sniffer_stop, args=(self.sniff,), daemon=True).start()
        self.sniff = None
        self.buffers.clear()
        if t:
            self.target = t
            host, port = t
            self.sniff = AsyncSniffer(prn=self.on_packet, filter=f'tcp and host {host} and port {port}')
            self.sniff.start()

    def on_packet(self, pkt):
        tcp_payload = pkt.payload.payload
        try:
            src = pkt['IP'].src
            dst = pkt['IP'].dst
        except IndexError:
            return
        if ipaddress.IPv4Address(src).is_global:
            if (src, tcp_payload.sport) != self.target:
                return
            is_up = False
            k = tcp_payload.dport
        elif ipaddress.IPv4Address(dst).is_global:
            if (dst, tcp_payload.dport) != self.target: return
            is_up = True
            k = tcp_payload.sport
        else:
            return

        is_fin = tcp_payload.flags & 1
        if not (is_fin or tcp_payload.payload.name == 'Raw'): return
        if tcp_payload.flags & 1:
            self.buffers.pop((k, True), None)
            self.buffers.pop((k, False), None)
            return
        buffer_key = (k, is_up)
        if buffer_key not in self.buffers:
            self.buffers[buffer_key] = buffer = TcpBuffer()
        else:
            buffer = self.buffers[buffer_key]
        if buffer.put(tcp_payload.seq, tcp_payload.flags & 0b1000 > 0, bytes(tcp_payload.payload)):
            self.pipe.send(('tcp_data', k, is_up, buffer.buffer))
            buffer.buffer.clear()

    def start(self):
        self.pipe.send(('ask_target',))
        while True:
            cmd, *args = self.pipe.recv()
            match cmd:
                case 'set_target':
                    self.on_target_change(args[0])


def start_sniff(pipe: multiprocessing.connection.Connection, sniff_promisc=True):
    install()
    try:
        from scapy.all import conf
        conf.sniff_promisc = sniff_promisc
        SniffRunner(pipe).start()
    except Exception as e:
        logging.error('error in sniff runner', exc_info=e)
