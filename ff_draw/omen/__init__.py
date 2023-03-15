import logging
import math

import glm
import typing
import time

from nylib.utils import Counter
from .hit_check import hit_check
from . import effector

if typing.TYPE_CHECKING:
    from ff_draw.main import FFDraw

preset_colors = {
    'enemy': (glm.vec4(1.0, 0.6, 0.6, 0.2), glm.vec4(1.0, 0.2, 0.2, .7)),
    'g_enemy': (glm.vec4(1.0, 0.6, 0.2, 0.2), glm.vec4(1.0, 0.8, 0.5, .7)),
    'friend': (glm.vec4(0.6, 1.0, 0.6, 0.2), glm.vec4(0.2, 1.0, 0.2, .7)),
    'g_friend': (glm.vec4(0.6, 0.8, 1.0, 0.2), glm.vec4(0.7, 0.9, 1.0, .7)),
}

omen_counter = Counter()
pi_2 = math.pi / 2


class BaseOmen:
    logger = logging.getLogger('Omen')
    shape = 0
    scale = glm.vec3(0, 0, 0)
    pos = glm.vec3(0, 0, 0)
    facing = 0
    surface_color = glm.vec4(0, 0, 0, 0)
    line_color = glm.vec4(0, 0, 0, 0)
    line_width = 5
    label = ''
    label_color = (0, 0, 0)
    label_scale = 1
    label_at = 1
    effectors: list[effector.Effector]

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

            label='',
            label_color=None,
            label_scale=1,
            label_at=1,

            duration=0,
            in_effector=effector.ScaleInEffector,
            out_effector=effector.FadeOutEffector,
            alpha=None,
    ):
        self.oid = omen_counter.get()
        self.main = main
        self.preset_colors = self.main.preset_omen_colors
        self.working = True
        self.start_at = time.time()
        self._shape = shape
        self._scale = scale
        self._shape_scale = shape_scale
        self._pos = pos
        self._facing = facing
        self._surface_color = surface_color
        self._line_color = line_color
        self._surface_line_color = surface_line_color
        self._line_width = line_width

        self._label = label
        self._label_color = label_color or (0, 0, 0)
        self._label_scale = label_scale
        self._label_at = label_at

        self.duration = duration
        self._alpha = alpha or 1
        self.current_alpha = 1
        self.main.omens[self.oid] = self
        # self.logger.debug(f'create omen {self.oid}')

        self.effectors = []
        self._out_effect_playing = False
        self._out_effector = out_effector
        if in_effector: self.apply_effect(in_effector)

    def get_maybe_callable(self, f):
        return f(self) if callable(f) else f

    def get_color(self, c):
        if c:
            r, g, b, *a = c
            _c = glm.vec4(r, g, b, (self.current_alpha * a[0]) if a else self.current_alpha)
            for eff in self.effectors:
                _c = eff.color(_c)
            return _c

    def apply_effect(self, eff: typing.Type[effector.Effector]):
        if (e := eff.create(self)) and e.update():
            self.effectors.append(e)

    def timeout(self):
        self.duration = -1

    def destroy(self):
        self.working = False
        self.main.omens.pop(self.oid, None)
        return False

    @property
    def remaining_time(self):
        return self.duration - self.play_time

    @property
    def play_time(self):
        return time.time() - self.start_at

    @property
    def progress(self):
        return 1 - self.remaining_time / self.duration

    def is_hit(self, dst: glm.vec3):
        return hit_check(self.shape, self.scale, self.pos, self.facing, dst)

    def draw(self):
        if not self.working: return self.destroy()
        self.effectors = [eff for eff in self.effectors if eff.update()]
        if not self.working: return self.destroy()
        if self.duration and time.time() - self.start_at > self.duration:
            if self._out_effector:
                if not self._out_effect_playing:
                    self.apply_effect(self._out_effector)
            else:
                return self.destroy()
        if self._shape_scale is None:
            self.shape = self.get_maybe_callable(self._shape)
            self.scale = self.get_maybe_callable(self._scale)
        else:
            self.shape, self.scale = self.get_maybe_callable(self._shape_scale) or (None, None)
        if isinstance(self.scale, (tuple, list)):
            self.scale = glm.vec3(*self.scale)
        for eff in self.effectors:
            self.scale = eff.scale(self.scale)
        if not self.working: return self.destroy()
        self.pos = None
        if self.shape:
            self.pos = self.get_maybe_callable(self._pos)
            if self.pos is None: return
            for eff in self.effectors:
                self.pos = eff.pos(self.pos)
            if isinstance(self.pos, (tuple, list)):
                self.pos = glm.vec3(*self.pos)
            self.facing = self.get_maybe_callable(self._facing) or 0
            self.current_alpha = self.get_maybe_callable(self._alpha)
            if self._surface_line_color is None:
                surface_color = self.get_maybe_callable(self._surface_color)
                line_color = self.get_maybe_callable(self._line_color)
                self.surface_color = self.get_color(self.preset_colors.get(surface_color)[0] if surface_color in self.preset_colors else surface_color)
                self.line_color = self.get_color(self.preset_colors.get(line_color)[1] if line_color in self.preset_colors else line_color)
            else:
                slc = self.get_maybe_callable(self._surface_line_color)
                self.surface_color, self.line_color = map(self.get_color, self.preset_colors.get(slc) if isinstance(slc, str) else (slc, None))
            self.line_width = self.get_maybe_callable(self._line_width)
            self.render()
            if self.shape == 0x20002:  # 0x20000|2 *cross
                self.render(True)
        self.label = self.get_maybe_callable(self._label)
        if self.label:
            if self.pos is None:
                self.pos = self.get_maybe_callable(self._pos)
                if self.pos is None: return
            view = self.main.gui.get_view()
            label_pos, is_in_screen = view.world_to_screen(*self.pos)
            if is_in_screen:
                self.main.gui.render_text(
                    self.label,
                    (label_pos * glm.vec2(1, -1) + 1) * view.screen_size / 2,
                    self.get_maybe_callable(self._label_scale),
                    self.get_maybe_callable(self._label_color),
                    self.get_maybe_callable(self._label_at)
                )

    def render(self, cross=False):
        f = self.facing + pi_2 if cross else self.facing
        self.main.gui.add_3d_shape(
            self.shape,
            glm.translate(self.pos) * glm.rotate(f, glm.vec3(0, 1, 0)) * glm.scale(self.scale),
            self.surface_color, self.line_color, self.line_width,
        )


