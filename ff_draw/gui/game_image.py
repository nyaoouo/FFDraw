import base64
import io
import queue
import threading
import time
import traceback
import typing

import OpenGL.GL as gl
from PIL import Image
import imgui

from fpt4.utils.sqpack.utils import icon_path, map_path

if typing.TYPE_CHECKING:
    from . import Drawing


def img2tex(img: Image.Image) -> int:
    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, img.width, img.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, img.tobytes())
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_BORDER)  # transparent
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_BORDER)
    gl.glTexParameterfv(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_BORDER_COLOR, (0, 0, 0, 0))

    return texture


class DefaultIcons:
    error_icon = Image.open(io.BytesIO(base64.b64decode(
        b'iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEz0lEQVR4nO2dWYgdRRSG/7iNu7gQDVHcIiIqgpAXERGCL4IILmBEfEn'
        b'AJRNEBcUHHRUMkZnb53S8jETE8UUlBuKLy4tRJCaDookQcUHRQdEgGjXRjCaa/FJ3ccSZvsztruqqvl0f/C8z3Dp1/q7b3dPnVA8QiUQikUgkEolEIpH8cARHMcFKKt6l4K'
        b'eOtlCxwvyuwNCRLnwKp1IwSQXnlOADjmLhvx+I9A9HcAQF2zNNntGHfBmH5wgRMTDF6nmY3FaK1a0PRfqDDZzSOhfP12jBzxzDaX2GiVDw9LxNntF4dK4PmOBiKv7q22jB3'
        b'1yHy/qJVWuoeDvHau6avYXEAt85BA8VN+c2uasEN/nOI2jYwDFUfF3YaMU3XI9jfecTLBQ8YsHkrh72nU+QMMWZVPxu0ehpNnG277yCg4oXLZrcvTC+4DuvoGCKKyg45MDo'
        b'QxRc5Tu/IOAIDqPgfesmz5i93cRA3WH78ScdawXqDJ/ECRTsKsHoH7gWJ6GuUDBWgsndU8go6ggbWELBn6UZrdhPwYWoGxS8VqLJXb2KOkHFNR5M7upa1AGux5FUfObR6C+'
        b'YYgiDDhX3ezS5LcF9GGQ4ioVU/OrdaMVeNnEGBhUKng3A5K6ewSDCBJdTcTCnKXdzHCfPqQSrco550MwJgwYV7xQ4p96ROa7grgLjbh2oshcFywt+ze/JHFtxb8Gxb8HAlK'
        b'cEU4XMEDyYOb7goYJjf8tRHIeqQ8HjBVec0UiP8R+1MP5jqDIcw1kU7LNgxJrMGIq1FsafpuAcVBUqNlowgRQkPWKIpRgbUEWouNJieWrccutYltlXo0qYFloKPrJowHOZs'
        b'RQT1uIoPjatwqgKVNxpMXmaCnlmLMFLVmP1uGcPitZfa4ofLSe/KTOe4hXLB3W32WWA0KEitZw4qXg9M57gDevxBIqQoeAiCg44SPwtJ52n2TItw5cgVJysLm1pW4+Y2RuJ'
        b'ih3cNxEiTHG9yyYYZMVV7HAWN8F1CG4foOJzZwkrPsmMLfjU4QH+Mqiyl3no49BkUvBVZmw7/dS99ABCgIrTKdjjONnvM+O773TaywSLynV17kSfd5wozda2zPiKX5zHV0y'
        b'U6+rsJJcWKE+xD6MPdJ7SzZaL28nZMjku9WMysaCz8Z21kGDSS9mLgtu9J6+l67ZyTW7ieAq+CyBxlryqdzHFieUZrVjjPWn1ZvYT5Zic4DwK/vCesHrTfioucG+0YJOnlb'
        b'TPlJtaxdi2NliqR1p9bGvHZMUyT4lNmW/SrPmkOL+1S9bPyl7m8m0wOz0ZvbzHwb/V05x2Oil7UTHsaeWQ63Bu5rwSLPI2rwSr7L9AypR4fCUk2T0Xpv3W27xsl72oaHpMh'
        b'r364yz09RVV047JDVya620wdlf0lLnwzTG3JR4vhnbLXlRs9pwIO5pudT6ZXr52P9/Gzs8YgDYXNfnGAJJgJSS4IZ/JKYZMZcN7AloRGa8mcHSom+E5UEqwsn+jzQtXfU9c'
        b'KybB1v6NNm9G9D1xrZx25zH6twAmzkpJsKd/oxXveZ+4VkyCSbdvuo1ix4PhPEYPOW230oHTjtxvZ2cDi6PZmJ/JDSzOZfL/+uqGW+X2eIHkf87H5mZhW8ub+H8GIpFIJBK'
        b'JRCKRSCQSiaBe/ANxr83SYOzJ3gAAAABJRU5ErkJggg=='
    )))
    spinner_icon = Image.open(io.BytesIO(base64.b64decode(
        b'iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAACXBIWXMAAAsTAAALEwEAmpwYAAAGrUlEQVR4nO3cf2wTVRwA8AeCgMJfEolB/AEEIguCYKIS4tYOlLbDH0E'
        b'gGkED1/KHYOKvGE207SbG+SMKxigoCYbEtReIcB1bC5jaexMYvXvXwR1L710dIigCKgI6FdiZGxuM2W137bq73t4nef9ev/1+e++19759ABAEQRAEQRAEQRAEQRCEhX2w9+'
        b'ioKl66vbqheYzZsQwqfuFQWZAXdweRdCGIJFUbAV5ElejwclVVh5gdn60FkPhagBfbOhP/v8FLtD8eH2Z2nLZUyUlLekx8lxHgxffMjtV2/Ko6NIDEI7oKgKR//Zx4m9kx2'
        b'0qQk+7Tk/wud8Eas2O2lUokPmWwAOvMjtlW/Eh8wlABkFhtdsy24ufFyQYL8KTZMVtKvKVlZL7f0YNITOgqAC/94hfF0fm81po6eQQodkI6PV6QlfUIK8cErKgCVi4gjBtT'
        b'cmYFrarXGb1eJdc8PchL5/qY+9sCvLQ0l3gplqugILfbC7lWL+RUiuVOe2FyCwUbS0CxQbJcijD+tSPxWQbe1dxs/BGCnxPnBnjpRPYCiK0BJK00fE1VHeqFyY1a0rMONvk'
        b'PleCeBcWCx3iyIOMzPSf/ShG25nL96obmMQEkvhTgxV1BXpICSGQDvLi26sChCblcz8tyVT0m/+q4SCU4JygGSFZCfSf/ShHKzIyViu+/lYLJv3UUQPXCZBOwOu748RsEGb'
        b'caKMCnZsbrY7nn9SX/8ljFomnAyvh0+i79yW8f35oZLwWTnxgpgDdxYBGwsqbm76caKoCM95gZL8VyHxspAJVIPgqsTBTF6xFWzuotAML4QzPjpSDvM1IAXwM3CVgdkpUNu'
        b'pIv47YmjGeZGasvzo2lYPKczgI0gGLAHT5yi4CV41ZfgDtRbHKNjuS3+hKcqR8WQ5oymekI45Ze5v7N2nQFLMIHuTcoNnkp67wPuTM+ll8Aik0qlboRYfyyICt7kYxPdBSE'
        b'RnJmPrAgqqFxJsVym7yQS1OQO+VlOYFik2+v3LdvnNmxEQRBEARBEARBDGql8fjIivrELE89nOeJwhmzOW642TENCg9FExPcMXaTOwrPu2NQ7RyuGPzNFYXrKuLxsQMe1MF'
        b'MZhzCeI6AcYmqqkOBTXnqYZmW6K6JzzJ+dMcaZg5IQAfT6YmCjHciGV+6+mxfOYYU5RlgMw/XwxJXjD3bR/I7x0+ePXvHFzQgTpYnCVg52csmy+vARtxR+I3O5F+ekqJwS0'
        b'EDQliJ9bHNeFGbkoANLKhjpxlJfseacLFg64HW7abtZOnYanwH2IArBp8zWgBteGLw8YIEpPXx6NtuVL4GNuCKwbdyKYArClcXJCBeUWbr63ZQvgQ24InCV3MpgLueXVaQg'
        b'DiOGy5g5ZSOKWg5sAFXDLpymoKicEbBghIwXt1Ht8MhrVDABhbU1Y1wRdkTBgsgFTwwbZHtYTGWhOaWO4CNeGLQpzv5UbbNXZ/wDEhg7euBrKwXZFynNeQiWV5ppU6H/uSO'
        b'wY06C+Dv1xcmOqjqEFeMfbGXX8QnXVFoi3XP0h7b3XiTa1eCckfh5+4Y3OqKsp+5Y+zTj2xvIOdVEARBEARBEPlw0pHx5V9tv6d8a+3E2Rvs8UjF8uZv23azI8y87whHjjr'
        b'DEfXKCEXOOkKRUCldOzB7vYORM8QsdISZP65JfLfhCEcuOULMWr/fb9vGA1OUhZhFWnJ7S/61dwSzARQL7T/DCCuMIOOfkYzTCOPqXM6HKJT59I47HWHmvO7kd94NNFOYzZ'
        b'b+xGP8QLZ/zCOs7I9b5FRDR4jZbDT57QUIRX5YTNPWfeqrnQskYOVwz9uV8gtmx3g/TY9yhCJ/5lIAbZSHaucBq2pv2rLwv+M182hmbq7J77gLgsCqUpnMlD72jBNmx+gM1'
        b'S7OpwDOELMRWJXWI9rllKxsLSum7xqV1+yoyO8OYD4CViZgvKRr32iXDfu0dqSN2fE56O1T87oD6Ehh+n76v4kLpzrm/b8EGddoxxgAi3CGIjjH6adNe0wBBtOJiYXgDDGr'
        b'crwDcjpqjeimNB4f5ggzrMFvP6e1H3DdrzUoCRiX8Bgv4xXl3vwewkWa9E09kd/LaKa0f99FkUKy8ma3Rf6LXK9VStOjtWc8zhBzocdPfpiJl9fsnNK/76JI8ZnM3dm68lK'
        b'yvDCf62oLq4NmXnGGmW3a1OQIRyKOMFPtqKmd03/R20BKzqzooSG4yuzYBgU+nX7Qzh3ZRUHACt3t/wjf2aUjuyioqjokhfFShPG72pREkk8QBEEQBEEQBEEQBEGAIvEfgB'
        b'l/xP89dEAAAAAASUVORK5CYII='
    )))
    spinner_frames = 100
    spinner_dur = 1.5
    spinner_cache_key = '__game_icon_place_holder'

    def __init__(self, gui: 'Drawing'):
        self.main = gui.main
        self._placeholder_texture = [None for _ in range(self.spinner_frames)]
        self._error_texture = None

    @property
    def error_texture(self):
        if self._error_texture is None:
            self._error_texture = img2tex(self.error_icon)
        return self._error_texture

    @property
    def placeholder_texture(self):
        fc = self.main.gui.frame_cache
        if (tex := fc.get(self.spinner_cache_key)) is None:
            idx = int((time.time() % self.spinner_dur) / self.spinner_dur * self.spinner_frames)
            if self._placeholder_texture[idx] is None:
                self._placeholder_texture[idx] = tex = img2tex(
                    self.spinner_icon.rotate(idx * -360 / self.spinner_frames))
            else:
                tex = self._placeholder_texture[idx]
            fc[self.spinner_cache_key] = tex
        return tex

    def image_place_holder(self, width: int = None, height: int = None):
        if width is None: width = 64
        if height is None: height = 64
        imgui.image(self.placeholder_texture, width, height)

    def image_error(self, width: int = None, height: int = None):
        if width is None: width = 64
        if height is None: height = 64
        imgui.image(self.error_texture, width, height)


