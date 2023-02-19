import typing
from nylib.utils.win32 import memory as ny_mem

if typing.TYPE_CHECKING:
    from . import XivMem


class PacketFix:
    def __init__(self, main: 'XivMem'):
        self.main = main
        self.handle = main.handle
        self.p_fix_param_1 = main.scanner.find_point("89 1d * * * * 40 ? ? 75")[0]
        self.p_fix_param_2 = main.scanner.find_point("41 ? ? 89 15 * * * * 48 ? ? ? 5f")[0]
        self.p_fix_param_3 = main.scanner.find_point("8b ? * * * * 44 ? ? ? ? ? ? 4c 89 b4 24")[0]

    @property
    def value(self):
        return min(ny_mem.read_uint(self.handle, self.p_fix_param_1) + ny_mem.read_uint(self.handle, self.p_fix_param_3) - ny_mem.read_uint(self.handle, self.p_fix_param_2), 0)
