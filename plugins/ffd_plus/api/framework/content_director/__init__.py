import time
import typing
import imgui

from nylib.utils.win32 import memory as ny_mem
from nylib.utils.imgui import ctx as imgui_ctx
from ff_draw.mem.utils import struct_mem_property
from ffd_plus.api.utils import CachedStaticPatternSearcher, U32_MAX
from ffd_plus.api.utils.mem import ClassFunction, StaticFunction, scan_val
from .content_ex_action import ContentExAction

if typing.TYPE_CHECKING:
    from .. import Framework


class ContentDirectorOffset:
    def __init__(self):
        from ffd_plus.api import Api
        scanner = Api.instance.scanner
        self._content_ex_action = scanner.find_val('48 ? <? ? ? ?> 33 ? 38 48')[0] & U32_MAX


class ContentDirector:
    offsets: 'ContentDirectorOffset' = None

    def __init__(self, handle, address):
        if ContentDirector.offsets is None:
            ContentDirector.offsets = ContentDirectorOffset()
        self.handle = handle
        self.address = address

    _content_ex_action = struct_mem_property(ContentExAction)

    @property
    def content_ex_action(self):
        if (cea := self._content_ex_action).content_ex_action_id: return cea

    def render_panel(self):
        pass

    def render_game(self):
        pass
