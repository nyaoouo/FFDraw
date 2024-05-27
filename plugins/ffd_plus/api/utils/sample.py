import typing
from nylib.utils import LazyClassAttr
from nylib.utils.imgui import ctx as imgui_ctx

from ff_draw.mem.utils import struct_mem_property, direct_mem_property

if typing.TYPE_CHECKING:
    from .. import Api


class ManagerOffsets:
    pass

    # _is_validate_ = False
    #
    # @classmethod
    # def validate(cls):
    #     if cls._is_validate_: return cls
    #     from ffd_plus.api import Api
    #     # if Api.instance.scanner.find_val(
    #     #         "80 b9 <? ? ? ?> ? 48 ? ? 0f 84 ? ? ? ? 83 ? ? 0f 87"
    #     # )[0] != cls.initialized: raise Exception('PControlOffsets is not validate')
    #     cls._is_validate_ = True
    #     return cls


class Manager:
    instance: 'Manager' = None
    offsets: 'ManagerOffsets' = None

    def __init__(self, api: 'Api'):
        assert Manager.instance is None, "Manager already initialized"
        Manager.instance = self
        if Manager.offsets is None:
            Manager.offsets = ManagerOffsets.validate()

    def render_panel(self):
        with imgui_ctx.TreeNode(f'Manager#{self.address:X}', push_id=True) as n, n:
            pass

    def render_game(self):
        pass


class Cls:
    def __init__(self, handle, address):
        self.handle = handle
        self.address = address

    def render_panel(self):
        with imgui_ctx.TreeNode(f'Cls#{self.address:X}', push_id=True) as n, n:
            pass

    def render_game(self):
        pass
