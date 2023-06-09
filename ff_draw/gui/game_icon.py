import queue
import threading
import typing

import OpenGL.GL as gl
import imgui

from fpt4.utils.sqpack.utils import icon_path

if typing.TYPE_CHECKING:
    from . import Drawing


class GameIcon:
    _load_game_icon_thread: threading.Thread | None = None

    def __init__(self, gui: 'Drawing'):
        self.main = gui.main
        self._game_icon_texture_cache = {}
        self._game_icon_res_queue = queue.Queue()
        self._game_icon_to_load_queue = queue.Queue()

    def load_game_icon_texture(self):
        while True:
            try:
                to_load_id, res = self._game_icon_res_queue.get_nowait()
            except queue.Empty:
                break
            texture = gl.glGenTextures(1)
            gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, res.width, res.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, res.tobytes())
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            self._game_icon_texture_cache[to_load_id] = texture, (res.width, res.height)

    def load_game_icon_res(self):
        while True:
            try:
                to_load_id = self._game_icon_to_load_queue.get_nowait()
            except queue.Empty:
                self._load_game_icon_thread = None
                break
            if self._game_icon_texture_cache.get(to_load_id) is None:
                try:
                    res = self.main.sq_pack.pack.get_texture_file(icon_path(to_load_id, True)).get_image()
                except Exception as e:
                    self._game_icon_texture_cache[to_load_id] = e
                else:
                    self._game_icon_res_queue.put((to_load_id, res))

    def get_gl_texture(self, icon_id, raise_exc=True):
        if icon_id not in self._game_icon_texture_cache:
            self._game_icon_texture_cache[icon_id] = None
            self._game_icon_to_load_queue.put(icon_id)
            if not self._load_game_icon_thread or not self._load_game_icon_thread.is_alive():
                self._load_game_icon_thread = threading.Thread(target=self.load_game_icon_res, daemon=True)
                self._load_game_icon_thread.start()
        res = self._game_icon_texture_cache[icon_id]
        if raise_exc and isinstance(res, Exception): raise res
        return res

    def is_load(self, icon_id, auto_load=False):
        if self._game_icon_texture_cache.get(icon_id) is None:
            if auto_load: self.get_gl_texture(icon_id, False)
            return False
        return True

    def clear_cache(self):
        while self._game_icon_texture_cache:
            k, v = self._game_icon_texture_cache.popitem()
            if isinstance(v, tuple):
                gl.glDeleteTextures(v[0])

    def imgui_image(self, icon_id, width=None, height=None, *args):
        res = self.get_gl_texture(icon_id)
        if res is None: return None  # todo: load default icon
        texture, (_width, _height) = res
        if width is None: width = _width
        if height is None: height = _height
        return imgui.image(texture, width, height, *args)
