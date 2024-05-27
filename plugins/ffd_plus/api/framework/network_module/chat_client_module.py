import typing
from nylib.utils.imgui import ctx as imgui_ctx
from ffd_plus.api.utils.mem import ClassFunction, scan_val

if typing.TYPE_CHECKING:
    from . import NetworkModule


class ChatClientModule:
    def __init__(self, network_module: 'NetworkModule', address: int):
        self.network_module = network_module
        self.handle = network_module.handle
        self.address = address

    pop_recv_packet = ClassFunction(scan_val("e8 * * * * 84 ? 74 ? 66 66 0f 1f 84 00"), 'c_bool', 'c_void_p',main_loop=True)
    push_send_packet = ClassFunction(scan_val("e8 * * * * 48 ? ? ? ? 0f ? ? e8 ? ? ? ? 48 ? ? ? e8 ? ? ? ? 0f"), 'c_bool', 'c_char_p', 'c_uint', 'c_uint', 'c_bool',main_loop=True)

    def render_panel(self):
        with imgui_ctx.TreeNode(f'chat_client_module#{self.address:X}') as n, n, imgui_ctx.ImguiId('chat_client_module'):
            pass
