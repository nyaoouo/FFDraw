import ctypes

from ff_draw.mem.utils import direct_mem_property
from nylib.utils import LazyClassAttr
from . import Character


class OrnamentCharaOffsets:
    pass


class OrnamentChara(Character):
    offsets = LazyClassAttr(lambda _: OrnamentCharaOffsets)
