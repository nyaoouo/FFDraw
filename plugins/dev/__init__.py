from __future__ import annotations
import json
from ff_draw.plugins import FFDrawPlugin
import imgui
import requests

from .Code_debug import tab_code_debug
from .action_list.Action_list import tab_action_list
from .i18n import *


class Dev(FFDrawPlugin):
    def __init__(self, main):
        super().__init__(main)
        self.show_action_list = False

        self.actor_list = main.mem.actor_table
        self.action_list_current_omen_id = None

        self.code_debug_code = ''

    def draw_panel(self):
        with imgui.begin_tab_bar("##tabBar") as tab_bar:
            if tab_bar.opened:
                with imgui.begin_tab_item(i18n(Action_list)) as item1:
                    if item1.selected:
                        tab_action_list(self)
                with imgui.begin_tab_item(i18n(Code_debug)) as item2:
                    if item2.selected:
                        tab_code_debug(self)

    def send_post(self, json_data: dict):
        res = requests.post(f'http://127.0.0.1:{self.main.http_port}/rpc', json=json_data)
        return int(json.loads(res.text)['res'])
