import queue

import glfw

import imgui
from imgui.integrations import compute_fb_scale
from imgui.integrations.opengl import ProgrammablePipelineRenderer
from nylib.utils.imgui.glfw_fix import GlfwRenderer
from pynput import mouse, keyboard

nput_alt = keyboard.Key.alt.value.vk
nput_alt_gr = keyboard.Key.alt_gr.value.vk
nput_alt_l = keyboard.Key.alt_l.value.vk
nput_alt_r = keyboard.Key.alt_r.value.vk
nput_backspace = keyboard.Key.backspace.value.vk
nput_caps_lock = keyboard.Key.caps_lock.value.vk
nput_cmd = keyboard.Key.cmd.value.vk
nput_cmd_l = keyboard.Key.cmd_l.value.vk
nput_cmd_r = keyboard.Key.cmd_r.value.vk
nput_ctrl = keyboard.Key.ctrl.value.vk
nput_ctrl_l = keyboard.Key.ctrl_l.value.vk
nput_ctrl_r = keyboard.Key.ctrl_r.value.vk
nput_delete = keyboard.Key.delete.value.vk
nput_down = keyboard.Key.down.value.vk
nput_end = keyboard.Key.end.value.vk
nput_enter = keyboard.Key.enter.value.vk
nput_esc = keyboard.Key.esc.value.vk
nput_f1 = keyboard.Key.f1.value.vk
nput_home = keyboard.Key.home.value.vk
nput_insert = keyboard.Key.insert.value.vk
nput_left = keyboard.Key.left.value.vk
nput_media_next = keyboard.Key.media_next.value.vk
nput_media_play_pause = keyboard.Key.media_play_pause.value.vk
nput_media_previous = keyboard.Key.media_previous.value.vk
nput_media_volume_down = keyboard.Key.media_volume_down.value.vk
nput_media_volume_mute = keyboard.Key.media_volume_mute.value.vk
nput_media_volume_up = keyboard.Key.media_volume_up.value.vk
nput_menu = keyboard.Key.menu.value.vk
nput_num_lock = keyboard.Key.num_lock.value.vk
nput_page_down = keyboard.Key.page_down.value.vk
nput_page_up = keyboard.Key.page_up.value.vk
nput_pause = keyboard.Key.pause.value.vk
nput_print_screen = keyboard.Key.print_screen.value.vk
nput_right = keyboard.Key.right.value.vk
nput_scroll_lock = keyboard.Key.scroll_lock.value.vk
nput_shift = keyboard.Key.shift.value.vk
nput_shift_l = keyboard.Key.shift_l.value.vk
nput_shift_r = keyboard.Key.shift_r.value.vk
nput_space = keyboard.Key.space.value.vk
nput_tab = keyboard.Key.tab.value.vk
nput_up = keyboard.Key.up.value.vk
nput_mouse_to_idx = {
    mouse.Button.left: 0,
    mouse.Button.right: 1,
    mouse.Button.middle: 2,
    mouse.Button.x1: 3,
    mouse.Button.x2: 4,
}

