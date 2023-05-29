import logging
import tkinter.filedialog
import typing
import glfw
import glm
import imgui

from .default_style import set_style, pop_style, text_tip, style_color_default, set_color
from .i18n import *
from ..omen import preset_colors

if typing.TYPE_CHECKING:
    from . import Drawing
main_page = 'FFDraw'


class FFDPanel:
    logger = logging.getLogger('Panel')

    def __init__(self, gui: 'Drawing'):
        self.main = gui.main
        self.renderer = gui.imgui_panel_renderer
        self.window = gui.window_panel
        self.is_expand = True
        self.is_show = True
        self.current_page = ''

        # 初始化
        self.lang_idx = self.main.config.setdefault('language', 0)
        i18n.current_lang = self.lang_idx
        self.style_color = self.main.config.setdefault('style_color', style_color_default)

    def ffd_page(self):
        with imgui.begin_tab_bar("tabBar") as tab_bar:
            if tab_bar.opened:
                with imgui.begin_tab_item(i18n(Panel) + '###tab_panel') as item1:
                    if item1.selected:
                        self.main.mem.panel.render()
                with imgui.begin_tab_item(i18n(Plugin) + '###tab_plugin') as item2:
                    if item2.selected:
                        self.tab_plugin()
                with imgui.begin_tab_item(i18n(Style) + '###tab_style') as item3:
                    if item3.selected:
                        self.tab_style()
                with imgui.begin_tab_item(i18n(Setting) + '###tab_setting') as item4:
                    if item4.selected:
                        self.tab_setting()

    def tab_plugin(self):
        """插件标签页"""
        imgui.text(i18n(Enable_plugin))

        for k, v in self.main.enable_plugins.items():
            clicked, v = imgui.checkbox(k.replace('/', '-'), v)
            if clicked:
                if v:
                    self.main.reload_plugin(k)
                elif p := self.main.plugins.pop(k, None):
                    p.unload()
                self.main.enable_plugins[k] = v
                self.main.save_config()
        imgui.new_line()
        if imgui.collapsing_header(i18n(Custom_plugin_path), None, imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            for i, path in list(enumerate(self.main.config['plugin_paths'])):
                imgui.text(path)
                imgui.same_line()
                if imgui.button(f'delete##delete_plugin_path_{i}'):
                    self.main.config['plugin_paths'].pop(i)
                    self.main.save_config()
                imgui.same_line()
                if imgui.button(f'edit##edit_plugin_path_{i}'):
                    if p := tkinter.filedialog.askdirectory():
                        self.main.config['plugin_paths'][i] = p
                        self.main.save_config()
                    self.main.save_config()
            if imgui.button(i18n(Add)) and (p := tkinter.filedialog.askdirectory()):
                self.main.config['plugin_paths'].append(p)
                self.main.save_config()
            text_tip(i18n(Enable_plugin_tooltip))

    def tab_style(self):
        flag = imgui.TREE_NODE_DEFAULT_OPEN
        if imgui.collapsing_header(i18n(GUI), None, flag)[0]:
            changed, new_color = imgui.color_edit3(f'##style_color_select_1', *self.style_color['color_main_up'])
            imgui.same_line()
            imgui.text(i18n(Color))
            if changed:
                set_color(self.style_color, new_color, self.style_color['color_background'])
                self.main.save_config()

            style = imgui.get_style()
            changed, style.alpha = imgui.slider_float(i18n(Opacity), self.style_color['alpha'], 0.5, 1)
            if changed:
                self.style_color['alpha'] = style.alpha
                self.main.save_config()

        if imgui.collapsing_header(i18n(Omen_draw))[0]:
            imgui.columns(3)
            imgui.set_column_width(0, 150)
            imgui.set_column_width(1, 600)
            imgui.text(i18n(Name))
            imgui.next_column()
            imgui.text(i18n(Color))
            imgui.next_column()
            imgui.next_column()
            for k in self.main.preset_omen_colors.keys():
                imgui.separator()
                surface_color, line_color = self.main.preset_omen_colors[k]
                if surface_color is None: surface_color = glm.vec4()
                if line_color is None: line_color = glm.vec4()

                imgui.text(k)
                imgui.next_column()
                changed, new_surface_color = imgui.color_edit4(f'##{k}_surface_color', *surface_color)
                if changed: self.apply_color(k, False, new_surface_color)
                imgui.same_line()
                imgui.text(i18n(Padding))
                imgui.next_column()
                if imgui.button(f'reset##{k}_reset'):
                    new_surface_color, new_line_color = preset_colors.get(k, [None, None])
                    self.apply_color(k, False, new_surface_color)
                    self.apply_color(k, True, new_line_color)
                imgui.next_column()
                imgui.next_column()
                changed, new_line_color = imgui.color_edit4(f'##{k}_line_color', *line_color)
                if changed: self.apply_color(k, True, new_line_color)
                imgui.same_line()
                imgui.text(i18n(Border))
                imgui.next_column()
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

    def tab_setting(self):
        """设置标签页"""
        flag = imgui.TREE_NODE_DEFAULT_OPEN
        if imgui.collapsing_header(i18n(Normal) + '###tab_setting_div_normal', None, flag)[0]:
            imgui.text(i18n(Language))
            changed, self.lang_idx = imgui.combo('##lang', self.lang_idx, ['English', '简体中文'])
            if changed:
                i18n.current_lang = self.lang_idx
                self.main.config['language'] = self.lang_idx
                self.main.save_config()
            # imgui.text(localStr('代理', self.language))
            # imgui.same_line()
            # changed, _ = imgui.input_text('地址','1')
            # if changed:

        if imgui.collapsing_header(i18n(Omen_draw) + '###tab_setting_div_draw', None, flag)[0]:
            gui = self.main.gui
            clicked, gui.always_draw = imgui.checkbox(i18n(Always_drawing), gui.always_draw)
            if clicked:
                gui.cfg['always_draw'] = gui.always_draw
                self.main.save_config()

        if imgui.collapsing_header(i18n(Sniffer) + '###tab_setting_div_sniffer', None, flag)[0]:
            self.main.sniffer.render_panel()

        if imgui.collapsing_header(i18n(Func_parser) + '###tab_setting_div_func_parser', None, flag)[0]:
            parser = self.main.parser
            clicked, parser.print_compile = imgui.checkbox(i18n(Print_compile), parser.print_compile)
            if clicked:
                parser.compile_config.setdefault('print_debug', {})['enable'] = parser.print_compile
                self.main.save_config()

    def draw(self):
        if not self.is_show:
            glfw.iconify_window(self.window)
            self.is_show = True
            return
        if glfw.get_window_attrib(self.window, glfw.ICONIFIED):
            return
        window_flag = 0
        if not self.is_expand: window_flag |= imgui.WINDOW_NO_MOVE

        set_style(self.style_color)  # 设置gui风格
        imgui.set_next_window_size(1280, 720, imgui.FIRST_USE_EVER)
        self.is_expand, self.is_show = imgui.begin('FFDraw', True, window_flag)
        glfw.set_window_size(self.window, *map(int, imgui.get_window_size()))
        if not self.is_expand: return imgui.end()
        win_pos = glm.vec2(*imgui.get_window_position())
        if any(win_pos):
            glfw.set_window_pos(self.window, *map(int, glm.vec2(*glfw.get_window_pos(self.window)) + win_pos))
        imgui.set_window_position(0, 0)

        # panel窗口绘制
        imgui.set_cursor_pos_y(50)
        imgui.set_cursor_pos_x(20)
        imgui.begin_child('##leftFrame', 250, 0)
        # --左侧导航窗口
        plugin_keys = set(self.main.plugins.keys())
        if self.current_page not in plugin_keys:
            self.current_page = main_page
        plugins = [main_page] + list(sorted(plugin_keys))
        for name in plugins:
            button_w = 245
            button_h = 50
            button_name = ' ' + name + ' ' * 200
            imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (10, 6))
            imgui.push_style_color(imgui.COLOR_BORDER, *self.style_color['color_main_up'])
            imgui.push_style_color(imgui.COLOR_BUTTON, *self.style_color['color_background2'])
            imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, *self.style_color['color_main_up'])
            if name == self.current_page:  # 选中的按钮
                imgui.text("")
                imgui.same_line(spacing=10)
                imgui.push_style_color(imgui.COLOR_BUTTON, *self.style_color['color_main_up'])
                imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, *self.style_color['color_main_up'])
                imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, *self.style_color['color_main_up'])
                imgui.button("", 10, button_h)
                imgui.pop_style_color(3)

                imgui.same_line()
                imgui.push_style_color(imgui.COLOR_BUTTON, *self.style_color['color_background'])
                imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, *self.style_color['color_background'])
                imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, *self.style_color['color_background'])
                imgui.push_style_color(imgui.COLOR_TEXT, *self.style_color['color_main_up_up'])
                if imgui.button(button_name, button_w - 30, button_h):
                    self.current_page = name
                imgui.pop_style_color(4)
            else:  # 未选中的
                imgui.push_style_var(imgui.STYLE_FRAME_BORDERSIZE, 1)
                if imgui.button(button_name, button_w, button_h):
                    self.current_page = name
                imgui.pop_style_var()
            imgui.pop_style_color(3)
            imgui.pop_style_var()

        # if (imgui.text if self.current_page == main_page else imgui.button)(main_page):
        #     self.current_page = main_page
        imgui.end_child()
        imgui.same_line(spacing=25)
        imgui.begin_child('##rightFrame', 0, 0)
        # --右侧插件页面
        try:
            if self.current_page == main_page:
                self.ffd_page()
            else:
                if p := self.main.plugins.get(self.current_page):
                    p.draw_panel()
        except Exception as e:
            self.logger.error('error in tab drawing', exc_info=e)
        imgui.end_child()

        imgui.end()
        pop_style()
