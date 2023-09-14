import threading
import typing
from tkinter import filedialog

import imgui
from nylib.utils.imgui import ctx as imgui_ctx
from .db_handler import RsDataHandler

if typing.TYPE_CHECKING:
    from ..main import FFDraw

shell = '''
import ctypes
def load_rs_data(kwarg: dict):
    if getattr(inject_server,'#__rs_data_loaded__', False) and not kwarg.get('force',False): return
    load_rsv_string = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_size_t, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t)(kwarg['p_load_rsv_string'])
    load_rsf_header = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_size_t, ctypes.c_uint64, ctypes.c_char_p)(kwarg['p_load_rsf_header'])
    p_secret_module = kwarg['p_secret_module']
    for key, value in kwarg['rsv_string']: load_rsv_string(p_secret_module, key.encode('utf-8'), value, len(value))
    for key, value in kwarg['rsf_header']: load_rsf_header(p_secret_module, key, value)
    setattr(inject_server,'#__rs_data_loaded__',True)
load_rs_data(args[0])
'''


class RsData:
    def __init__(self, main: 'FFDraw'):
        from ff_draw.sniffer.message_structs import ZoneServer
        self.main = main
        self.db_handler = RsDataHandler(main.app_data_path / 'rs_data' / f'{main.mem.game_build_date}.db')
        main.sniffer.on_zone_server_message[ZoneServer.RsvString].append(self.on_rsv_string)
        main.sniffer.on_zone_server_message[ZoneServer.RsfHeader].append(self.on_rsf_header)
        self.load_to_game()

    def on_rsv_string(self, msg):
        self.db_handler.insert_rsv_string(msg.message.key, msg.message.raw_value)

    def on_rsf_header(self, msg):
        self.db_handler.insert_rsf_header(msg.message.key, msg.message.value)

    def load_db(self):
        if path := filedialog.askopenfilename():
            self.db_handler.load_new_db(path).wait()

    def load_to_game(self, force=False):
        mem = self.main.mem
        rsv_strings = self.db_handler.list_rsv_string()
        rsf_headers = self.db_handler.list_rsf_header()
        mem.inject_handle.run(shell, {
            'p_secret_module': mem.scanner_v2.find_val("48 ? ? * * * * 48 83 78 ? ? 74 ? 40")[0],
            'p_load_rsv_string': mem.scanner_v2.find_address("40 ? 55 56 57 41 ? 41 ? 41 ? 41 ? 48 ? ? ? ? ? ? 48 ? ? ? ? ? ? 48 ? ? 48 89 84 24 ? ? ? ? 4d ? ? 48 ? ? 4c"),
            'p_load_rsf_header': mem.scanner_v2.find_address("48 89 5c 24 ? 48 89 74 24 ? 57 48 ? ? ? 48 83 b9 ? ? ? ? ? 49 ? ? 48 ? ? 48 ? ? 75"),
            'rsv_string': rsv_strings.wait(),
            'rsf_header': rsf_headers.wait(),
            'force': force,
        }, filename='<load_rs>')

    def render_panel(self):
        with imgui_ctx.ImguiId('rs_data'):
            if imgui.button('load db'):
                threading.Thread(target=self.load_db, daemon=True).start()
            imgui.same_line()
            if imgui.button('force load'):
                threading.Thread(target=self.load_to_game, daemon=True).start()
