import base64
import io
import queue
import threading
import time
import typing
import zlib

import OpenGL.GL as gl
from PIL import Image
import imgui

from fpt4.utils.sqpack.utils import icon_path

if typing.TYPE_CHECKING:
    from . import Drawing

spinner = Image.open(io.BytesIO(zlib.decompress(base64.b64decode(
    b'eJwB+wYE+YlQTkcNChoKAAAADUlIRFIAAABgAAAAYAgGAAAA4ph3OAAAAAlwSFlzAAALEwAACxMBAJqcGAAABq1JREFUeJzt3H9sE1UcAPAHgoDCXxKJQfwBBCILgmCiEu'
    b'LWDpS2wx9BIBpBA9fyh2DirxhNtO0mxvkjCsYoKAmGxLUXiHAdWwuY2nsTGL1718EdS+9dHSIoAioCOhXYmRsbjNltd+26u97eJ3n/Xr/9fnvvtfe+fQAQBEEQBEEQBEEQ'
    b'BEEQhIV9sPfoqCpeur26oXmM2bEMKn7hUFmQF3cHkXQhiCRVGwFeRJXo8HJVVYeYHZ+tBZD4WoAX2zoT/7/BS7Q/Hh9mdpy2VMlJS3pMfJcR4MX3zI7VdvyqOjSAxCO6Co'
    b'Ckf/2ceJvZMdtKkJPu05P8LnfBGrNjtpVKJD5lsADrzI7ZVvxIfMJQAZBYbXbMtuLnxckGC/Ck2TFbSrylZWS+39GDSEzoKgAv/eIXxdH5vNaaOnkEKHZCOj1ekJX1CCvH'
    b'BKyoAlYuIIwbU3JmBa2q1xm9XiXXPD3IS+f6mPvbAry0NJd4KZaroCC32wu5Vi/kVIrlTnthcgsFG0tAsUGyXIow/rUj8VkG3tXcbPwRgp8T5wZ46UT2AoitASStNHxNVR'
    b'3qhcmNWtKzDjb5D5XgngXFgsd4siDjMz0n/0oRtuZy/eqG5jEBJL4U4MVdQV6SAkhkA7y4turAoQm5XM/LclU9Jv/quEglOCcoBkhWQn0n/0oRysyMlYrvv5WCyb91FED1'
    b'wmQTsDru+PEbBBm3GijAp2bG62O55/Ul//JYxaJpwMr4dPou/clvH9+aGS8Fk58YKYA3cWARsLKm5u+nGiqAjPeYGS/Fch8bKQCVSD4KrEwUxesRVs7qLQDC+EMz46Ug7z'
    b'NSAF8DNwlYHZKVDbqSL+O2JoxnmRmrL86NpWDynM4CNIBiwB0+couAleNWX4A7UWxyjY7kt/oSnKkfFkOaMpnpCOOWXub+zdp0BSzCB7k3KDZ5Keu8D7kzPpZfAIpNKpW6'
    b'EWH8siAre5GMT3QUhEZyZj6wIKqhcSbFcpu8kEtTkDvlZTmBYpNvr9y3b5zZsREEQRAEQRAEQQxqpfH4yIr6xCxPPZznicIZszluuNkxDQoPRRMT3DF2kzsKz7tjUO0crh'
    b'j8zRWF6yri8bEDHtTBTGYcwniOgHGJqqpDgU156mGZluiuic8yfnTHGmYOSEAH0+mJgox3IhlfuvpsXzmGFOUZYDMP18MSV4w920fyO8dPnj17xxc0IE6WJwlYOdnLJsvr'
    b'wEbcUfiNzuRfnpKicEtBA0JYifWxzXhRm5KADSyoY6cZSX7HmnCxYOuB1u2m7WTp2Gp8B9iAKwafM1oAbXhi8PGCBKT18ejbblS+BjbgisG3cimAKwpXFyQgXlFm6+t2UL'
    b'4ENuCJwldzKYC7nl1WkIA4jhsuYOWUjiloObABVwy6cpqConBGwYISMF7dR7fDIa1QwAYW1NWNcEXZEwYLIBU8MG2R7WExloTmljuAjXhi0Kc7+VG2zV2f8AxIYO3rgays'
    b'F2RcpzXkIlleaaVOh/7kjsGNOgvg79cXJjqo6hBXjH2xl1/EJ11RaIt1z9Ie2914k2tXgnJH4efuGNzqirKfuWPs049sbyDnVRAEQRAEQRD5cNKR8eVfbb+nfGvtxNkb7P'
    b'FIxfLmb9t2syPMvO8IR446wxH1yghFzjpCkVApXTswe72DkTPELHSEmT+uSXy34QhHLjlCzFq/32/bxgNTlIWYRVpye0v+tXcEswEUC+0/wwgrjCDjn5GM0wjj6lzOhyiU'
    b'+fSOOx1h5rzu5HfeDTRTmM2W/sRj/EC2f8wjrOyPW+RUQ0eI2Ww0+e0FCEV+WEzT1n3qq50LJGDlcM/blfILZsd4P02PcoQif+ZSAG2Uh2rnAatqb9qy8L/jNfNoZm6uye'
    b'+4C4LAqlKZzJQ+9owTZsfoDNUuzqcAzhCzEViV1iPa5ZSsbC0rpu8aldfsqMjvDmA+AlYmYLyka99olw37tHakjdnxOejtU/O6A+hIYfp++r+JC6c65v2/BBnXaMcYAItw'
    b'hiI4x+mnTXtMAQbTiYmF4Awxq3K8A3I6ao3opjQeH+YIM6zBbz+ntR9w3a81KAkYl/AYL+MV5d78HsJFmvRNPZHfy2imtH/fRZFCsvJmt0X+i1yvVUrTo7VnPM4Qc6HHT3'
    b'6YiZfX7JzSv++iSPGZzN3ZuvJSsrwwn+tqC6uDZl5xhplt2tTkCEcijjBT7aipndN/0dtASs6s6KEhuMrs2AYFPp1+0M4d2UVBwArd7f8I39mlI7soqKo6JIXxUoTxu9qU'
    b'RJJPEARBEARBEARBEARBgCLxH4AZf8T/PXRAAAAAAElFTkSuQmCCB8JURA=='
))))
spinner_frames = 100
spinner_dur = 3
place_holder_cache_key = '__game_icon_place_holder'


