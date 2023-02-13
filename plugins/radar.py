import glm
from ff_draw.gui.text import TextPosition
from ff_draw.plugins import FFDrawPlugin


class Radar(FFDrawPlugin):
    def __init__(self, main):
        super().__init__(main)
        self.print_name = self.main.config.setdefault('radar', {}).setdefault('print_name', True)

    def update(self, main):
        view = main.gui.get_view()
        for actor in main.mem.actor_table:
            pos = actor.pos
            main.gui.add_3d_shape(
                0x90000,
                glm.translate(pos),
                point_color=glm.vec4(1, 1, 1, .7),
            )
            if self.print_name:
                text_pos, valid = view.world_to_screen(*pos)
                if not valid: continue
                self.main.gui.text_mgr.render_text(
                    actor.name,
                    (text_pos * glm.vec2(1, -1) + 1) * view.screen_size / 2,
                    color=(1, 0, 1),
                    at=TextPosition.center_bottom
                )
