import enum

from .utils import *


class TargetType(enum.Enum):
    Null = 0X0
    ENPCInstanceID = 0X1
    Player = 0X2
    PartyMember = 0X3
    ENPCDirect = 0X4
    BNPCDirect = 0X5
    BGObjInstanceID = 0X6
    SharedGroupInstanceID = 0X7
    BGObj = 0X8
    SharedGroup = 0X9
    Weapon = 0XA
    StableChocobo = 0XB
    AllianceMember = 0XC
    GuestMember = 0XD
    GroomPlayer = 0XE
    BridePlayer = 0XF
    CustomSharedGroup = 0X10


@set_fields_from_annotations
class WeaponModel(ctypes.Structure):
    skeleton_id: 'fctypes.c_uint16' = eval('0X0')
    pattern_id: 'fctypes.c_uint16' = eval('0X2')
    image_change_id: 'fctypes.c_uint16' = eval('0X4')
    staining_id: 'fctypes.c_uint16' = eval('0X6')


@set_fields_from_annotations
class HelperObjInstanceObject(InstanceObject):
    obj_type: 'fctypes.c_uint32' = eval('0X30')
    target_type: 'fctypes.c_uint32' = eval('0X34')  # TargetType
    specific: 'fctypes.c_int8' = eval('0X38')
    character_size: 'fctypes.c_uint8' = eval('0X39')
    use_default_motion: 'fctypes.c_int8' = eval('0X3A')
    party_member_index: 'fctypes.c_uint8' = eval('0X3B')
    target_instance_id: 'fctypes.c_uint32' = eval('0X3C')
    direct_id: 'fctypes.c_uint32' = eval('0X40')
    use_direct_id: 'fctypes.c_int8' = eval('0X44')
    keep_high_texture: 'fctypes.c_int8' = eval('0X45')
    weapon: 'WeaponModel' = eval('0X46')
    alliance_member_index: 'fctypes.c_uint8' = eval('0X4E')
    guest_member_index: 'fctypes.c_uint8' = eval('0X4F')
    sky_visibility: 'fctypes.c_float' = eval('0X50')
    other_instance_object: 'fctypes.c_int32' = eval('0X54')
    use_transform: 'fctypes.c_int8' = eval('0X58')
    model_lod: 'fctypes.c_uint8' = eval('0X59')
    texture_lod: 'fctypes.c_uint8' = eval('0X5A')
    draw_head_parts: 'fctypes.c_uint8' = eval('0X5B')
    _default_transform: 'fctypes.array(fctypes.array(fctypes.c_float,3),3)' = eval('0X5C')
    dummy: 'fctypes.c_int8' = eval('0X80')
    disable_hide_weapon_config: 'fctypes.c_int8' = eval('0X81')
    replace_player_customize: 'fctypes.c_int8' = eval('0X82')
    extend_parameter: 'fctypes.c_int32' = eval('0X88')

    @functools.cached_property
    def default_transform(self):
        return Transformation.from_ctypes(self._default_transform)

    @property
    def e_target_type(self):
        return TargetType(self.target_type)