nput2glfw = {}
nput2glfw[nput_space] = glfw.KEY_SPACE
nput2glfw[nput_tab] = glfw.KEY_TAB
nput2glfw[nput_left] = glfw.KEY_LEFT
nput2glfw[nput_right] = glfw.KEY_RIGHT
nput2glfw[nput_up] = glfw.KEY_UP
nput2glfw[nput_down] = glfw.KEY_DOWN
nput2glfw[nput_page_up] = glfw.KEY_PAGE_UP
nput2glfw[nput_page_down] = glfw.KEY_PAGE_DOWN
nput2glfw[nput_home] = glfw.KEY_HOME
nput2glfw[nput_end] = glfw.KEY_END
nput2glfw[nput_delete] = glfw.KEY_DELETE
nput2glfw[nput_backspace] = glfw.KEY_BACKSPACE
nput2glfw[nput_enter] = glfw.KEY_ENTER
nput2glfw[nput_esc] = glfw.KEY_ESCAPE
nput2glfw[nput_ctrl_l] = glfw.KEY_LEFT_CONTROL
nput2glfw[nput_ctrl_r] = glfw.KEY_RIGHT_CONTROL
nput2glfw[nput_ctrl] = glfw.KEY_LEFT_CONTROL
nput2glfw[nput_shift_l] = glfw.KEY_LEFT_SHIFT
nput2glfw[nput_shift_r] = glfw.KEY_RIGHT_SHIFT
nput2glfw[nput_shift] = glfw.KEY_LEFT_SHIFT
nput2glfw[nput_alt_l] = glfw.KEY_LEFT_ALT
nput2glfw[nput_alt_r] = glfw.KEY_RIGHT_ALT
nput2glfw[nput_alt] = glfw.KEY_LEFT_ALT
nput2glfw[nput_cmd_l] = glfw.KEY_LEFT_SUPER
nput2glfw[nput_cmd_r] = glfw.KEY_RIGHT_SUPER
nput2glfw[nput_cmd] = glfw.KEY_LEFT_SUPER
nput2glfw[nput_caps_lock] = glfw.KEY_CAPS_LOCK
nput2glfw[nput_scroll_lock] = glfw.KEY_SCROLL_LOCK
nput2glfw[nput_num_lock] = glfw.KEY_NUM_LOCK
nput2glfw[nput_print_screen] = glfw.KEY_PRINT_SCREEN
nput2glfw[nput_pause] = glfw.KEY_PAUSE
nput2glfw[nput_f1] = glfw.KEY_F1
nput2glfw[nput_f1 + 1] = glfw.KEY_F2
nput2glfw[nput_f1 + 2] = glfw.KEY_F3
nput2glfw[nput_f1 + 3] = glfw.KEY_F4
nput2glfw[nput_f1 + 4] = glfw.KEY_F5
nput2glfw[nput_f1 + 5] = glfw.KEY_F6
nput2glfw[nput_f1 + 6] = glfw.KEY_F7
nput2glfw[nput_f1 + 7] = glfw.KEY_F8
nput2glfw[nput_f1 + 8] = glfw.KEY_F9
nput2glfw[nput_f1 + 9] = glfw.KEY_F10
nput2glfw[nput_f1 + 10] = glfw.KEY_F11
nput2glfw[nput_f1 + 11] = glfw.KEY_F12




