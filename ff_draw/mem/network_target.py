import re
import struct
import typing
from nylib.utils.win32 import memory as ny_mem
from nylib.pattern import sig_to_pattern
from .utils import read_utf8_string

if typing.TYPE_CHECKING:
    from . import XivMem

get_network_skeleton, _ = sig_to_pattern("80 b9 ? ? ? ? ? 74 08 48 8b 81 * * * * ?")


class NetworkInfo:
    def __init__(self, main: 'XivMem'):
        self.main = main
        self.handle = main.handle
        p_get_network_module = main.scanner.find_point('e8 * * * * 41 81 7f ? ? ? ? ? 75')[0]
        if get_network_module_asm_match := re.match(get_network_skeleton, ny_mem.read_bytes(self.handle, p_get_network_module, 17)):
            self.network_module_offset, = struct.unpack('I', get_network_module_asm_match.group(1))
        else:
            raise KeyError('Not found network_module_offset')
        self.p_p_framework = main.scanner.find_point('48 ? ? * * * * 41 39 b1')[0]
        self.network_zone_offset = main.scanner.find_val("48 ? ? * * * * 48 ? ? 0f 84 ? ? ? ? 0f ? ? ? ? ? ? 45")[0]

    def get_target(self):
        addr = ny_mem.read_address(self.handle, self.p_p_framework)
        for off in [self.network_module_offset, 8, self.network_zone_offset]:
            if not (addr := ny_mem.read_address(self.handle, addr + off)):
                break
        else:
            return read_utf8_string(self.handle, addr), ny_mem.read_ushort(self.handle, addr + 0x68)
