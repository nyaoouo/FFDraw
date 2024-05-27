import ctypes

import typing
import imgui

from nylib.utils.win32 import memory as ny_mem
from nylib.utils.imgui import ctx as imgui_ctx
from ff_draw.mem.utils import direct_mem_property, struct_mem_property
from ffd_plus.api.utils import imgui_display_data
from ffd_plus.api.utils.commons import Utf8String, ItemVector, vector, Pointer
from .account_info import AccountInfo
from .character_info import CharacterInfo, CharacterInfo11
from .world_info import WorldInfo

if typing.TYPE_CHECKING:
    from .. import NetworkModule


class LobbyClientModule:
    class offsets:
        p_login_type = 0x10  # int32*
        p_chara_make_type = 0x18  # int32*
        last_request_id = 0x28  # uint32
        region_id = 0x2c  # uint8
        game_login_type = 0x2d  # uint8
        platform_id = 0x21c  # int32
        os_id = 0x220  # int16
        is_steam = 0x222  # uint8
        p_account_list = 0x248  # vector<AccountInfo>
        p_character_list = 0x260  # vector<CharacterInfo>
        p_world_list = 0x278  # vector<WorldInfo>
        p_character11_list = 0x290  # vector<CharacterInfo2>
        retainer_count = 0x2a8  # int32
        retainer_list = 0x2b0  # RetainerInfo[24]
        billing_info = 0X2C8  # BillingInfo
        make_character_list = 0X328  # vector<CharacterInfo>
        login_info = 0X340  # LoginInfo

    def __init__(self, network_module: 'NetworkModule', address: int):
        self.network_module = network_module
        self.handle = network_module.handle
        self.address = address

    @property
    def login_type(self):
        if addr := ny_mem.read_address(self.handle, self.address + self.offsets.p_login_type):
            return ny_mem.read_int32(self.handle, addr + 0x8)

    @property
    def chara_make_type(self):
        if addr := ny_mem.read_address(self.handle, self.address + self.offsets.p_chara_make_type):
            return ny_mem.read_int32(self.handle, addr + 0x8)

    last_request_id = direct_mem_property(ctypes.c_uint32)
    region_id = direct_mem_property(ctypes.c_uint8)
    game_login_type = direct_mem_property(ctypes.c_uint8)
    platform_id = direct_mem_property(ctypes.c_uint32)
    os_id = direct_mem_property(ctypes.c_uint16)
    is_steam = direct_mem_property(ctypes.c_uint8)
    p_account_list = struct_mem_property(ItemVector[Pointer[AccountInfo], 8])
    p_character_list = struct_mem_property(ItemVector[Pointer[CharacterInfo], 8])
    p_world_list = struct_mem_property(ItemVector[WorldInfo, 0X54])
    p_character11_list = struct_mem_property(ItemVector[CharacterInfo11, 0X28])

    def render_panel(self):
        with imgui_ctx.TreeNode(f'lobby_client_module#{self.address:X}') as n, n, imgui_ctx.ImguiId('lobby_client_module'):
            imgui_display_data('login_type', self.login_type)
            imgui_display_data('chara_make_type', self.chara_make_type)
            imgui_display_data('last_request_id', self.last_request_id)
            imgui_display_data('region_id', self.region_id)
            imgui_display_data('game_login_type', self.game_login_type)
            imgui_display_data('platform_id', self.platform_id)
            imgui_display_data('os_id', self.os_id)
            imgui_display_data('is_steam', self.is_steam)

            p_account_list = self.p_account_list
            with imgui_ctx.TreeNode(f'account_list[{len(p_account_list)}]') as n, n, imgui_ctx.ImguiId('account_list'):
                for i in range(len(p_account_list)):
                    p_account_list[i].content.render_panel(f'[{i}]')

            p_character_list = self.p_character_list
            with imgui_ctx.TreeNode(f'character_list[{len(p_character_list)}]') as n, n, imgui_ctx.ImguiId('character_list'):
                for i in range(len(p_character_list)):
                    p_character_list[i].content.render_panel(f'[{i}]')

            p_world_list = self.p_world_list
            with imgui_ctx.TreeNode(f'world_list[{len(p_world_list)}]') as n, n, imgui_ctx.ImguiId('world_list'):
                for i in range(len(p_world_list)):
                    p_world_list[i].render_panel(f'[{i}]')

            p_character11_list = self.p_character11_list
            with imgui_ctx.TreeNode(f'character11_list[{len(p_character11_list)}]') as n, n, imgui_ctx.ImguiId('character11_list'):
                for i in range(len(p_character11_list)):
                    p_character11_list[i].render_panel(f'[{i}]')


class LobbyClientProxy:
    class offsets:
        lobby_port = 0x8  # int32
        lobby_host = 0X10  # Utf8String
        proxy_id = 0X78  # uint32
        ping_ms = 0X7C  # uint32
        module = 0X80  # LobbyClientModule*
        save_data_port = 0x90  # int32
        save_data_host = 0X98  # Utf8String
        save_data_mode = 0X100  # int32
        status = 0x170  # int32
        region = 0x190  # int32
        language = 0x194  # int32

    def __init__(self, network_module: 'NetworkModule', address: int):
        self.network_module = network_module
        self.handle = network_module.handle
        self.address = address

    lobby_port = direct_mem_property(ctypes.c_int32)
    lobby_host = struct_mem_property(Utf8String)
    proxy_id = direct_mem_property(ctypes.c_uint32)
    ping_ms = direct_mem_property(ctypes.c_uint32)
    module = struct_mem_property(LobbyClientModule, is_pointer=True, pass_self='network_module')
    save_data_port = direct_mem_property(ctypes.c_int32)
    save_data_host = struct_mem_property(Utf8String)
    save_data_mode = direct_mem_property(ctypes.c_int32)
    status = direct_mem_property(ctypes.c_int32)
    region = direct_mem_property(ctypes.c_int32)
    language = direct_mem_property(ctypes.c_int32)

    def render_panel(self):
        with imgui_ctx.TreeNode(f'lobby_client_proxy#{self.address:X}') as n, n, imgui_ctx.ImguiId('lobby_client_proxy'):
            lobby_host = self.lobby_host.value.rstrip(b'\0').decode("utf-8")
            imgui_display_data('lobby_remote', f'{lobby_host}:{self.lobby_port}')
            imgui_display_data('proxy_id', self.proxy_id)
            imgui_display_data('ping_ms', self.ping_ms)
            save_data_host = self.save_data_host.value.rstrip(b'\0').decode("utf-8")
            imgui_display_data('save_data_remote', f'{save_data_host}:{self.save_data_port}')
            imgui_display_data('save_data_mode', self.save_data_mode)
            imgui_display_data('status', self.status)
            imgui_display_data('region', self.region)
            imgui_display_data('language', self.language)
            m.render_panel() if (m := self.module) else imgui.text('module: None')