def on_get_line_shape(omen: 'Line'):
    omen._pos = omen.src = src = omen.get_maybe_callable(omen._src)
    omen.dst = dst = omen.get_maybe_callable(omen._dst)
    if not (src and dst and src != dst): return 0
    dis = glm.distance(src, dst)
    omen._scale = glm.vec3(dis, 1, dis)
    omen._facing = glm.polar(dst - src).y
    omen.long = math.atan2(src.y - dst.y, glm.distance(src.xz, dst.xz))
    return 0x80000


class Line(BaseOmen):
    src: glm.vec3 = None
    dst: glm.vec3 = None
    long = 0

    def __init__(self, main: 'FFDraw', src, dst, line_color=None, line_width=3.0, label='',
                 label_color=None, label_scale=1, label_at=1, duration=0, alpha=None):
        self._src = src
        self._dst = dst
        super().__init__(
            main=main,
            pos=lambda o: o.pos,
            shape=on_get_line_shape, scale=lambda o: o.shape,
            facing=lambda o: o.facing,
            line_color=line_color,
            line_width=line_width,

            label=label,
            label_color=label_color,
            label_scale=label_scale,
            label_at=label_at,

            duration=duration,
            alpha=alpha,
        )

    def render(self, _=None):
        self.main.gui.add_3d_shape(
            self.shape,
            glm.translate(self.pos) * glm.rotate(self.facing, glm.vec3(0, 1, 0)) * glm.rotate(self.long, glm.vec3(1, 0, 0)) * glm.scale(self.scale),
            self.surface_color, self.line_color, self.line_width,
        )
