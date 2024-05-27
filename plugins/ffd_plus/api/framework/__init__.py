import ctypes
import logging

import time
import typing
import imgui

from nylib.utils.win32 import memory as ny_mem
from nylib.utils.imgui import ctx as imgui_ctx
from ff_draw.main import FFDraw
from ff_draw.mem.utils import struct_mem_property, direct_mem_property
from ffd_plus.api.utils import CachedStaticPatternSearcher
from ffd_plus.api.utils.mem import ClassFunction, StaticFunction, scan_val

from .content_director import ContentDirector
from .network_module import NetworkModuleProxy
from .bg_collision_module import BgCollisionModule
from .ui_module import UiModule

if typing.TYPE_CHECKING:
    from .. import Api


class FrameworkOffsets:
    def __init__(self, scanner: CachedStaticPatternSearcher):
        self.content_director, = scanner.find_val(
            'e8 (* * * *:48 8B 81 <? ? ? ?>) 48 ? ? 0f 84 ? ? ? ? 8b ? ? ? 0f ? ? 44'
        )
        self.is_network_module_initialized, self.network_module_proxy = scanner.find_val(
            ' e8 (* * * *:80 b9 <? ? ? ?> ? 74 08 48 8b 81 <? ? ? ?>) 41 81 7f ? ? ? ? ? 75'
        )
        self.bg_collision_module, = scanner.find_val(
            '48 ? ? <? ? ? ?> f3 ? ? ? f3 ? ? ? f3 ? ? ? e8 ? ? ? ? f3 ? ? ? 48'
        )
        self.ui_module, = scanner.find_val(
            'e8 (* * * *:48 ? ? 75 (*:48 ? ? <? ? ? ?>)) 8b ? ? ? ? ? 83 ? ? a9'
        )


class Framework:
    instance: 'Framework' = None
    logger = logging.getLogger('FFDBot.api.framework.Framework')
    offsets: 'FrameworkOffsets' = None

    def __init__(self, api: 'Api'):
        assert Framework.instance is None, "Framework already initialized"
        Framework.instance = self
        self.api = api
        self.handle = api.handle
        self._pp_framework, = api.scanner.find_val('48 ? ? <* * * *> 41 39 b1')
        if Framework.offsets is None:
            Framework.offsets = FrameworkOffsets(api.scanner)

    @property
    def address(self):
        return ny_mem.read_address(self.handle, self._pp_framework)

    content_director = struct_mem_property(ContentDirector, is_pointer=True)
    network_module_proxy = struct_mem_property(NetworkModuleProxy, is_pointer=True)
    bg_collision_module = struct_mem_property(BgCollisionModule, is_pointer=True)
    ui_module = struct_mem_property(UiModule, is_pointer=True)
    is_network_module_initialized = direct_mem_property(ctypes.c_uint8)

    get_user_path = ClassFunction(scan_val("e8 * * * * 48 ? ? ? ? ? ? ? 48 ? ? 48 ? ? 74 ? e8 ? ? ? ? 48 89 bc 24"), 'c_wchar_p')

    @property
    def network_module(self):
        if self.is_network_module_initialized and (pxy := self.network_module_proxy):
            return pxy.network_module

    def render_panel(self):
        with imgui_ctx.TreeNode(f'Framework#{self.address:X}', push_id=True) as n, n:
            (cd := self.content_director) and cd.render_panel()
            (nm := self.network_module) and nm.render_panel()
            (bg := self.bg_collision_module) and bg.render_panel()
            (ui := self.ui_module) and ui.render_panel()

    def render_game(self):
        (cd := self.content_director) and cd.render_game()
        (nm := self.network_module) and nm.render_game()
        (bg := self.bg_collision_module) and bg.render_game()
        (ui := self.ui_module) and ui.render_game()
