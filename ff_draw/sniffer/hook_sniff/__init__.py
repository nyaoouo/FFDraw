def install(key='hook_sniff'):
    import time
    import pathlib

    from ff_draw.main import FFDraw
    from ff_draw.sniffer.utils import message

    main = FFDraw.instance

    chat_pop_recv_packet_addr, = main.mem.scanner.find_point("e8 * * * * 84 ? 74 ? 66 66 0f 1f 84 00")
    zone_pop_recv_packet_addr, = main.mem.scanner.find_point("48 ? ? ? ? 4c 89 6c 24 ? 4c 89 6c 24 ? e8 * * * * 84")
    chat_push_send_packet_addr, = main.mem.scanner.find_point("e8 * * * * 48 ? ? ? ? 0f ? ? e8 ? ? ? ? 48 ? ? ? e8 ? ? ? ? 0f")
    zone_push_send_packet_addr, = main.mem.scanner.find_point("e8 * * * * 84 ? 74 ? 48 ? ? c7 87")
    # replay_pop_load_packet_addr, = main.mem.scanner.find_point("e8 * * * * 48 ? ? 48 ? ? 0f 84 ? ? ? ? 8b ? ? 0f ? ? 0f")
    replay_parse_packet_addr, = main.mem.scanner.find_point("e8 * * * * 80 bb ? ? ? ? ? 77")
    me_id_addr, = main.mem.scanner.find_point("39 15 * * * * 49")
    empty_ipc = bytearray(16)

    def callback(_, args):
        is_zone, is_up, pno, src_id, data = args
        main.sniffer.on_ipc_message(is_zone, is_up, message.ElementMessage(
            bundle_header=message.BundleHeader(timestamp_ms=int(time.time() * 1000)),
            el_header=message.ElementHeader(source_id=src_id),
            element=message.IpcHeader(proto_no=pno),
            raw_data=empty_ipc + data,
        ))

    main.mem.inject_handle.client.subscribe(key, callback)
    shell = (pathlib.Path(__file__).parent / 'shell.py').read_text(encoding='utf-8') + f'''
chat_pop_recv_packet_addr = {chat_pop_recv_packet_addr}
zone_pop_recv_packet_addr = {zone_pop_recv_packet_addr}
chat_push_send_packet_addr = {chat_push_send_packet_addr}
zone_push_send_packet_addr = {zone_push_send_packet_addr}
replay_parse_packet_addr = {replay_parse_packet_addr}
me_id_addr = {me_id_addr} 
def try_hook():
    if hasattr(inject_server, {key!r}):
        for h in getattr(inject_server, {key!r}):
            h.uninstall()
        delattr(inject_server, {key!r})
    if not hasattr(inject_server, {key!r}):
        setattr(inject_server, {key!r}, install(
            lambda is_zone, is_up, pno, src_id, data: inject_server.push_event('hook_sniff', (is_zone, is_up, pno, src_id, data))
        ))
        return len(inject_server.hook_sniff)
    return 0


res = try_hook()
'''
    install_cnt = main.mem.inject_handle.run(shell)
    main.logger.info(f'sniff hook install:{install_cnt}')
