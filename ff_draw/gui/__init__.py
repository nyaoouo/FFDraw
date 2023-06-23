import logging
import queue
import threading
import time
import typing
import os

from nylib.utils import Counter, ResEvent

os.environ['PYGLFW_LIBRARY'] = os.path.join(res_path := os.path.join(os.environ['ExcPath'], 'res'), 'glfw3.dll')
os.environ['PYGLFW_PREVIEW'] = 'True'
os.environ["PATH"] += os.pathsep + res_path

import glm
import glfw
import imgui
from . import window, view, text, panel as m_panel, default_style, game_image, game_window_manager
from .utils import common_shader, models

if typing.TYPE_CHECKING:
    from ff_draw.main import FFDraw
    from . import ffd_imgui


class DrawTimeMission:
    counter = Counter()
    logger = logging.getLogger('DrawTimeMission')

    def __init__(self, func, sec, call_time):
        self.mid = self.counter.get()
        self.func = func
        self.sec = sec
        self.call_time = call_time
        self.next_call = time.perf_counter() + sec

    def update(self, current):
        if current >= self.next_call:
            try:
                self.func()
            except Exception as e:
                self.logger.error(f'error in DrawTimeMission-{self.mid}:', exc_info=e)
                return True
            self.call_time -= 1
            if self.call_time == 0: return True
            self.next_call += self.sec
        return False


class DrawTimeMgr:
    def __init__(self):
        self.last_frame = 0
        self.this_frame = time.perf_counter()
        self.fps = 0
        self.missions = {}

    def update(self):
        self.last_frame = self.this_frame
        self.this_frame = time.perf_counter()
        self.fps = int(1 // (self.this_frame - self.last_frame))
        for k, mission in tuple(self.missions.items()):
            if mission.update(self.this_frame):
                self.missions.pop(k, None)

    def add_mission(self, func, sec, call_time=1):
        m = DrawTimeMission(func, sec, call_time)
        self.missions[m.mid] = m
        return m

    def remove_mission(self, k: int | DrawTimeMission):
        if isinstance(k, DrawTimeMission): k = k.mid
        return self.missions.pop(k, None)


class Drawing:
    logger = logging.getLogger('Gui/Drawing')
    panel: m_panel.FFDPanel = None

    def __init__(self, main: "FFDraw"):
        self.main = main
        self.program = None
        self.models: models.Models | None = None

        self.work_thread = None
        self._view = None

        self.timer = DrawTimeMgr()
        self.cfg = self.main.config.setdefault('gui', {})
        self.always_draw = self.cfg.setdefault('always_draw', False)
        self.font_path = self.cfg.setdefault('font_path', r'res\PingFang.ttf')
        self.font_size = self.cfg.setdefault('font_size', default_style.stlye_font_size)
        self._label_counter = 0
        self._game_image = {}  # game_image.GameImage(self)
        self.draw_update_call = set()
        self._frame_cache = {}

        self.game_hwnd = main.mem.hwnd
        self.window_manager = game_window_manager.FFDWindowManager(self, self.font_size, None, self.font_path)

    @property
    def frame_cache(self):
        return self._frame_cache.setdefault(self.window_manager.current_window.guid, {})

    @property
    def game_image(self) -> game_image.GameImage:
        assert (current_window := self.window_manager.current_window), 'current_window is None'
        key = current_window.guid
        if key not in self._game_image:
            self._game_image[key] = game_image.GameImage(self)
        return self._game_image[key]

    def _init_everything_in_work_process(self):
        if not glfw.init():
            raise Exception("glfw can not be initialized")
        self.work_thread = threading.get_ident()
        self.logger.debug('imgui is enabled')
        panel_window = self.window_manager._new_window('FFDraw', None)
        self.panel = m_panel.FFDPanel(self)
        panel_window.draw_func = self.panel.draw
        panel_window.before_window_draw = self.panel.push_style
        panel_window.after_window_draw = self.panel.pop_style
        panel_window.on_want_close = self.panel.on_want_close
        self.window_manager.draw_window = game_window_manager.DrawWindow(self.window_manager, self.game_hwnd)
        self.program = common_shader.get_common_shader()
        self.models = models.Models()

    def _update(self):
        self._frame_cache.clear()
        self._label_counter = 0
        self._view = view.View()
        self._view.projection_view, self._view.screen_size = self.main.mem.load_screen()
        self.timer.update()
        for k, i in tuple(self._game_image.items()):
            if not isinstance(k, int) and k not in self.window_manager.windows:
                del self._game_image[k]
        return self.window_manager.update()

    def update(self):
        try:
            return self._update()
        except Exception as e:
            self.logger.critical('error in frame rendering', exc_info=e)
            self.window_manager.terminate()
            return False

    def start(self):
        try:
            self._init_everything_in_work_process()
            while self.update():
                pass
            glfw.terminate()
        except Exception as e:
            self.logger.error('error in main thread', exc_info=e)
        finally:
            os._exit(0)

    def get_view(self) -> view.View:
        if threading.get_ident() != self.work_thread:
            raise Exception("must be called in gui work thread")
        return self._view

    def add_3d_shape(self, shape: int, transform: glm.mat4, surface_color: glm.vec4 = None, line_color: glm.vec4 = None,
                     line_width: float = 3.0, point_color: glm.vec4 = None, point_size: float = 5.0):
        shape_type = shape >> 16
        shape_value = shape & 0xFFFF
        match shape_type:
            case 1:  # circle/donut
                if shape_value == 0:
                    _shape = self.models.circle
                else:
                    _shape = self.models.get_donut(shape_value)
            case 2:  # plane
                if shape_value:
                    _shape = self.models.plane_xz_with_back
                else:
                    _shape = self.models.plane_xz
            case 5:  # sector
                _shape = self.models.get_sector(shape_value)
            case 6:  # triangle
                _shape = self.models.triangle
            case 8:  # line
                _shape = self.models.line
            case 9:  # point
                _shape = self.models.point
            case 0x101:
                _shape = self.models.arrow
            case s:
                raise Exception(f"unknown shape {shape:#X} - {s}")
        _shape.render(
            program=self.program,
            mvp=self.get_view().projection_view,
            transform=transform,
            surface=surface_color,
            edge=line_color,
            line_width=line_width,
            point=point_color,
            point_size=point_size
        )

    def render_text(self, string, text_pos: glm.vec2, scale=1, color=(1, 1, 1), at=text.TextPosition.left_bottom):
        width, height = imgui.calc_text_size(string)
        text_size = glm.vec2(width + 18, height + 16)
        imgui.set_next_window_position(*text.adjust(at, text_pos, text_size))
        imgui.set_next_window_size(*text_size)
        imgui.set_next_window_bg_alpha(.4)
        imgui.push_style_color(imgui.COLOR_BORDER, *color)
        imgui.begin(
            f"_label_{self._label_counter:#x}",
            flags=imgui.WINDOW_NO_TITLE_BAR |
                  imgui.WINDOW_NO_RESIZE |
                  imgui.WINDOW_NO_MOVE |
                  imgui.WINDOW_NO_INPUTS |
                  imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS
        )
        self._label_counter += 1
        imgui.text_colored(string, *color)
        imgui.end()
        imgui.pop_style_color()
