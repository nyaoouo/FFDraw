import os
import threading
import typing

import OpenGL.GL as gl
import glfw
import glm
import imgui

from nylib.utils import ResEvent, safe
# from imgui.integrations.glfw import GlfwRenderer
from .glfw_fix import GlfwRenderer

if os.name == 'nt':
    import ctypes

    os_scale = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
else:
    os_scale = 1.


class Window:
    def __init__(
            self,
            mgr: 'WindowManager',
            guid: str, draw_func,
            x_pad=10,
            y_pad=10,
            init_width=1024,
            init_height=980,
            title=None,
            on_want_close=None,
            before_window_draw=None,
            after_window_draw=None,
            closable=True,
    ):
        self.mgr = mgr
        self.guid = guid
        self._title = title or guid
        self.draw_func = draw_func
        self._x_pad = x_pad
        self._y_pad = y_pad
        self._init_width = init_width
        self._init_height = init_height
        self.on_want_close = on_want_close
        self.before_window_draw = before_window_draw
        self.after_window_draw = after_window_draw
        self.closable = closable
        self.imgui_window_flag = 0

        if not glfw.init():
            raise Exception("glfw can not be initialized")
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE)
        glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
        glfw.window_hint(glfw.DECORATED, glfw.FALSE)
        window_width = init_width + x_pad * 2
        window_height = init_height + y_pad * 2
        self.window = glfw.create_window(window_width, window_height, self._title, None, None)
        screen = glfw.get_video_mode(glfw.get_primary_monitor())[0]
        glfw.set_window_pos(self.window, (screen.width - window_width) // 2, (screen.height - window_height) // 2)

        glfw.make_context_current(self.window)
        try:
            shared_font_atlas = imgui.get_io().fonts
        except imgui.ImGuiError:
            shared_font_atlas = None
        self.imgui_ctx = imgui.create_context(shared_font_atlas)
        imgui.set_current_context(self.imgui_ctx)
        self.imgui_renderer = GlfwRenderer(self.window)
        if self.mgr.init_imgui():
            glfw.swap_interval(1)
            self.imgui_renderer.refresh_font_texture()

    def update(self):
        self.mgr.ensure_thread()
        if self.mgr.any_window_select:
            raise RuntimeError('only one window can be select at the same time')
        self.mgr.any_window_select = True
        glfw.make_context_current(self.window)

        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
        imgui.set_current_context(self.imgui_ctx)
        self.imgui_renderer.process_inputs()

        imgui.new_frame()
        imgui.push_font(self.mgr.imgui_font)

        win_pad = glm.vec2(self._x_pad, self._y_pad)
        imgui.set_next_window_position(*win_pad, imgui.FIRST_USE_EVER)
        imgui.set_next_window_size(self._init_width, self._init_height, imgui.FIRST_USE_EVER)
        self.before_window_draw and self.before_window_draw(self)
        do_draw, is_show = imgui.begin(self._title + '###' + self.guid, self.closable, self.imgui_window_flag)
        if is_show:
            win_size = glm.vec2(*imgui.get_window_size()) + (win_pad * 2)
            glfw.set_window_size(self.window, *map(int, win_size))
            win_pos = glm.vec2(*imgui.get_window_position()) - win_pad
            if any(win_pos):
                glfw.set_window_pos(self.window, *map(int, glm.vec2(*glfw.get_window_pos(self.window)) + win_pos))
            imgui.set_window_position(*win_pad)
            if do_draw:
                self.draw_func(self)
        elif self.on_want_close is None or self.on_want_close(self):
            glfw.set_window_should_close(self.window, True)

        imgui.end()
        self.after_window_draw and self.after_window_draw(self)
        imgui.pop_font()
        imgui.end_frame()
        imgui.render()

        self.imgui_renderer.render(imgui.get_draw_data())
        glfw.swap_buffers(self.window)
        self.mgr.any_window_select = False

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self.mgr.ensure_thread()
        if value == self._title: return
        self._title = value
        glfw.set_window_title(self.window, value)

    def close(self):
        self.mgr.ensure_thread()
        if self.on_want_close is None or self.on_want_close(self):
            glfw.set_window_should_close(self.window, True)


class WindowManager:
    imgui_font: typing.Any

    def __init__(self, font_size=16, ini_file_name: bytes | None = b'imgui.ini', default_font_path: str = None):
        self.ident = -1
        self.font_size = font_size * os_scale
        self._ini_file_name = ini_file_name
        self._default_font_path = default_font_path
        self.any_window_select = False
        self.windows = {}
        self.calls_before_draw = []

    def ensure_thread(self):
        if self.ident == -1:
            self.ident = threading.get_ident()
        elif self.ident != threading.get_ident():
            raise RuntimeError('current thread is not the main thread')

    def init_imgui(self):
        self.ensure_thread()
        if hasattr(self, 'imgui_font'): return False
        imgui_io = imgui.get_io()
        if self._default_font_path and os.path.exists(self._default_font_path):
            fonts = imgui_io.fonts
            self.imgui_font = fonts.add_font_from_file_ttf(self._default_font_path, self.font_size, None, fonts.get_glyph_ranges_chinese_full())
        else:
            self.imgui_font = None
        imgui_io.ini_file_name = self._ini_file_name
        return True

    def _new_window(
            self,
            guid: str,
            draw_func, x_pad=10,
            y_pad=10,
            init_width=1024,
            init_height=980,
            title=None,
            on_want_close=None,
            before_window_draw=None,
            after_window_draw=None,
    ):
        assert guid not in self.windows, f'window {guid} already exists'
        self.windows[guid] = window = Window(self, guid, draw_func, x_pad, y_pad, init_width, init_height, title, on_want_close, before_window_draw, after_window_draw)
        return window

    def new_window(
            self,
            guid: str,
            draw_func, x_pad=10,
            y_pad=10,
            init_width=1024,
            init_height=980,
            title=None,
            on_want_close=None,
            before_window_draw=None,
            after_window_draw=None,
    ):
        res = ResEvent()
        self.calls_before_draw.append(lambda: res.set(self._new_window(guid, draw_func, x_pad, y_pad, init_width, init_height, title, on_want_close, before_window_draw, after_window_draw)))
        return res

    def update(self):
        self.ensure_thread()
        while self.calls_before_draw:
            self.calls_before_draw.pop()()
        if not self.windows: return False
        glfw.poll_events()
        for title, window in list(self.windows.items()):
            if glfw.window_should_close(window.window):
                glfw.destroy_window(window.window)
                self.windows.pop(title)
            else:
                window.update()
        return True

    def run(self):
        self.ensure_thread()
        while self.update():
            pass

    def terminate(self):
        self.ensure_thread()
        for window in self.windows.values():
            safe(window.imgui_renderer.shutdown)
            safe(imgui.set_current_context, window.imgui_ctx)
            safe(imgui.destroy_context, window.imgui_ctx)
            safe(glfw.destroy_window, window.window)
        self.windows.clear()
        glfw.terminate()


def main():
    mgr = WindowManager()

    class SubWindow:
        def __init__(self, value):
            self.value = value
            self.tmp_title = None

        def __call__(self, window: Window):
            imgui.text(f'this is sub window {self.value}')
            imgui.text(f'guid {window.guid}')
            imgui.text(f'imgui win size {imgui.get_window_size()}')
            imgui.text(f'imgui win pos {imgui.get_window_position()}')
            imgui.text(f'glfw win size {glfw.get_window_size(window.window)}')
            imgui.text(f'glfw win pos {glfw.get_window_pos(window.window)}')
            if self.tmp_title is None: self.tmp_title = window.title
            _, window.title = imgui.input_text('title', window.title, 1024)

    class MainWindow:
        def __init__(self, mgr: WindowManager):
            self.mgr = mgr
            self.counter = 0

        def __call__(self, window: Window):
            imgui.text(f'fps {imgui.get_io().framerate:.2f}')
            imgui.text(f'imgui win size {imgui.get_window_size()}')
            imgui.text(f'imgui win pos {imgui.get_window_position()}')
            imgui.text(f'glfw win size {glfw.get_window_size(window.window)}')
            imgui.text(f'glfw win pos {glfw.get_window_pos(window.window)}')
            imgui.text(f'counter {self.counter}')
            if imgui.button('click me'):
                v = self.counter
                self.counter += 1
                self.mgr.new_window(f'window_{v}', SubWindow(v))

    mgr.new_window('main', MainWindow(mgr))
    mgr.run()


if __name__ == '__main__':
    main()
