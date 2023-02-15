import glm
from ff_draw.gui import use_imgui
from ff_draw.gui.text import TextPosition
from ff_draw.plugins import FFDrawPlugin

if use_imgui:
    import imgui


class Radar(FFDrawPlugin):
    def __init__(self, main):
        super().__init__(main)
        self.print_name = self.main.config.setdefault('radar', {}).setdefault('print_name', True)
        self.show_imgui_window = use_imgui

    def render_imgui_window(self):
        if not self.show_imgui_window: return
        # if imgui.button("show name" if self.print_name else "not show name"):
        #     self.print_name = not self.print_name
        #     self.main.config.setdefault('radar', {})['print_name'] = self.print_name
        #     self.main.save_config()
        clicked, self.print_name = imgui.checkbox("show name", self.print_name)
        if clicked:
            self.main.config.setdefault('radar', {})['print_name'] = self.print_name
            self.main.save_config()

    def update(self, main):
        if self.show_imgui_window:
            expanded, self.show_imgui_window = imgui.begin('Radar', self.show_imgui_window)
            if expanded:
                self.render_imgui_window()
            imgui.end()
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
