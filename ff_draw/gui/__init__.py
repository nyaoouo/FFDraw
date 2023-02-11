import logging
import math
import queue
import sys
import threading
import typing
import traceback
import os

os.environ['PYGLFW_LIBRARY'] = os.path.join(os.environ['ExcPath'], 'res', 'glfw3.dll')
os.environ['PYGLFW_PREVIEW'] = 'True'

import glm
import glfw
import OpenGL.GL as gl
from win32gui import GetForegroundWindow

from . import window, view
from .utils import common_shader, models

if typing.TYPE_CHECKING:
    from ff_draw.main import FFDraw


class Drawing:
    logger = logging.getLogger('Gui/Drawing')

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

    def _init_everything_in_work_process(self):
        self.work_thread = threading.get_ident()
        self.window = window.init_window(self.hwnd)
        self.program = common_shader.get_common_shader()
        self.models = models.Models()

    def _process_single_frame(self):
        self._view = None
        glfw.poll_events()
        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glClear(gl.GL_DEPTH_BUFFER_BIT)

        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_BLEND)
        # gl.glEnable(gl.GL_DEPTH_TEST)

        while not self.work_queue.empty():
            try:
                f, a = self.work_queue.get(block=False)
            except queue.Empty:
                break
            try:
                f(*a)
            except Exception as e:
                self.logger.error(f"work queue error:", exc_info=e)
        if self.always_draw or GetForegroundWindow() == self.hwnd:
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
        self._init_everything_in_work_process()
        glfw.swap_interval(1)
        while not glfw.window_should_close(self.window):
            self.process_single_frame()
        self.work_thread = None
        glfw.terminate()

    def get_view(self) -> view.View:
        if threading.get_ident() != self.work_thread:
            raise Exception("must be called in gui work thread")
        if self._view is None:
            self._view = view.View()
            self._view.projection_view, self._view.screen_size = self.main.mem.load_screen()
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
