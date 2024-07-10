import typing
from nylib.utils import LazyClassAttr
from nylib.utils.imgui import ctx as imgui_ctx

from ff_draw.mem.utils import struct_mem_property
from ffd_plus.api.utils.commons import ItemArr
from ffd_plus.api.utils.commons import simple_type as st

from .quest_work import QuestWork

if typing.TYPE_CHECKING:
    from .. import Api


class CharaPcOffsets:
    quests = 0x10
    _quest_completed_flags = 0x2E0
    _quest_marker_visible_flags = 0X593

    _is_validate_ = False

    @classmethod
    def validate(cls):
        if cls._is_validate_: return cls
        from ffd_plus.api import Api
        if Api.instance.scanner.find_val(
                "42 ? ? ? <? ? ? ?> 0f ? ? 84 ? 75 ? 40"
        )[0] != cls._quest_marker_visible_flags: raise Exception('CharaPcOffsets is not validate')
        cls._is_validate_ = True
        return cls


class CharaPc:
    instance: 'CharaPc' = None
    offsets: 'CharaPcOffsets' = None

    def __init__(self, api: 'Api'):
        assert CharaPc.instance is None, "CharaPc already initialized"
        CharaPc.instance = self
        self.handle = api.handle
        self.address, = api.scanner.find_val("48 ? ? * * * * e8 ? ? ? ? c6 44 24 ? ? 0f")
        if CharaPc.offsets is None:
            CharaPc.offsets = CharaPcOffsets.validate()

    quests = struct_mem_property(ItemArr[QuestWork, QuestWork.offsets.size_, 30])
    _quest_completed_flags = struct_mem_property(st.uint8_arr)
    _quest_marker_visible_flags = struct_mem_property(st.uint8_arr)

    def is_quest_completed(self, quest_id: int) -> bool:
        if quest_id >> 16 > 1: return False
        quest_id &= 0xffff
        if not quest_id: return True
        return self._quest_completed_flags[quest_id // 8] & (0x80 >> (quest_id % 8)) != 0

    def is_quest_marker_visible(self, marker_id: int) -> bool:
        return self._quest_marker_visible_flags[marker_id // 8] & (0x80 >> (marker_id % 8)) != 0

    def render_panel(self):
        with imgui_ctx.TreeNode(f'CharaPc#{self.address:X}', push_id=True) as n, n:
            with imgui_ctx.TreeNode(f'Quests', push_id=True) as n_, n_:
                for quest in self.quests:
                    if quest.id:
                        quest.render_panel()

    def render_game(self):
        pass
