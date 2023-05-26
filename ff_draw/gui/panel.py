import logging
import tkinter.filedialog
import typing

import glfw
import glm
import imgui

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

    def ffd_page(self):
        self.main.mem.panel.render()

        imgui.text('plugins')

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
        if imgui.collapsing_header('plugin paths')[0]:
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
            if imgui.button('add plugin path') and (p := tkinter.filedialog.askdirectory()):
                self.main.config['plugin_paths'].append(p)
                self.main.save_config()
            imgui.same_line()
            imgui.text('*plugin path change active when restart')

        if imgui.collapsing_header('gui')[0]:
            gui = self.main.gui
            clicked, gui.always_draw = imgui.checkbox("always_draw", gui.always_draw)
            if clicked:
                gui.cfg['always_draw'] = gui.always_draw
                self.main.save_config()

        if imgui.collapsing_header('sniffer')[0]:
            self.main.sniffer.render_panel()

        if imgui.collapsing_header('func_parser')[0]:
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
        self.is_expand, self.is_show = imgui.begin('FFDPanel', True, window_flag)
        glfw.set_window_size(self.window, *map(int, imgui.get_window_size()))
        if not self.is_expand: return imgui.end()
        win_pos = glm.vec2(*imgui.get_window_position())
        if any(win_pos):
            glfw.set_window_pos(self.window, *map(int, glm.vec2(*glfw.get_window_pos(self.window)) + win_pos))
        imgui.set_window_position(0, 0)

        plugin_keys = set(self.main.plugins.keys())
        if self.current_page not in plugin_keys:
            self.current_page = main_page
        if (imgui.text if self.current_page == main_page else imgui.button)(main_page):
            self.current_page = main_page

        for k in sorted(plugin_keys):
            imgui.same_line()
            if (imgui.text if self.current_page == k else imgui.button)(k):
                self.current_page = k
        try:
            if self.current_page == main_page:
                self.ffd_page()
            else:
                if p := self.main.plugins.get(self.current_page):
                    p.draw_panel()
        except Exception as e:
            self.logger.error('error in tab drawing', exc_info=e)
        imgui.end()
