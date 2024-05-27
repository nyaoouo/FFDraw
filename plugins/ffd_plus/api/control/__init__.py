import ctypes
import typing
from nylib.utils.imgui import ctx as imgui_ctx

from ff_draw.mem.utils import struct_mem_property, direct_mem_property
from ..game_object_manager.character.battle_chara import BattleChara
from ..utils import imgui_display_data

from .target_system import TargetSystem
from ffd_plus.utils import game_version

if typing.TYPE_CHECKING:
    from .. import Api


class ControlOffsets:
    if game_version >= (6, 4, 0):
        camera_manager = 0x0
        target_system = 0x180
        move_config = 0x54F0
        fly_manager = 0x5518
        move_manager = 0x5520
        look_at_spline_calculator = 0x5A90
        event_control = 0x5AD4
        spectator = 0x5AD8
        chara_camera = 0x5AE0
        control_character_id = 0x5AE8
        control_character = 0x5AF0
        initialized = 0x5AF8
    else:
        camera_manager = 0X0
        target_system = 0X180
        move_config = 0X5470
        fly_manager = 0X5488
        move_manager = 0X5490
        look_at_spline_calculator = 0X59F0
        event_control = 0X5A34
        spectator = 0X5A38
        chara_camera = 0X5A40
        control_character_id = 0X5A48
        control_character = 0X5A50
        initialized = 0X5A58

    _is_validate_ = False

    @classmethod
    def validate(cls):
        if cls._is_validate_: return cls
        from ffd_plus.api import Api
        if Api.instance.scanner.find_val(
                "80 b9 <? ? ? ?> ? 48 ? ? 0f 84 ? ? ? ? 83 ? ? 0f 87"
        )[0] != cls.initialized: raise Exception('PControlOffsets is not validate')
        cls._is_validate_ = True
        return cls


class Control:
    instance: 'Control' = None
    offsets: 'ControlOffsets' = None

    def __init__(self, api: 'Api'):
        assert Control.instance is None, "Control already initialized"
        Control.instance = self
        self.api = api
        self.handle = api.handle
        self.address, = api.scanner.find_val("48 ? ? * * * * 45 ? ? 44 0f 29 84 24")
        if Control.offsets is None:
            Control.offsets = ControlOffsets.validate()

    control_character_id = direct_mem_property(ctypes.c_uint32)
    control_character = struct_mem_property(BattleChara, is_pointer=True)
    target_system = struct_mem_property(TargetSystem)

    def render_game(self):
        pass

    def render_panel(self):
        with imgui_ctx.TreeNode(f'control#{self.address:X}') as n, n, imgui_ctx.ImguiId('control'):
            imgui_display_data('control_character_id', hex(self.control_character_id))
            imgui_display_data('control_character', self.control_character)