class GameIcon:
    _load_game_icon_thread: threading.Thread | None = None

    def __init__(self, gui: 'Drawing'):
        self.main = gui.main
        self._game_icon_texture_cache = {}
        self._game_icon_res_queue = queue.Queue()
        self._game_icon_to_load_queue = queue.Queue()
        self._placeholder_texture = None

    def placeholder_texture(self, idx):
        if self._placeholder_texture is None:
            self._placeholder_texture = gl.glGenTextures(spinner_frames)
            for i in range(spinner_frames):
                img = spinner.rotate(i * -360 / spinner_frames)
                gl.glBindTexture(gl.GL_TEXTURE_2D, self._placeholder_texture[i])
                gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, img.width, img.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, img.tobytes())
                gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
                gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        return self._placeholder_texture[idx]

    def imgui_image_place_holder(self, width: int = None, height: int = None):
        if width is None: width = 64
        if height is None: height = 64
        if (k := self.main.gui.frame_cache.get(place_holder_cache_key)) is None:
            self.main.gui.frame_cache[place_holder_cache_key] = k = self.placeholder_texture(int((time.time() % spinner_dur) / spinner_dur * spinner_frames))
        imgui.image(k, width, height)

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
        if res is None:
            return self.imgui_image_place_holder(width, height, *args)
        texture, (_width, _height) = res
        if width is None: width = _width
        if height is None: height = _height
        return imgui.image(texture, width, height, *args)
