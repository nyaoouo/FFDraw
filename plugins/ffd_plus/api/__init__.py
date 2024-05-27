import typing
# from .action_manager import ActionManager
# from .atk_stage import AtkStage
# from .charapc import CharaPc
from .control import Control
# from .event_framework import EventFramework
from .framework import Framework
# from .game_main import GameMain
# from .game_object_manager import GameObjectManager
# from .group_manager import GroupManager
from .pkt_work import PktWorks
# from .storage_manager import StorageManager
# from .ui import UiManager
# from .warp import Warp
# from .auto_move import AutoMove

if typing.TYPE_CHECKING:
    from .. import Bot


class Api:
    instance: 'Api' = None

    def __init__(self, bot: 'Bot'):
        Api.instance = self
        self.bot = bot
        self.handle = self._mem.handle
        self.scanner = self._mem.scanner_v2
        # self.action_manager = ActionManager(self)
        # self.atk_stage = AtkStage(self)
        # self.charapc = CharaPc(self)
        self.control = Control(self)
        # self.event_framework = EventFramework(self)
        self.framework = Framework(self)
        # self.ui_manager = UiManager(self)
        # self.game_main = GameMain(self)
        # self.game_object_manager = GameObjectManager(self)
        # self.group_manager = GroupManager(self)
        # self.storage_manager = StorageManager(self)
        # self.warp = Warp(self)

        # self.auto_move = AutoMove(self)
        self.pkt_work = PktWorks(self)

    def setup(self):
        pass
        # self.auto_move.setup()

    def unload(self):
        pass
        # self.auto_move.unload()

    @property
    def gui(self):
        return self.bot.main.main.gui

    @property
    def sniffer(self):
        return self.bot.main.main.sniffer

    @property
    def _mem(self):
        return self.bot.main.main.mem

    def render_panel(self):
        # self.action_manager.render_panel()
        # self.atk_stage.render_panel()
        # self.charapc.render_panel()
        self.control.render_panel()
        # self.event_framework.render_panel()
        self.framework.render_panel()
        # self.ui_manager.render_panel()
        # self.game_main.render_panel()
        # self.game_object_manager.render_panel()
        # self.group_manager.render_panel()
        # self.storage_manager.render_panel()
        # self.warp.render_panel()

        # self.auto_move.render_panel()

    def render_game(self):
        # self.action_manager.render_game()
        # self.atk_stage.render_game()
        # self.charapc.render_game()
        self.control.render_game()
        # self.event_framework.render_game()
        self.framework.render_game()
        # self.ui_manager.render_game()
        # self.game_main.render_game()
        # self.game_object_manager.render_game()
        # self.group_manager.render_game()
        # self.storage_manager.render_game()
        # self.warp.render_game()

        # self.auto_move.render_game()
