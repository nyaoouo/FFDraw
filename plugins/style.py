import glm
import imgui

from ff_draw.plugins import FFDrawPlugin
from ff_draw.omen import preset_colors

styles = [
    ('Text color', imgui.COLOR_TEXT),
    ('Background color', imgui.COLOR_WINDOW_BACKGROUND),
]


class StyleEditor(FFDrawPlugin):
    def __init__(self, main):
        super().__init__(main)

        self._old_imgui_begin = imgui.begin
        imgui.begin = self.imgui_begin

        self.style_colors = self.data.setdefault('style_colors', {})

    def on_unload(self):
        imgui.begin = self._old_imgui_begin

    def imgui_begin(self, *args, **kwargs):
        pop_cnt = 0
        for k, code in styles:
            if color := self.style_colors.get(k):
                imgui.push_style_color(code, *color)
                pop_cnt += 1
        res = self._old_imgui_begin(*args, **kwargs)

        old_end = imgui.end

        def new_end():
            old_end()
            imgui.end = old_end
            for _ in range(pop_cnt):
                imgui.pop_style_color()

        imgui.end = new_end
        return res

    def draw_panel(self):
        with imgui.begin_tab_bar("styleEditorBar") as tab_bar:
            if tab_bar.opened:
                with imgui.begin_tab_item("绘制") as item1:
                    if item1.selected:
                        self.omen_preset_color_editor()
                with imgui.begin_tab_item("界面") as item2:
                    if item2.selected:
                        self.style_editor()

    def style_editor(self):
        for k, code in styles:
            if not (color := self.style_colors.get(k)):
                color = imgui.get_style_color_vec_4(code)
            if imgui.button(f'reset##style_color_reset_{code}'):
                self.style_colors.pop(k, None)
                self.storage.save()
            imgui.same_line()
            changed, new_color = imgui.color_edit4(f'##style_color_select_{code}', *color, imgui.COLOR_EDIT_FLOAT)
            imgui.same_line()
            imgui.text(k)
            if changed:
                self.style_colors[k] = new_color
                self.storage.save()

    def omen_preset_color_editor(self):
        imgui.columns(4)
        imgui.text('Name')
        imgui.next_column()
        imgui.text('Surface')
        imgui.next_column()
        imgui.text('Line')
        imgui.next_column()
        imgui.text('-')
        imgui.next_column()
        imgui.separator()
        for k in self.main.preset_omen_colors.keys():
            surface_color, line_color = self.main.preset_omen_colors[k]
            if surface_color is None: surface_color = glm.vec4()
            if line_color is None: line_color = glm.vec4()

            imgui.text(k)
            imgui.next_column()
            changed, new_surface_color = imgui.color_edit4(f'##{k}_surface_color', *surface_color,
                                                           imgui.COLOR_EDIT_FLOAT)
            if changed: self.apply_color(k, False, new_surface_color)
            imgui.next_column()
            changed, new_line_color = imgui.color_edit4(f'##{k}_line_color', *line_color, imgui.COLOR_EDIT_FLOAT)
            if changed: self.apply_color(k, True, new_line_color)
            imgui.next_column()
            if imgui.button(f'reset##{k}_reset'):
                new_surface_color, new_line_color = preset_colors.get(k, [None, None])
                self.apply_color(k, False, new_surface_color)
                self.apply_color(k, True, new_line_color)
            imgui.next_column()
        imgui.columns(1)

    def apply_color(self, k, is_line, color: tuple[float, float, float, float] | glm.vec4):
        if isinstance(color, tuple):
            color = glm.vec4(*color)
        if is_line:
            surface_color = self.main.preset_omen_colors.get(k, [None, None])[0]
            line_color = color
        else:
            surface_color = color
            line_color = self.main.preset_omen_colors.get(k, [None, None])[1]

        self.main.preset_omen_colors[k] = surface_color, line_color

        self.main.config.setdefault('omen', {}).setdefault('preset_colors', {})[k] = {
            'surface': list(surface_color) if line_color is not None else None,
            'line': list(line_color) if line_color is not None else None,
        }
        self.main.save_config()
