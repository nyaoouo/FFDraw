import ctypes
import logging
import zlib
from typing import Iterable

from nylib.utils import serialize_data
from .message import BaseMessage
from .oodle import Oodle
from .structs import BundleHeader, ElementHeader, CompressType

MAGIC_PREFIX = b'\x52\x52\xA0\x41\xFF\x5D\x46\xE2\x7F\x2A\x64\x4D\x7B\x99\xC4\x75'
prefix_len = len(MAGIC_PREFIX)
header_size = ctypes.sizeof(BundleHeader)
packet_header_offset = BundleHeader.size.offset
el_header_size = ctypes.sizeof(ElementHeader)
logger = logging.getLogger('Bundle')


def unpack_message(data: bytearray, oodle: Oodle = None):
    header = BundleHeader.from_buffer_copy(data)
    if header.compress_type == CompressType.none.value:
        raw_messages = data
        msg_offset = header_size
    elif header.compress_type == CompressType.zip.value:
        raw_messages = bytearray(zlib.decompress(data[header_size + 2:header.size], wbits=-zlib.MAX_WBITS))
        msg_offset = 0
    elif header.compress_type == CompressType.oodle.value:
        if oodle is None: raise ValueError('Oodle is not provided')
        raw_messages = oodle.decompress(data[header_size:header.size], header.size_before_compress)
        msg_offset = 0
    else:
        raise TypeError(f'Unknown packet compression type: {header.compress_type}')
    for i in range(header.element_count):
        el_header = ElementHeader.from_buffer_copy(raw_messages, msg_offset)
        yield header, el_header, raw_messages[msg_offset + el_header_size:msg_offset + el_header.size]
        msg_offset += el_header.size


def pack_message(header: BundleHeader, messages: Iterable[bytearray], oodle: Oodle = None):
    raw_message = bytearray()
    cnt = 0
    for message in messages:
        if message:
            raw_message.extend(message)
            cnt += 1
    if not cnt: return raw_message
    header.size_before_compress = len(raw_message)
    if header.compress_type == CompressType.none.value:
        pass
    elif header.compress_type == CompressType.zip.value:
        raw_message = zlib.compress(raw_message)
    elif header.compress_type == CompressType.oodle.value:
        if oodle is None: raise ValueError('Oodle is not provided')
        raw_message = oodle.compress(raw_message)
    else:
        raise TypeError(f'Unknown packet compression type:{header.compress_type}')
    header.element_count = cnt
    header.size = header_size + len(raw_message)
    return bytearray(header) + raw_message


def decode(buffer: bytearray, oodle: Oodle = None):
    while (buffer_len := len(buffer)) > 0:
        prefix = buffer[:prefix_len]
        if buffer_len < packet_header_offset + 4:
            if any(buffer) and not MAGIC_PREFIX.startswith(prefix):
                buffer.clear()
            return
        if any(prefix) and prefix != MAGIC_PREFIX:
            reset_buffer(buffer)
            continue
        packet_size = int.from_bytes(buffer[packet_header_offset:packet_header_offset + 4], byteorder='little')
        if packet_size <= header_size:
            reset_buffer(buffer)
            continue
        if packet_size > buffer_len:
            return
        try:
            for bundle_header, el_header, bundle_data in unpack_message(buffer, oodle):
                yield BaseMessage(bundle_header, el_header, bundle_data)
        except Exception as e:
            logger.warning(f'error in unpacking message', exc_info=e)
        finally:
            del buffer[:packet_size]


def reset_buffer(buffer: bytearray):
    try:
        del buffer[:buffer.index(MAGIC_PREFIX, 1)]
    except ValueError:
        buffer.clear()
