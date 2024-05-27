import ctypes
import struct
from ffd_plus.api.framework import Framework
from ffd_plus.api.control import Control
from ff_draw.sniffer.message_structs import zone_server, zone_client, chat_server, chat_client
from ff_draw.sniffer.message_structs import ZoneServer, ZoneClient, ChatServer, ChatClient, ActorControlId
from ff_draw.sniffer.sniffer_main import Sniffer

zone_proto_no = Sniffer.instance.zone_client_pno
chat_proto_no = Sniffer.instance.chat_client_pno


def build_event_start(handler_id, target_common_id=None):
    if target_common_id is None:
        if me := Control.instance.control_character:
            target_common_id = me.common_id
        else:
            raise ValueError('target_common_id is None and no control character')
    pkt = zone_client.EventStart()
    pkt.handler_id = handler_id
    pkt.target_common_id = target_common_id
    return packet_builder(zone_proto_no['EventStart'][0], pkt)


def build_event_finish(handler_id, scene_id, error=0, *args):
    arg_cnt = len(args)
    n = next(i for i in [2, 4, 8, 16, 32, 64, 128, 255] if arg_cnt <= i)
    buffer = ctypes.create_string_buffer(0x8 + n * 4)
    pkt = ctypes.cast(buffer, ctypes.POINTER(zone_client.EventFinish)).contents
    pkt.handler_id = handler_id
    pkt.scene_id = scene_id
    pkt.error = error
    pkt.arg_cnt = arg_cnt
    for i, arg in enumerate(args): pkt._args[i] = arg
    return packet_builder(zone_proto_no[f'EventFinish{n if n !=2 else ""}'][0], bytes(buffer), 0x8 + n * 4)


def build_event_action(handler_id, scene_id, res=0, *args):
    arg_cnt = len(args)
    n = next(i for i in [2, 4, 8, 16, 32, 64, 128, 255] if arg_cnt <= i)
    buffer = ctypes.create_string_buffer(0x8 + n * 4)
    pkt = ctypes.cast(buffer, ctypes.POINTER(zone_client.EventAction)).contents
    pkt.handler_id = handler_id
    pkt.scene_id = scene_id
    pkt.res = res
    pkt.arg_cnt = arg_cnt
    for i, arg in enumerate(args): pkt._args[i] = arg
    return packet_builder(zone_proto_no[f'EventAction{n if n !=2 else ""}'][0], bytes(buffer), 0x8 + n * 4)


def build_client_trigger(trigger_id, arg0=0, arg1=0, arg2=0, arg3=0, target_common_id=0):
    pkt = zone_client.ClientTrigger()
    pkt.id = trigger_id
    pkt.arg0 = arg0
    pkt.arg1 = arg1
    pkt.arg2 = arg2
    pkt.arg3 = arg3
    pkt.target_common_id = target_common_id
    return packet_builder(zone_proto_no['ClientTrigger'][0], pkt)


def build_inventory_handler(context_id, operation_type, src_entity, src_storage_id, src_container_index, src_cnt, src_item_id, dst_entity, dst_storage_id, dst_container_index, dst_cnt, dst_item_id):
    pkt = zone_client.InventoryModifyHandler()
    pkt.context_id = context_id
    pkt.operation_type = operation_type
    pkt.src_entity = src_entity
    pkt.src_storage_id = src_storage_id
    pkt.src_container_index = src_container_index
    pkt.src_cnt = src_cnt
    pkt.src_item_id = src_item_id
    pkt.dst_entity = dst_entity
    pkt.dst_storage_id = dst_storage_id
    pkt.dst_container_index = dst_container_index
    pkt.dst_cnt = dst_cnt
    pkt.dst_item_id = dst_item_id
    return packet_builder(zone_proto_no['InventoryModifyHandler'][0], pkt)


def add_black_proto_shell(is_zone, key='hook_sniff'):
    return f'''
def work():
    if hasattr(inject_server, {key!r}):
        h = getattr(inject_server, {key!r})[{3 if is_zone else 2}]
        h.proto_no_to_block_recv.update(args[0])
        return h.proto_no_to_block_recv
res = work()
'''


def remove_black_proto_shell(is_zone, key='hook_sniff'):
    return f'''
def work():
    if hasattr(inject_server, {key!r}):
        h = getattr(inject_server, {key!r})[{3 if is_zone else 2}]
        h.proto_no_to_block_recv.difference_update(args[0])
        return h.proto_no_to_block_recv
res = work()
'''


def get_black_proto_shell(is_zone, key='hook_sniff'):
    return f'''
def work():
    if hasattr(inject_server, {key!r}):
        h = getattr(inject_server, {key!r})[{3 if is_zone else 2}]
        return h.proto_no_to_block_recv
res = work()
'''


def packet_builder(proto_no, data: bytes | ctypes.Structure, data_size: int = None):
    if isinstance(data, ctypes.Structure): data = bytes(data)
    if data_size is None:
        data_size = len(data)
    else:
        data = data[:data_size]
    return struct.pack(b'IIQ', proto_no, 0, data_size + 16) + b'\0' * 16 + data


def send_zone_packet(*packet_datas: bytes, immediate=False):
    c = Framework.instance.network_module.zone_client_module.push_send_packet
    for packet_data in packet_datas: c(packet_data, 0, 0, immediate)


def send_chat_packet(*packet_datas: bytes, immediate=False):
    c = Framework.instance.network_module.chat_client_module.push_send_packet
    for packet_data in packet_datas: c(packet_data, 0, 0, immediate)
