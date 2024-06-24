import enum

from .utils import *


@set_fields_from_annotations
class PopRangeInstanceObject(InstanceObject):
    class PopType(enum.Enum):
        PC = 0X1
        NPC = 0X2
        BNPC = 0X2
        Content = 0X3

    pop_type: 'fctypes.c_uint32' = eval('0X30')
    relative_positions: 'RelativePositions' = eval('0X34')
    inner_radius_ratio: 'fctypes.c_float' = eval('0X3C')
    index: 'fctypes.c_uint8' = eval('0X40')
    shuffle_count: 'fctypes.c_uint8' = eval('0X41')

    @property
    def e_pop_type(self):
        return self.PopType(self.pop_type)
