import ctypes

import typing
from ff_draw.main import FFDraw
from ff_draw.mem.utils import direct_mem_property, struct_mem_property
from ffd_plus.api.utils.commons import ItemArr
from ffd_plus.api.utils.commons.game import RecastInfo
from ffd_plus.api.control import Control

if typing.TYPE_CHECKING:
    from .. import ContentDirector


class ContentExAction:
    class offsets:
        requested_content_ex_action_id = 0x0
        content_ex_action_id = 0x1
        action_count = 0x18
        recast = 0x2c
        cost_count = 0x54

    def __init__(self, content_director: 'ContentDirector', address):
        self.content_director = content_director
        self.handle = content_director.handle
        self.address = address

    requested_content_ex_action_id = direct_mem_property(ctypes.c_uint8)
    content_ex_action_id = direct_mem_property(ctypes.c_uint8)
    action_count = direct_mem_property(ctypes.c_uint8)
    recast = struct_mem_property(ItemArr[RecastInfo, 0x18])

    def get_action_id(self, idx):
        # e8 * * * * 44 ? ? 85 ? 0f 84 ? ? ? ? 33
        try:
            k = FFDraw.instance.sq_pack.sheets.content_ex_action_sheet[self.content_ex_action_id].action_id[idx]
        except (IndexError, KeyError):
            return 0
        match k:
            case 10401:
                if me := Control.control_character:
                    if me.status.find_status(1467): return 10263
                    if me.status.find_status(1468): return 10265
                    if me.status.find_status(1469): return 10264
                    if me.status.find_status(1470): return 10262
            case 14213:
                if me := Control.control_character:
                    if me.status.find_status(1733): return 14415
                    if me.status.find_status(1734): return 14414
            case 20018:
                if me := Control.control_character:
                    if me.status.find_status(2264): return 19994
        return k

    def get_action_idx(self, action_id):
        return next((i for i in range(self.action_count) if self.get_action_id(i) == action_id), -1)