class GameImage:
    _load_game_icon_thread: threading.Thread | None = None

    def __init__(self, gui: 'Drawing'):
        self.main = gui.main
        self._game_icon_cache = {}
        self._game_map_cache = {}
        self._game_texture_cache = {}
        self._game_res_queue = queue.Queue()
        self._game_to_load_queue = queue.Queue()
        self.default_icons = DefaultIcons(gui)

    def load_game_texture(self):
        while True:
            try:
                texture_path, res = self._game_res_queue.get_nowait()
            except queue.Empty:
                break
            self._game_texture_cache[texture_path] = img2tex(res), (res.width, res.height)

    def assert_frame_load(self):
        fc = self.main.gui.frame_cache
        if '__is_game_img_load__' in fc: return
        self.load_game_texture()
        fc['__is_game_img_load__'] = True

    def load_game_res(self):
        while True:
            try:
                texture_path = self._game_to_load_queue.get_nowait()
            except queue.Empty:
                self._load_game_icon_thread = None
                break
            if self._game_texture_cache.get(texture_path) is None:
                try:
                    res = self.main.sq_pack.pack.get_texture_file(texture_path).get_image()
                except Exception as e:
                    self._game_texture_cache[texture_path] = e
                else:
                    self._game_res_queue.put((texture_path, res))

    def get_game_texture(self, texture_path):
        self.assert_frame_load()
        if texture_path not in self._game_texture_cache:
            self._game_texture_cache[texture_path] = None
            self._game_to_load_queue.put(texture_path)
            if not self._load_game_icon_thread or not self._load_game_icon_thread.is_alive():
                self._load_game_icon_thread = threading.Thread(target=self.load_game_res, daemon=True)
                self._load_game_icon_thread.start()
        return self._game_texture_cache[texture_path]

    def is_load(self, texture_path, auto_load=False):
        if self._game_texture_cache.get(texture_path) is None:
            if auto_load: self.get_game_texture(texture_path)
            return False
        return True

    def clear_cache(self):
        while self._game_texture_cache:
            k, v = self._game_texture_cache.popitem()
            if isinstance(v, tuple):
                gl.glDeleteTextures(v[0])
        self._game_icon_cache.clear()

    def _image(self, res, width=None, height=None, exc_handling=2, **kwargs):
        if res is None:
            self.default_icons.image_place_holder(width, height)
            return 1
        if isinstance(res, Exception):
            if exc_handling == 1:
                for line in traceback.format_exception(type(res), res, res.__traceback__):
                    imgui.text(line)
            elif exc_handling == 2:
                self.default_icons.image_error(width, height)
            return 2
        texture, (_width, _height) = res
        if width is None: width = _width
        if height is None: height = _height
        imgui.image(texture, width, height, **kwargs)
        return 0

    def image(self, texture_path, width=None, height=None, exc_handling=2, **kwargs):
        """
        :param texture_path: texture path
        :param width: image width, None for auto
        :param height: image height, None for auto
        :param exc_handling: 0 for ignore, 1 for show exception, 2 for show error icon
        :param args: imgui.image remain args
        :return: 0 for success, 1 for loading, 2 for load failed
        """
        return self._image(self.get_game_texture(texture_path), width, height, exc_handling, **kwargs)

    def icon_image(self, icon_id, width=None, height=None, hq_icon=True, exc_handling=2, **kwargs):
        """
        :param icon_id: icon id
        :param width: image width, None for auto
        :param height: image height, None for auto
        :param hq_icon: use hq icon
        :param exc_handling: 0 for ignore, 1 for show exception, 2 for show error icon
        :param args: imgui.image remain args
        :return: 0 for success, 1 for loading, 2 for load failed
        """
        if icon_id not in self._game_icon_cache:
            texture_path = icon_path(icon_id, hq_icon)
            res = self.get_game_texture(texture_path)
            if res is not None: self._game_icon_cache[icon_id] = res
        else:
            res = self._game_icon_cache[icon_id]
        return self._image(res, width, height, exc_handling, **kwargs)

    def map_image(self, map_id, width=None, height=None, size='m', exc_handling=2, **kwargs):
        """
        :param map_id: map id
        :param width: image width, None for auto
        :param height: image height, None for auto
        :param size: map size, 's' for small, 'm' for medium
        :param exc_handling: 0 for ignore, 1 for show exception, 2 for show error icon
        :param args: imgui.image remain args
        :return: 0 for success, 1 for loading, 2 for load failed
        """
        if map_id not in self._game_map_cache:
            try:
                texture_path = map_path(self.main.sq_pack, map_id, size)
            except Exception as e:
                res = e
            else:
                res = self.get_game_texture(texture_path)
            if res is not None: self._game_map_cache[map_id] = res
        else:
            res = self._game_map_cache[map_id]
        return self._image(res, width, height, exc_handling, **kwargs)
