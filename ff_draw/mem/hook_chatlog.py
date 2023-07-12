import time
import typing

from fpt4.utils import se_string
from nylib.utils import serialize_data, KeyRoute, BroadcastHook

if typing.TYPE_CHECKING:
    from . import XivMem

shell = '''
def on_print_log_hook(cb):
    from nylib.hook import create_hook
    import ctypes
    import logging
    mv_from_mem = ctypes.pythonapi.PyMemoryView_FromMemory
    mv_from_mem.argtypes = (ctypes.c_void_p, ctypes.c_ssize_t, ctypes.c_int)
    mv_from_mem.restype = ctypes.py_object

    def utf8_string_content(ptr):
        if (p_size := ctypes.c_size_t.from_address(ptr + 16).value) and (p_buffer := ctypes.c_size_t.from_address(ptr).value):
            return mv_from_mem(p_buffer, p_size, 0x100).tobytes()

    def on_print_log(_hook, manager, channel_id, p_sender, p_msg, timestamp, is_echo):
        try:
            cb(channel_id, utf8_string_content(p_sender), utf8_string_content(p_msg), timestamp, is_echo)
        except Exception as e:
            logging.error(f"on_print_log_hook error:{e}", exc_info=e)
            _hook.uninstall()
        return _hook.original(manager, channel_id, p_sender, p_msg, timestamp, is_echo)

    return create_hook(print_log_addr, ctypes.c_int64, [
        ctypes.c_size_t,
        ctypes.c_ushort,
        ctypes.c_size_t,
        ctypes.c_size_t,
        ctypes.c_uint,
        ctypes.c_uint8,
    ])(on_print_log).install_and_enable()


def install():
    if not hasattr(inject_server, 'on_print_log_hook') or not getattr(inject_server, 'on_print_log_hook')._installed:
        setattr(inject_server, 'on_print_log_hook', on_print_log_hook(lambda *a: inject_server.push_event('print_log', a)))
        return 1
    return 0

res = install()
'''


class ChatLog(typing.NamedTuple):
    channel_id: int
    sender: str | se_string.SeString | se_string.Macro
    msg: str | se_string.SeString | se_string.Macro
    timestamp: int
    is_echo: bool


class OnPrintChatLog(KeyRoute):
    def __init__(self, mem: 'XivMem'):
        super().__init__(lambda c: c.channel_id)
        self.mem = mem
        print_log_addr, = mem.scanner.find_point("e8 * * * * 48 ? ? ? e8 ? ? ? ? b8 ? ? ? ? 66")
        mem.inject_handle.client.subscribe('print_log', lambda _, data: self(ChatLog(
            data[0],
            se_string.SeString.from_buffer(bytearray(data[1].rstrip(b'\0'))),
            se_string.SeString.from_buffer(bytearray(data[2].rstrip(b'\0'))),
            data[3] or time.time(),
            data[4],
        )))
        mem.inject_handle.run(f'print_log_addr = {print_log_addr}\n' + shell)