class OpenglPynputRenderer(ProgrammablePipelineRenderer):
    def __init__(self, window, shared_font_atlas=None):
        self.ctx = imgui.create_context(shared_font_atlas)
        super(OpenglPynputRenderer, self).__init__()
        self.window = window
        self.call_queue = queue.Queue()
        self.mouse_thread = mouse.Listener(
            on_move=lambda *args: self.call_queue.put((self._on_mouse_move, args)),
            on_click=lambda *args: self.call_queue.put((self.on_mouse_click, args)),
            on_scroll=lambda *args: self.call_queue.put((self.on_mouse_scroll, args))
        )
        self.key_thread = keyboard.Listener(
            on_press=lambda k: self.call_queue.put((self.on_key_change, (k, True))),
            on_release=lambda k: self.call_queue.put((self.on_key_change, (k, False)))
        )

        glfw.set_window_size_callback(self.window, self.resize_callback)

        self.io.display_size = glfw.get_framebuffer_size(self.window)
        self.io.get_clipboard_text_fn = self._get_clipboard_text
        self.io.set_clipboard_text_fn = self._set_clipboard_text

        GlfwRenderer._map_keys(self)
        self._gui_time = None
        self.mouse_thread.start()
        self.key_thread.start()
        self.cached_mouse_pos = -1, -1

    def shutdown(self):
        super(OpenglPynputRenderer, self).shutdown()
        self.mouse_thread.stop()
        self.key_thread.stop()
        self.mouse_thread.join()
        self.key_thread.join()

    def _on_mouse_move(self, x: float, y: float):
        self.cached_mouse_pos = x, y

    def on_mouse_click(self, x: float, y: float, button: mouse.Button, pressed: bool):
        io = self.io
        self._on_mouse_move(x, y)
        if button in nput_mouse_to_idx:
            io.mouse_down[nput_mouse_to_idx[button]] = pressed

    def on_mouse_scroll(self, x: float, y: float, dx: float, dy: float):
        io = self.io
        self._on_mouse_move(x, y)
        io.mouse_wheel_horizontal = dx
        io.mouse_wheel = dy

    def on_key_change(self, key: str | keyboard.Key | keyboard.KeyCode, is_press):
        if not key: return
        io = self.io
        if isinstance(key, keyboard.Key):
            key = key.value
        elif isinstance(key, str):
            key = keyboard.KeyCode.from_char(key)
        key: keyboard.KeyCode
        if key.vk in nput2glfw:
            io.keys_down[nput2glfw[key.vk]] = is_press
        io.key_ctrl = (
                io.keys_down[glfw.KEY_LEFT_CONTROL] or
                io.keys_down[glfw.KEY_RIGHT_CONTROL]
        )
        io.key_alt = (
                io.keys_down[glfw.KEY_LEFT_ALT] or
                io.keys_down[glfw.KEY_RIGHT_ALT]
        )
        io.key_shift = (
                io.keys_down[glfw.KEY_LEFT_SHIFT] or
                io.keys_down[glfw.KEY_RIGHT_SHIFT]
        )
        io.key_super = (
                io.keys_down[glfw.KEY_LEFT_SUPER] or
                io.keys_down[glfw.KEY_RIGHT_SUPER]
        )
        if is_press and key.char and 32 <= (c := ord(key.char)):
            io.add_input_character(c)

    def _get_clipboard_text(self):
        return glfw.get_clipboard_string(self.window)

    def _set_clipboard_text(self, text):
        glfw.set_clipboard_string(self.window, text)

    def resize_callback(self, window, width, height):
        self.io.display_size = width, height

    def process_inputs(self, is_drawing=True):
        glfw.make_context_current(self.window)
        imgui.set_current_context(self.ctx)
        self.io = io = imgui.get_io()

        while not self.call_queue.empty():
            try:
                call, args = self.call_queue.get(False)
            except queue.Empty:
                break
            else:
                call(*args)

        window_size = glfw.get_window_size(self.window)
        fb_size = glfw.get_framebuffer_size(self.window)

        io.display_size = window_size
        io.display_fb_scale = compute_fb_scale(window_size, fb_size)
        io.delta_time = 1.0 / 60

        current_time = glfw.get_time()
        if is_drawing:
            wx, wy = glfw.get_window_pos(self.window)
            x, y = self.cached_mouse_pos
            io.mouse_pos = x - wx, y - wy
        else:
            io.mouse_pos = -1, -1
        if self._gui_time:
            self.io.delta_time = current_time - self._gui_time
        else:
            self.io.delta_time = 1. / 60.

        self._gui_time = current_time

    def render(self, draw_data):
        super(OpenglPynputRenderer, self).render(draw_data)
        glfw.swap_buffers(self.window)


class FFDGlfwRenderer(GlfwRenderer):
    def __init__(self, window, shared_font_atlas=None):
        self.ctx = imgui.create_context(shared_font_atlas)
        super(FFDGlfwRenderer, self).__init__(window)

    def _map_keys(self): ...

    def process_inputs(self, is_drawing=True):
        glfw.make_context_current(self.window)
        imgui.set_current_context(self.ctx)
        super(FFDGlfwRenderer, self).process_inputs()

    def render(self, draw_data):
        super(FFDGlfwRenderer, self).render(draw_data)
        glfw.swap_buffers(self.window)
