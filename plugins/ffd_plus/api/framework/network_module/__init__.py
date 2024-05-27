import ctypes

import typing
import imgui

from ffd_plus.utils import game_version
from nylib.utils.win32 import memory as ny_mem
from nylib.utils.imgui import ctx as imgui_ctx
from ff_draw.mem.utils import direct_mem_property, struct_mem_property
from ffd_plus.api.utils import imgui_display_data
from ffd_plus.api.utils.commons import Utf8String

from .chat_client_module import ChatClientModule
from .lobby_client_module import LobbyClientModule, LobbyClientProxy
from .zone_client_module import ZoneClientModule

if typing.TYPE_CHECKING:
    from .. import Framework

if game_version >= (6, 5, 0):
    class NetworkModuleOffsets:
        default_lobby_count = 0x28  # uint8
        default_lobby_ports = 0x2C  # int32[12]
        default_lobby_hosts = 0x60  # Utf8String[12]
        platform_id = 0x5A8  # int32
        os_id = 0x5AC  # int16
        save_data_port = 0x5B0  # int32
        save_data_host = 0x5B8  # Utf8String
        save_data_mode = 0x620  # int32
        lobby_port = 0x690  # int32
        lobby_host = 0x698  # Utf8String
        lobby_retry_count = 0x770  # int32
        lobby_retry_interval = 0x774  # int32
        lobby_ping = 0x778  # int32
        use_default_remote = 0x850  # int32
        default_ticket = 0x858  # Utf8String
        default_world = 0x8C0  # Utf8String
        default_zone = 0x928  # Utf8String
        use_chat = 0x990  # int8
        language = 0x994  # int32
        zone_client_module = 0x998  # ZoneClientModule*
        chat_client_module = 0x9A0  # ChatClientModule*
        lobby_client_module = 0x9A8  # LobbyClientModule*
        lobby_client_proxy = 0x9B0  # LobbyClientProxy*
else:
    class NetworkModuleOffsets:
        default_lobby_count = 0x28  # uint8
        default_lobby_ports = 0x2C  # int32[12]
        default_lobby_hosts = 0x60  # Utf8String[12]
        platform_id = 0x540  # int32
        os_id = 0x544  # int16
        save_data_port = 0x548  # int32
        save_data_host = 0x550  # Utf8String
        save_data_mode = 0x5B8  # int32
        lobby_port = 0x628  # int32
        lobby_host = 0x630  # Utf8String
        lobby_retry_count = 0x708  # int32
        lobby_retry_interval = 0x70C  # int32
        lobby_ping = 0x710  # int32
        use_default_remote = 0x7E8  # int32
        default_ticket = 0x7F0  # Utf8String
        default_world = 0x858  # Utf8String
        default_zone = 0x8C0  # Utf8String
        use_chat = 0x928  # int8
        language = 0x92C  # int32
        zone_client_module = 0x930  # ZoneClientModule*
        chat_client_module = 0x938  # ChatClientModule*
        lobby_client_module = 0x940  # LobbyClientModule*
        lobby_client_proxy = 0x948  # LobbyClientProxy*


class NetworkModule:
    offsets = NetworkModuleOffsets

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    default_lobby_count = direct_mem_property(ctypes.c_uint8)

    def get_default_lobby_remote(self, idx):
        port = ny_mem.read_int32(self.handle, self.address + self.offsets.default_lobby_ports + idx * 4)
        host = Utf8String(self.handle, self.address + self.offsets.default_lobby_hosts + idx * 0x68)
        return port, host

    def iter_default_lobby_remote(self):
        for i in range(self.default_lobby_count):
            yield self.get_default_lobby_remote(i)

    platform_id = direct_mem_property(ctypes.c_int32)
    os_id = direct_mem_property(ctypes.c_int16)
    save_data_port = direct_mem_property(ctypes.c_int32)
    save_data_host = struct_mem_property(Utf8String)
    save_data_mode = direct_mem_property(ctypes.c_int32)
    lobby_port = direct_mem_property(ctypes.c_int32)
    lobby_host = struct_mem_property(Utf8String)
    lobby_retry_count = direct_mem_property(ctypes.c_int32)
    lobby_retry_interval = direct_mem_property(ctypes.c_int32)
    lobby_ping = direct_mem_property(ctypes.c_int32)
    use_default_remote = direct_mem_property(ctypes.c_int32)
    default_ticket = struct_mem_property(Utf8String)
    default_world = struct_mem_property(Utf8String)
    default_zone = struct_mem_property(Utf8String)
    use_chat = direct_mem_property(ctypes.c_int8)
    language = direct_mem_property(ctypes.c_int32)
    zone_client_module = struct_mem_property(ZoneClientModule, is_pointer=True, pass_self=True)
    chat_client_module = struct_mem_property(ChatClientModule, is_pointer=True, pass_self=True)
    lobby_client_module = struct_mem_property(LobbyClientModule, is_pointer=True, pass_self=True)
    lobby_client_proxy = struct_mem_property(LobbyClientProxy, is_pointer=True, pass_self=True)

    def render_panel(self):
        with imgui_ctx.TreeNode(f'network module#{self.address:X}') as n, n, imgui_ctx.ImguiId('network_module_panel'):
            with imgui_ctx.TreeNode('default lobby remote') as n, n:
                for i, (port, host) in enumerate(self.iter_default_lobby_remote()):
                    host = host.value.rstrip(b'\0').decode("utf-8")
                    imgui_display_data(f'[{i}]', f'{host}:{port}')
            imgui_display_data('platform_id', self.platform_id)
            imgui_display_data('os_id', self.os_id)
            save_data_host = self.save_data_host.value.rstrip(b'\0').decode("utf-8")
            imgui_display_data(f'save data remote', f'{save_data_host}:{self.save_data_port}')
            imgui_display_data('save data mode', self.save_data_mode)
            lobby_host = self.lobby_host.value.rstrip(b'\0').decode("utf-8")
            imgui_display_data(f'lobby remote', f'{lobby_host}:{self.lobby_port}')
            imgui.input_int2('lobby retry count/interval', self.lobby_retry_count, self.lobby_retry_interval, imgui.INPUT_TEXT_READ_ONLY)
            imgui_display_data('lobby ping', self.lobby_ping)
            imgui_display_data('use chat', self.use_chat)
            imgui_display_data('language', self.language)
            cm.render_panel() if (cm := self.lobby_client_module) else imgui.text('lobby_client_module: None')
            cm.render_panel() if (cm := self.zone_client_module) else imgui.text('zone_client_module: None')
            cm.render_panel() if (cm := self.chat_client_module) else imgui.text('chat_client_module: None')
            cm.render_panel() if (cm := self.lobby_client_proxy) else imgui.text('lobby_client_proxy: None')

    def render_game(self):
        pass


class NetworkModuleProxy:
    class offsets:
        network_module = 0x8

    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    network_module = struct_mem_property(NetworkModule, is_pointer=True)
