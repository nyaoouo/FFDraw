import glm
from ff_draw.gui.text import TextPosition
from ff_draw.plugins import FFDrawPlugin


class Fps(FFDrawPlugin):
    def __init__(self, main):
        super().__init__(main)
        self.print_fps_cfg = self.main.config.setdefault('fps', {})
        self.fps_text = f'fps: 0'
        self.mission = self.main.gui.timer.add_mission(
            (lambda: setattr(self, 'fps_text', f'fps: {self.main.gui.timer.fps}')),
            self.print_fps_cfg.setdefault('interval', 1), 0
        )

    def on_unload(self):
        self.main.gui.timer.remove_mission(self.mission)

    def update(self, main):
        view = self.main.gui.get_view()
        self.main.gui.render_text(
            self.fps_text,
            glm.vec2(0, view.screen_size.y),
            color=(1, 1, 0),
            at=TextPosition.left_bottom
        )
