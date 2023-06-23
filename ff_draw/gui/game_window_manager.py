import typing

import glfw
import imgui
import win32gui
import OpenGL.GL as gl

from nylib.utils.imgui.window_mgr import WindowManager
from . import window

if typing.TYPE_CHECKING:
    from . import Drawing


class DrawWindow:
    guid = -1
    def __init__(self, mgr: 'FFDWindowManager', game_hwnd):
        self.mgr = mgr
        self.game_hwnd = game_hwnd
        self.window = window.init_window('ffd draw window', True, None, game_hwnd)
        try:
            shared_font_atlas = imgui.get_io().fonts
        except imgui.ImGuiError:
            shared_font_atlas = None
        self.imgui_ctx = imgui.create_context(shared_font_atlas)
        imgui.set_current_context(self.imgui_ctx)
        from . import ffd_imgui
        self.imgui_renderer = ffd_imgui.OpenglPynputRenderer(self.window)
        if self.mgr.init_imgui():
            glfw.swap_interval(1)
            self.imgui_renderer.refresh_font_texture()

    def update(self):
        gui = self.mgr.gui
        glfw.make_context_current(self.window)
        imgui.set_current_context(self.imgui_ctx)
        imgui.new_frame()
        if self.mgr.imgui_font:
            imgui.push_font(self.mgr.imgui_font)
        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glClear(gl.GL_DEPTH_BUFFER_BIT)

        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_BLEND)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        pv = gui.get_view().projection_view
        gl.glLoadMatrixf(pv.to_list())

        if gui.always_draw or win32gui.GetForegroundWindow() == self.game_hwnd:
            window.set_window_cover(self.window, self.game_hwnd)
            for draw_func in gui.draw_update_call.copy():
                try:
                    draw_func(gui.main)
                except Exception as e:
                    gui.logger.error(f"draw_func error, func will be remove:", exc_info=e)
                    gui.draw_update_call.remove(draw_func)
                    raise
        else:
            gl.glClearColor(0, 0, 0, 0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        if self.mgr.imgui_font:
            imgui.pop_font()
        imgui.end_frame()
        imgui.render()
        self.imgui_renderer.render(imgui.get_draw_data())
        glfw.swap_buffers(self.window)

    def close(self):
        self.imgui_renderer.shutdown()
        imgui.set_current_context(self.imgui_ctx)
        imgui.destroy_context(self.imgui_ctx)
        glfw.destroy_window(self.window)


class FFDWindowManager(WindowManager):
    draw_window: DrawWindow

    def __init__(self, gui: 'Drawing', *args, **kwargs):
        self.gui = gui
        super().__init__(*args, **kwargs)

    def update(self):
        if super().update():
            self.current_window = self.draw_window
            self.draw_window.update()
            self.current_window = None
            return True
        else:
            self.draw_window.close()
            return False

    def terminate(self):
        self.draw_window.close()
        super().terminate()
