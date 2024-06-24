import enum
from .utils import *


@set_fields_from_annotations
class CTCharacter(InstanceObject):
    flags: 'fctypes.c_uint32' = eval('0X30')
    e_npc_id: 'fctypes.c_uint32' = eval('0X34')
    b_npc_id: 'fctypes.c_uint32' = eval('0X38')
    se_pack: 'fctypes.c_uint32' = eval('0X3C')
    _model_visibilities: 'fctypes.c_int32' = eval('0X40')
    model_visibility_count: 'fctypes.c_int32' = eval('0X44')
    _weapons: 'fctypes.c_int32' = eval('0X48')
    weapon_count: 'fctypes.c_int32' = eval('0X4C')
    visible: 'fctypes.c_int8' = eval('0X50')

    @functools.cached_property
    def model_visibilities(self):
        return (ctypes.c_uint8 * self.model_visibility_count).from_address(ctypes.addressof(self) + self._model_visibilities)

    @functools.cached_property
    def weapons(self):
        return (ctypes.c_uint8 * self.weapon_count).from_address(ctypes.addressof(self) + self._weapons)


@set_fields_from_annotations
class CTMonster(CTCharacter):
    primary_model_id: 'fctypes.c_uint16' = eval('0X54')
    secondary_model_id: 'fctypes.c_uint16' = eval('0X56')
    image_change_id: 'fctypes.c_uint16' = eval('0X58')
    material_id: 'fctypes.c_uint32' = eval('0X5C')
    decal_id: 'fctypes.c_uint32' = eval('0X60')
    vfx_id: 'fctypes.c_uint32' = eval('0X64')
    material_animation_id: 'fctypes.c_uint32' = eval('0X68')


@set_fields_from_annotations
class CTEquipmentElement(ctypes.Structure):
    _size_ = 0X20
    image_change_id: 'fctypes.c_uint32' = eval('0X0')
    equipment_id: 'fctypes.c_uint32' = eval('0X4')
    staining_id: 'fctypes.c_uint32' = eval('0X8')
    free_company: 'fctypes.c_uint32' = eval('0XC')
    material_id: 'fctypes.c_uint32' = eval('0X10')
    decal_id: 'fctypes.c_uint32' = eval('0X14')
    vfx_id: 'fctypes.c_uint32' = eval('0X18')
    material_animation_id: 'fctypes.c_uint32' = eval('0X1C')


@set_fields_from_annotations
class CTWeapon(CTCharacter):
    primary_model_id: 'fctypes.c_uint16' = eval('0X54')
    secondary_model_id: 'fctypes.c_uint16' = eval('0X56')
    image_change_id: 'fctypes.c_uint16' = eval('0X58')
    staining_id: 'fctypes.c_uint16' = eval('0X5A')
    material_id: 'fctypes.c_uint32' = eval('0X5C')
    free_company: 'fctypes.c_uint32' = eval('0X60')
    decal_id: 'fctypes.c_uint32' = eval('0X64')
    vfx_id: 'fctypes.c_uint32' = eval('0X68')
    material_animation_id: 'fctypes.c_uint32' = eval('0X6C')
    attach_type: 'fctypes.c_int32' = eval('0X70')


class AccessorySlot(enum.Enum):
    EARRING = 0X0
    NECKLACE = 0X1
    WRIST = 0X2
    FINGER_R = 0X3
    FINGER_L = 0X4


class ArmorSlot(enum.Enum):
    HELMET = 0X0
    TOP = 0X1
    GLOVE = 0X2
    DOWN = 0X3
    SHOES = 0X4


class ModelSlot(enum.Enum):
    HELMET = 0X0
    TOP = 0X1
    GLOVE = 0X2
    DOWN = 0X3
    SHOES = 0X4
    EARRING = 0X5
    NECKLACE = 0X6
    WRIST = 0X7
    FINGER_R = 0X8
    FINGER_L = 0X9
    HAIR = 0XA
    FACE = 0XB
    TAIL = 0XC
    CONNECTION_SUPER = 0XD
    CONNECTION = 0XE


@set_fields_from_annotations
class CTHuman(CTCharacter):
    _armor_elements: 'fctypes.c_int32' = eval('0X54')
    armor_element_count: 'fctypes.c_int32' = eval('0X58')

    @functools.cached_property
    def armor_elements(self):
        return (CTEquipmentElement * self.armor_element_count).from_address(ctypes.addressof(self) + self._armor_elements)


@set_fields_from_annotations
class CTPlayer(CTHuman):
    _customize_data: 'fctypes.c_int32' = eval('0X5C')
    customize_data_count: 'fctypes.c_int32' = eval('0X60')
    _accessory_elements: 'fctypes.c_int32' = eval('0X64')
    accessory_element_count: 'fctypes.c_int32' = eval('0X68')
    hair_material_id: 'fctypes.c_uint32' = eval('0X6C')

    @functools.cached_property
    def customize_data(self):
        return (ctypes.c_uint8 * self.customize_data_count).from_address(ctypes.addressof(self) + self._customize_data)

    @functools.cached_property
    def accessory_elements(self):
        return (CTEquipmentElement * self.accessory_element_count).from_address(ctypes.addressof(self) + self._accessory_elements)


@set_fields_from_annotations
class CTDemiHuman(CTHuman):
    skeleton_id: 'fctypes.c_uint32' = eval('0X5C')
