import queue

import glfw
from imgui.integrations.glfw import GlfwRenderer as _GlfwRenderer


class GlfwRenderer(_GlfwRenderer):
    def __init__(self, window, shared_font_atlas=None):
        self.window = window
        super(_GlfwRenderer, self).__init__()
        self.queue = queue.Queue()

        glfw.set_key_callback(self.window, lambda *a: self.queue.put((self.keyboard_callback, a)))
        glfw.set_cursor_pos_callback(self.window, lambda *a: self.queue.put((self.mouse_callback, a)))
        glfw.set_window_size_callback(self.window, lambda *a: self.queue.put((self.resize_callback, a)))
        glfw.set_char_callback(self.window, lambda *a: self.queue.put((self.char_callback, a)))
        glfw.set_scroll_callback(self.window, lambda *a: self.queue.put((self.scroll_callback, a)))

        self.io.display_size = glfw.get_framebuffer_size(self.window)
        self.io.get_clipboard_text_fn = self._get_clipboard_text
        self.io.set_clipboard_text_fn = self._set_clipboard_text

        self._map_keys()
        self._gui_time = None

    def process_inputs(self, is_drawing=True):
        try:
            while True:
                callback, args = self.queue.get_nowait()
                callback(*args)
        except queue.Empty:
            pass
        super(GlfwRenderer, self).process_inputs()
