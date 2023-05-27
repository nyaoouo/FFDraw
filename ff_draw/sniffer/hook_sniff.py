shell_code = r'''

def hook_sniff(cb):
    from nylib.hook import create_hook
    import ctypes
    import struct
    import traceback
    mv_from_mem = ctypes.pythonapi.PyMemoryView_FromMemory
    mv_from_mem.argtypes = (ctypes.c_void_p, ctypes.c_ssize_t, ctypes.c_int)
    mv_from_mem.restype = ctypes.py_object

    me_id = ctypes.c_uint32.from_address(me_id_addr)

    def on_recv(is_zone):
        def func(_hook, a1, pkt):
            try:
                if (res := _hook.original(a1, pkt)) and (ptr := pkt[2]):
                    _ptr = ctypes.cast(ptr, ctypes.c_void_p).value
                    _ptr += 0x20
                    src_id = ctypes.c_uint.from_address(_ptr).value
                    data_size = ctypes.c_uint64.from_address(_ptr + 16).value
                    data_ptr = ctypes.c_void_p.from_address(_ptr + 24).value
                    proto_no = ctypes.c_ushort.from_address(data_ptr + 2).value
                    data = bytearray(mv_from_mem(data_ptr + 16, data_size - 16, 0x100))
                    cb(is_zone, False, proto_no, src_id, data)
                return res
            except Exception:
                ctypes.windll.user32.MessageBoxW(0, f"sniffer_error (is_zone:{is_zone}, is_up:False), will be uninstall\n{traceback.format_exc()}", "sniffer_error", 0x10)
                _hook.uninstall()
                return True

        return func

    def on_send(is_zone):
        def func(_hook, a1, pkt, a3, a4, a5):
            try:
                ptr = ctypes.cast(pkt, ctypes.c_void_p).value
                proto_no, unk, size = struct.unpack(b'IIQ', mv_from_mem(ptr, 16, 0x100))
                cb(is_zone, True, proto_no, me_id.value, bytearray(mv_from_mem(ptr + 32, size, 0x100)))
            except Exception:
                ctypes.windll.user32.MessageBoxW(0, f"sniffer_error (is_zone:{is_zone}, is_up:True), will be uninstall\n{traceback.format_exc()}", "sniffer_error", 0x10)
                _hook.uninstall()
                pass
            return _hook.original(a1, pkt, a3, a4, a5)

        return func

    def replay_recv(_hook, a1):
        if res := _hook.original(a1):
            try:
                proto_no, size, timestamp, src_id = struct.unpack(b'2H2I', mv_from_mem(res, 0xc, 0x100))
                cb(True, False, proto_no, src_id, bytearray(mv_from_mem(res + 0xc, size, 0x100)))
            except Exception:
                ctypes.windll.user32.MessageBoxW(0, f"sniffer_error (replay recv), will be uninstall\n{traceback.format_exc()}", "sniffer_error", 0x10)
                _hook.uninstall()
                pass
        return res

    chat_recv = create_hook(chat_recv_addr, ctypes.c_char, [ctypes.c_int64, ctypes.POINTER(ctypes.c_void_p)])(on_recv(False)).install_and_enable()
    zone_recv = create_hook(zone_recv_addr, ctypes.c_char, [ctypes.c_int64, ctypes.POINTER(ctypes.c_void_p)])(on_recv(True)).install_and_enable()
    chat_send = create_hook(chat_send_addr, ctypes.c_char, [ctypes.c_int64, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_char])(on_send(False)).install_and_enable()
    zone_send = create_hook(zone_send_addr, ctypes.c_char, [ctypes.c_int64, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_char])(on_send(True)).install_and_enable()
    replay_recv = create_hook(replay_recv_addr, ctypes.c_int64, [ctypes.c_int64])(replay_recv).install_and_enable()
    return chat_recv, zone_recv, chat_send, zone_send, replay_recv


def try_hook():
    if not hasattr(inject_server, 'hook_sniff'):
        setattr(inject_server, 'hook_sniff', hook_sniff(
            lambda is_zone, is_up, pno, src_id, data: inject_server.push_event('hook_sniff', (is_zone, is_up, pno, src_id, data))
        ))
        return len(inject_server.hook_sniff)
    return 0


res = try_hook()


'''


def install():
    import os
    import sys
    import time

    from ff_draw.main import FFDraw
    from ff_draw.sniffer.utils import message
    from nylib.utils.win32.inject_rpc import Handle, pywin32_dll_place

    main = FFDraw.instance

    pywin32_dll_place()
    handle = Handle(main.mem.pid, main.mem.handle)
    if getattr(sys, 'frozen', False):
        handle.add_path(os.path.join(os.environ['ExcPath'], 'res', 'lib.zip'))

    chat_recv_addr, = main.mem.scanner.find_point("e8 * * * * 84 ? 74 ? 66 66 0f 1f 84 00")
    zone_recv_addr, = main.mem.scanner.find_point("48 ? ? ? ? 4c 89 6c 24 ? 4c 89 6c 24 ? e8 * * * * 84")
    chat_send_addr, = main.mem.scanner.find_point("e8 * * * * 48 ? ? ? ? 0f ? ? e8 ? ? ? ? 48 ? ? ? e8 ? ? ? ? 0f")
    zone_send_addr, = main.mem.scanner.find_point("e8 * * * * 84 ? 74 ? 48 ? ? c7 87")
    replay_recv_addr, = main.mem.scanner.find_point("e8 * * * * 48 ? ? 48 ? ? 0f 84 ? ? ? ? 8b ? ? 0f ? ? 0f")
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

    handle.wait_inject()
    handle.client.subscribe('hook_sniff', callback)
    install_cnt = handle.run(f'''
chat_recv_addr = {chat_recv_addr} 
zone_recv_addr = {zone_recv_addr}   
chat_send_addr = {chat_send_addr}   
zone_send_addr = {zone_send_addr} 
replay_recv_addr = {replay_recv_addr} 
me_id_addr = {me_id_addr} 
    ''' + shell_code)
    main.logger.info(f'sniff hook install:{install_cnt}')
