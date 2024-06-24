import ctypes
import enum
import functools

from nylib.struct import set_fields_from_annotations, fctypes
from nylib.utils.enum import auto_missing
from ..utils import offset_string


@auto_missing
class HousingSizeType(enum.Enum):
    S = 0X0
    M = 0X1
    L = 0X2


@auto_missing
class HousingTimelinePlayType(enum.Enum):
    Switch = 0X0
    Trigger = 0X1


@auto_missing
class HousingCraftType(enum.Enum):
    Null = 0X0
    AetherialWheel = 0X1
    House = 0X2
    Airship = 0X3
    Submarine = 0X4


@auto_missing
class HounsingCombinedFurnitureType(enum.Enum):
    Null = 0X0
    Gardening = 0X1
    AetherialWheel = 0X2
    EmploymentNPC = 0X3
    ChocoboStable = 0X4
    FishPrint = 0X5
    Picture = 0X6
    Wallpaper = 0X7
    Flowerpot = 0X8
    Aquarium = 0X9
    AquariumParts = 0XA


@set_fields_from_annotations
class HousingCombinedFurnitureSettings(ctypes.Structure):
    combined_furniture_type: 'fctypes.c_int32' = eval('0X0')
    slot_member_ids: 'fctypes.array(fctypes.c_uint32, 8)' = eval('0X4')

    @property
    def e_combined_furniture_type(self):
        return HounsingCombinedFurnitureType(self.combined_furniture_type)


@set_fields_from_annotations
class HousingLayoutAttribute(ctypes.Structure):
    wall: 'fctypes.c_int8' = eval('0X0')
    table: 'fctypes.c_int8' = eval('0X1')
    desktop: 'fctypes.c_int8' = eval('0X2')
    wall_hung: 'fctypes.c_int8' = eval('0X3')
    window: 'fctypes.c_int8' = eval('0X4')


@set_fields_from_annotations
class HousingSettings(ctypes.Structure):
    default_color_id: 'fctypes.c_uint16' = eval('0X0')
    block_id: 'fctypes.c_uint8' = eval('0X2')
    block_size: 'fctypes.c_int32' = eval('0X4')
    groups: 'fctypes.c_int32' = eval('0X20')
    group_count: 'fctypes.c_int32' = eval('0X24')
    _ob_set_asset_path: 'fctypes.c_int32' = eval('0X28')
    _combined_furniture_settings: 'fctypes.c_int32' = eval('0X2C')
    _layout_attribute: 'fctypes.c_int32' = eval('0X30')
    initial_emissive_state: 'fctypes.c_int8' = eval('0X34')
    timeline_play_type: 'fctypes.c_int32' = eval('0X38')
    housing_craft_type: 'fctypes.c_int32' = eval('0X3C')
    base_scale: 'fctypes.c_float' = eval('0X40')

    ob_set_asset_path = offset_string('_ob_set_asset_path')

    @property
    def e_block_size(self):
        return HousingSizeType(self.block_size)

    @property
    def e_timeline_play_type(self):
        return HousingTimelinePlayType(self.timeline_play_type)

    @property
    def e_housing_craft_type(self):
        return HousingCraftType(self.housing_craft_type)

    @functools.cached_property
    def combined_furniture_settings(self):
        return HousingCombinedFurnitureSettings.from_address(ctypes.addressof(self) + self._combined_furniture_settings)

    @functools.cached_property
    def layout_attribute(self):
        return HousingLayoutAttribute.from_address(ctypes.addressof(self) + self._layout_attribute)
