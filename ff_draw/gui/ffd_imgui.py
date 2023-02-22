import queue

import glfw

import imgui
from imgui.integrations import compute_fb_scale
from imgui.integrations.opengl import ProgrammablePipelineRenderer
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

        self._map_keys()
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
        io.keys_down[key.vk] = is_press
        io.key_ctrl = io.keys_down[nput_ctrl] or io.keys_down[nput_ctrl_l] or io.keys_down[nput_ctrl_r]
        io.key_alt = io.keys_down[nput_alt] or io.keys_down[nput_alt_l] or io.keys_down[nput_alt_r]
        io.key_shift = io.keys_down[nput_shift] or io.keys_down[nput_shift_l] or io.keys_down[nput_shift_r]
        io.key_super = io.keys_down[nput_cmd] or io.keys_down[nput_cmd_l] or io.keys_down[nput_cmd_r]
        if key.char and 32 <= (c := ord(key.char)):
            io.add_input_character(c)

    def _get_clipboard_text(self):
        return glfw.get_clipboard_string(self.window)

    def _set_clipboard_text(self, text):
        glfw.set_clipboard_string(self.window, text)

    def _map_keys(self):
        key_map = self.io.key_map

        key_map[imgui.KEY_SPACE] = nput_space
        key_map[imgui.KEY_TAB] = nput_tab
        key_map[imgui.KEY_LEFT_ARROW] = nput_left
        key_map[imgui.KEY_RIGHT_ARROW] = nput_right
        key_map[imgui.KEY_UP_ARROW] = nput_up
        key_map[imgui.KEY_DOWN_ARROW] = nput_down
        key_map[imgui.KEY_PAGE_UP] = nput_page_up
        key_map[imgui.KEY_PAGE_DOWN] = nput_page_down
        key_map[imgui.KEY_HOME] = nput_home
        key_map[imgui.KEY_END] = nput_end
        key_map[imgui.KEY_DELETE] = nput_delete
        key_map[imgui.KEY_BACKSPACE] = nput_backspace
        key_map[imgui.KEY_ENTER] = nput_enter
        key_map[imgui.KEY_ESCAPE] = nput_esc

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
