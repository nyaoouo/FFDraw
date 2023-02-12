import logging
import math

import glm
import typing
import time

from nylib.utils import Counter

if typing.TYPE_CHECKING:
    from ff_draw.main import FFDraw

preset_colors = {
    'enemy': (glm.vec4(1.0, 0.6, 0.6, 0.1), glm.vec4(1.0, 0.2, 0.2, .7)),
    'g_enemy': (glm.vec4(1.0, 0.6, 0.2, 0.1), glm.vec4(1.0, 0.8, 0.5, .7)),
    'friend': (glm.vec4(0.6, 1.0, 0.6, 0.1), glm.vec4(0.2, 1.0, 0.2, .7)),
    'g_friend': (glm.vec4(0.6, 0.8, 1.0, 0.1), glm.vec4(0.7, 0.9, 1.0, .7)),
}

omen_counter = Counter()
pi_2 = math.pi / 2


class BaseOmen:
    logger = logging.getLogger('Omen')

    def __init__(
            self,
            main: 'FFDraw',
            pos,
            shape=None, scale=None,
            shape_scale=None,
            facing=0,
            surface_color=None,
            line_color=None,
            surface_line_color=None,
            line_width=3.0,
            duration=0,
            alpha=None,
    ):
        self.oid = omen_counter.get()
        self.main = main
        self.working = True
        self.start_at = time.time()
        self.shape = shape
        self.scale = scale
        self.shape_scale = shape_scale
        self.pos = pos
        self.facing = facing
        self.surface_color = surface_color
        self.line_color = line_color
        self.surface_line_color = surface_line_color
        self.line_width = line_width
        self.duration = duration
        self.alpha = alpha or 1
        self.current_alpha = 1
        self.main.omens[self.oid] = self
        self.logger.debug(f'create omen {self.oid}')

    def get_maybe_callable(self, f):
        return f(self) if callable(f) else f

    def get_color(self, c):
        if c:
            r, g, b, *a = c
            return glm.vec4(r, g, b, (self.current_alpha * a[0]) if a else self.current_alpha)

    def destroy(self):
        self.working = False
        self.main.omens.pop(self.oid, None)

    @property
    def remaining_time(self):
        return self.duration - (time.time() - self.start_at)

    @property
    def progress(self):
        return 1 - self.remaining_time / self.duration

    def draw(self):
        if not self.working or self.duration and time.time() - self.start_at > self.duration:
            self.destroy()
        if self.shape_scale is None:
            shape = self.get_maybe_callable(self.shape)
            scale = self.get_maybe_callable(self.scale)
        else:
            shape, scale = self.get_maybe_callable(self.shape_scale) or (None, None)
        if not self.working: self.destroy()
        if not shape: return
        self.current_alpha = self.get_maybe_callable(self.alpha)

        if self.surface_line_color is None:
            surface_color = self.get_color(self.get_maybe_callable(self.surface_color))
            line_color = self.get_color(self.get_maybe_callable(self.line_color))
        else:
            slc = self.get_maybe_callable(self.surface_line_color)
            surface_color, line_color = preset_colors.get(slc) if isinstance(slc, str) else (slc, None)
        pos = self.get_maybe_callable(self.pos)
        facing = self.get_maybe_callable(self.facing) or 0
        line_width = self.get_maybe_callable(self.line_width)
        self.main.gui.add_3d_shape(
            shape,
            glm.translate(pos) * glm.rotate(facing, glm.vec3(0, 1, 0)) * glm.scale(scale),
            surface_color, line_color, line_width,
        )
        if shape == 0x20002:  # 0x20000|2 *cross
            self.main.gui.add_3d_shape(
                shape,
                glm.translate(pos) * glm.rotate(facing + pi_2, glm.vec3(0, 1, 0)) * glm.scale(scale),
                surface_color, line_color, line_width,
            )
