import time
import typing

import glm

if typing.TYPE_CHECKING:
    from . import BaseOmen


def trans_fast_to_slow(p):
    return -(p - 1) ** 2 + 1


class Effector:
    def __init__(self, omen: 'BaseOmen'):
        self.omen = omen
        self.start_at = time.time()

    def on_end(self):
        pass

    def display(self):
        return True

    def update(self):
        return True

    def color(self, c: glm.vec4):
        return c

    def pos(self, p: glm.vec3):
        return p

    def scale(self, s: glm.vec3):
        return s


class ScaleInEffector(Effector):
    duration = .3
    percent = 0

    def update(self):
        self.percent = (time.time() - self.start_at) / self.duration
        return self.percent < 1

    def scale(self, s: glm.vec3):
        return s * trans_fast_to_slow(self.percent)


class OutEffector(Effector):
    duration = 1
    percent = 0

    def __init__(self, omen: 'BaseOmen'):
        super().__init__(omen)

        omen._shape = omen.get_maybe_callable(omen._shape)
        omen._scale = omen.get_maybe_callable(omen._scale)
        omen._shape_scale = omen.get_maybe_callable(omen._shape_scale)
        omen._pos = omen.get_maybe_callable(omen._pos)
        omen._facing = omen.get_maybe_callable(omen._facing)
        omen._surface_color = omen.get_maybe_callable(omen._surface_color)
        omen._line_color = omen.get_maybe_callable(omen._line_color)
        omen._surface_line_color = omen.get_maybe_callable(omen._surface_line_color)
        omen._line_width = omen.get_maybe_callable(omen._line_width)
        omen._label = omen.get_maybe_callable(omen._label)
        omen._label_color = omen.get_maybe_callable(omen._label_color)
        omen._label_scale = omen.get_maybe_callable(omen._label_scale)
        omen._label_at = omen.get_maybe_callable(omen._label_at)
        omen._alpha = omen.get_maybe_callable(omen._alpha)

    def update(self):
        self.percent = (time.time() - self.start_at) / self.duration
        if not self.percent < 1:
            self.omen.destroy()
            return False
        return True


class ScaleOutEffector(OutEffector):
    duration = .2

    def scale(self, s: glm.vec3):
        return s * (1 - self.percent)


class FadeOutEffector(OutEffector):
    duration = .2

    def color(self, c: glm.vec4):
        return glm.vec4(*c.xyz, c.w * (1 - self.percent))
