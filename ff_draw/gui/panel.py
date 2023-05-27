import logging
import tkinter.filedialog
import typing
import glfw
import glm
import imgui

from .default_style import set_style, pop_style, text_tip, style_color_default, set_color

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

        # 初始化界面颜色
        self.style_color = self.main.config.setdefault('style_color', style_color_default)

    def ffd_page(self):
        with imgui.begin_tab_bar("tabBar") as tab_bar:
            if tab_bar.opened:
                with imgui.begin_tab_item("控制台") as item1:
                    if item1.selected:
                        self.main.mem.panel.render()
                with imgui.begin_tab_item("插件") as item2:
                    if item2.selected:
                        self.tab_plugin()
                with imgui.begin_tab_item("配色") as item3:
                    if item3.selected:
                        self.tab_style()
                with imgui.begin_tab_item("设置") as item4:
                    if item4.selected:
                        self.tab_setting()

    def tab_plugin(self):
        """插件标签页"""
        imgui.text('启用插件')

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
        if imgui.collapsing_header('自定义插件路径', None, imgui.TREE_NODE_DEFAULT_OPEN)[0]:
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
            if imgui.button('添加') and (p := tkinter.filedialog.askdirectory()):
                self.main.config['plugin_paths'].append(p)
                self.main.save_config()
            text_tip('*重启FFDraw后路径更改生效')

    def tab_style(self):
        flag = imgui.TREE_NODE_DEFAULT_OPEN
        if imgui.collapsing_header('界面', None, flag)[0]:
            changed, new_color = imgui.color_edit3(f'##style_color_select_1', *self.style_color['color_main_up'])
            imgui.same_line()
            imgui.text('配色')
            if changed:
                set_color(self.style_color, new_color, self.style_color['color_background'])
                self.main.save_config()

            style = imgui.get_style()
            changed, style.alpha = imgui.slider_float("透明度", self.style_color['alpha'], 0.5, 1)
            if changed:
                self.style_color['alpha'] = style.alpha
                self.main.save_config()

        if imgui.collapsing_header('绘制', None, flag)[0]:
            pass

    def tab_setting(self):
        """设置标签页"""
        flag = imgui.TREE_NODE_DEFAULT_OPEN
        if imgui.collapsing_header('gui', None, flag)[0]:
            gui = self.main.gui
            clicked, gui.always_draw = imgui.checkbox("始终绘制", gui.always_draw)
            if clicked:
                gui.cfg['always_draw'] = gui.always_draw
                self.main.save_config()

        if imgui.collapsing_header('sniffer', None, flag)[0]:
            self.main.sniffer.render_panel()

        if imgui.collapsing_header('func_parser', None, flag)[0]:
            parser = self.main.parser
            clicked, parser.print_compile = imgui.checkbox("print_compile", parser.print_compile)
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
        imgui.set_next_window_size(1280, 720, imgui.ONCE)
        self.is_expand, self.is_show = imgui.begin('FFDPanel', True, window_flag)
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
