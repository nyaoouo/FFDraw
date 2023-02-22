import glm
from ff_draw.gui.text import TextPosition
from ff_draw.plugins import FFDrawPlugin
import imgui


class Radar(FFDrawPlugin):
    def __init__(self, main):
        super().__init__(main)
        self.print_name = self.data.setdefault('print_name', True)
        self.show_imgui_window = True

    def draw_panel(self):
        if not self.show_imgui_window: return
        # if imgui.button("show name" if self.print_name else "not show name"):
        #     self.print_name = not self.print_name
        #     self.main.config.setdefault('radar', {})['print_name'] = self.print_name
        #     self.main.save_config()
        clicked, self.print_name = imgui.checkbox("show name", self.print_name)
        if clicked:
            self.data['print_name'] = self.print_name
            self.storage.save()

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
                self.main.gui.render_text(
                    actor.name,
                    (text_pos * glm.vec2(1, -1) + 1) * view.screen_size / 2,
                    color=(1, 0, 1),
                    at=TextPosition.center_bottom
                )
