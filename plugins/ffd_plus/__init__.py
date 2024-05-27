from ff_draw.plugins import FFDrawPlugin
from nylib.utils import safe
from nylib.utils.imgui import ctx as imgui_ctx
from .utils.loop import BasicUpdateLoop
from .api import Api
# from .combat import CombatManager
# from .moving import MoveModule
# from .teri import TerrainManager
# from .missions import MissionStack


class Bot:
    instance: 'Bot' = None

    def __init__(self, main: 'FFDPlus'):
        Bot.instance = self
        self.main = main
        self.storage = main.storage
        self.sq_pack = main.main.sq_pack
        self.api = Api(self)
        self.loop = BasicUpdateLoop().add_call(self.main_loop)
        # self.combat = CombatManager(self)
        # self.moving = MoveModule(self)
        # self.teri = TerrainManager(self)
        # self.mission_stack = MissionStack(self)

        try:
            self.setup()
        except Exception:
            self.unload()
            raise

    @property
    def config(self):
        return self.storage.data

    def save_config(self):
        self.storage.save()

    def setup(self):
        self.api.setup()
        # self.combat.setup()
        # self.teri.setup()
        # self.moving.setup()
        self.loop.start()

    def unload(self):
        self.loop.close()
        # safe(self.moving.unload)
        # safe(self.teri.unload)
        # safe(self.combat.unload)
        safe(self.api.unload)

    def main_loop(self):
        pass
        # self.combat.update()
        # self.moving.update()
        # self.teri.update()
        # self.mission_stack.update()

    def render_game(self):
        # self.combat.render_game()
        # self.moving.render_game()
        # self.teri.render_game()
        self.api.render_game()
        # self.mission_stack.render_game()

    def render_panel(self):
        # with imgui_ctx.TreeNode('combat') as n, n:
        #     self.combat.render_panel()
        # with imgui_ctx.TreeNode('moving') as n, n:
        #     self.moving.render_panel()
        # with imgui_ctx.TreeNode('teri') as n, n:
        #     self.teri.render_panel()
        with imgui_ctx.TreeNode('Api') as n, n:
            self.api.render_panel()
        # with imgui_ctx.TreeNode('MissionStack') as n, n:
        #     self.mission_stack.render_panel()


class FFDPlus(FFDrawPlugin):
    def __init__(self, main):
        super().__init__(main)
        self.bot = Bot(self)

    def unload(self):
        self.bot.unload()

    def update(self, main):
        self.bot.render_game()

    def draw_panel(self):
        self.bot.render_panel()
