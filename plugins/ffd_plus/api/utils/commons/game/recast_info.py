import ctypes

from ff_draw.mem.utils import direct_mem_property


class RecastInfo:
    class offsets:
        occupied = 0x0
        action_id = 0x4
        timer = 0x8
        time_max = 0xC
        last_state = 0x10

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    occupied = direct_mem_property(ctypes.c_int8)
    action_id = direct_mem_property(ctypes.c_int32)
    timer = direct_mem_property(ctypes.c_float)  # count up
    time_max = direct_mem_property(ctypes.c_float)
    last_state = direct_mem_property(ctypes.c_int8)

    @property
    def remaining(self):
        return max(0, self.time_max - self.timer)
