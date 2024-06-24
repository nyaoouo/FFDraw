import ctypes
import enum
import functools

from nylib.struct import set_fields_from_annotations, fctypes
from .sg_action import get_sg_action_from_addr


class ShowHideAnimationType(enum.Enum):
    Invalid = 0X0
    Null = 0X1
    Auto = 0X2
    Timeline = 0X3
    AutoWithAnimationTime = 0X4


@set_fields_from_annotations
class SGActionFolder(ctypes.Structure):
    _size_ = 0X8

    _sg_actions: 'fctypes.c_int32' = eval('0X0')
    sg_action_count: 'fctypes.c_int32' = eval('0X4')

    @property
    def sg_actions(self):
        p_offset = ctypes.addressof(self) + self._sg_actions
        return [get_sg_action_from_addr(p_offset + o) for o in (ctypes.c_int32 * self.sg_action_count).from_address(p_offset)]


@set_fields_from_annotations
class SGSettings(ctypes.Structure):
    _size_ = 0X24

    name_plate_instance_id: 'fctypes.c_uint8' = eval('0X0')
    timeline_showing_id: 'fctypes.c_uint8' = eval('0X1')
    timeline_hiding_id: 'fctypes.c_uint8' = eval('0X2')
    timeline_shown_id: 'fctypes.c_uint8' = eval('0X3')
    timeline_hidden_id: 'fctypes.c_uint8' = eval('0X4')
    general_purpose_timeline_ids: 'fctypes.array(fctypes.c_uint8, 16)' = eval('0X5')
    timeline_showing_id_enabled: 'fctypes.c_int8' = eval('0X15')
    timeline_hiding_id_enabled: 'fctypes.c_int8' = eval('0X16')
    need_system_actor: 'fctypes.c_int8' = eval('0X17')
    show_hide_animation_type: 'fctypes.c_int32' = eval('0X18')
    show_animation_time: 'fctypes.c_uint16' = eval('0X1C')
    hide_animation_time: 'fctypes.c_uint16' = eval('0X1E')
    _sg_action_folder: 'fctypes.c_int32' = eval('0X20')

    @property
    def e_show_hide_animation_type(self):
        return ShowHideAnimationType(self.show_hide_animation_type)

    @functools.cached_property
    def sg_actions(self):
        return SGActionFolder.from_address(ctypes.addressof(self) + self._sg_action_folder).sg_actions
