import logging
import queue
import threading
import time
import typing
import os

from nylib.utils import Counter

os.environ['PYGLFW_LIBRARY'] = os.path.join(res_path := os.path.join(os.environ['ExcPath'], 'res'), 'glfw3.dll')
os.environ['PYGLFW_PREVIEW'] = 'True'
os.environ["PATH"] += os.pathsep + res_path

import glm
import glfw
import OpenGL.GL as gl
from win32gui import GetForegroundWindow

from . import window, view, text
from .utils import common_shader, models

try:
    import imgui
except ImportError:
    use_imgui = False
else:
    use_imgui = True

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
    text_mgr: text.TextManager = None
    imgui_renderer: 'ffd_imgui.OpenglPynputRenderer' = None

    def __init__(self, main: "FFDraw"):
        self.main = main
        self.program = None
        self.models: models.Models | None = None
        self.window = None
        self.err_cnt = 0
        self.work_thread = None
        self._view = None
        self.work_queue = queue.Queue()
        self.interfaces = set()
        self.always_draw = False
        self.hwnd = main.mem.hwnd
        self.timer = DrawTimeMgr()
        self.font_path = self.main.config.setdefault('gui', {}).setdefault('font_path', './res/kaiu.ttf')

    def _init_everything_in_work_process(self):
        self.work_thread = threading.get_ident()
        self.window = window.init_window(self.hwnd)
        self.program = common_shader.get_common_shader()
        self.models = models.Models()
        self.text_mgr = text.TextManager(self.font_path)
        if use_imgui:
            self.logger.debug('imgui is enabled')
            imgui.create_context()
            from . import ffd_imgui
            self.imgui_renderer = ffd_imgui.OpenglPynputRenderer(self.window)

    def _process_single_frame(self):
        glfw.poll_events()
        self._view = view.View()
        self._view.projection_view, self._view.screen_size = self.main.mem.load_screen()
        self.text_mgr.set_projection(glm.ortho(0, *self._view.screen_size, 0))
        process_draw = self.always_draw or GetForegroundWindow() == self.hwnd
        if use_imgui:
            self.imgui_renderer.process_inputs(process_draw)
            imgui.new_frame()

        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glClear(gl.GL_DEPTH_BUFFER_BIT)

        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_BLEND)
        # gl.glEnable(gl.GL_DEPTH_TEST)
        self.timer.update()

        while not self.work_queue.empty():
            try:
                f, a = self.work_queue.get(block=False)
            except queue.Empty:
                break
            try:
                f(*a)
            except Exception as e:
                self.logger.error(f"work queue error:", exc_info=e)
        if process_draw:
            window.set_window_cover(self.window, self.hwnd)
            for draw_func in self.interfaces.copy():
                try:
                    draw_func(self.main)
                except Exception as e:
                    self.logger.error(f"draw_func error, func will be remove:", exc_info=e)
                    self.interfaces.remove(draw_func)
                    raise
        else:
            gl.glClearColor(0, 0, 0, 0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        if use_imgui:
            imgui.render()
            self.imgui_renderer.render(imgui.get_draw_data())
        glfw.swap_buffers(self.window)

    def process_single_frame(self):
        try:
            self._process_single_frame()
        except Exception as e:
            self.logger.error(f"process_single_frame error {self.err_cnt}:\t", exc_info=e)
            self.err_cnt += 1
            if self.err_cnt > 10:
                glfw.set_window_should_close(self.window, True)
        else:
            self.err_cnt = 0

    def start(self):
        try:
            self._init_everything_in_work_process()
            glfw.swap_interval(1)
            while not glfw.window_should_close(self.window):
                self.process_single_frame()
            self.work_thread = None
            if use_imgui:
                self.imgui_renderer.shutdown()
            glfw.terminate()
        except Exception as e:
            self.logger.error('error in main thread', exc_info=e)

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
