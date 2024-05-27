import typing
from nylib.utils.imgui import ctx as imgui_ctx
from ffd_plus.api.utils.mem import ClassFunction, scan_val

if typing.TYPE_CHECKING:
    from . import NetworkModule


class ZoneClientModule:
    def __init__(self, network_module: 'NetworkModule', address: int):
        self.network_module = network_module
        self.handle = network_module.handle
        self.address = address

    pop_recv_packet = ClassFunction(scan_val("48 ? ? ? ? 4c 89 6c 24 ? 4c 89 6c 24 ? e8 * * * * 84"), 'c_bool', 'c_void_p')
    push_send_packet = ClassFunction(scan_val("e8 * * * * 84 ? 74 ? 48 ? ? c7 87"), 'c_bool', 'c_char_p', 'c_uint', 'c_uint', 'c_bool')

    def render_panel(self):
        with imgui_ctx.TreeNode(f'zone_client_module#{self.address:X}') as n, n, imgui_ctx.ImguiId('zone_client_module'):
            pass
