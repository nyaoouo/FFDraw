from ctypes import *

import glm
import OpenGL.GL as gl
import math


class BaseModel3d:
    _surface_vertices = []
    _surface_mode = gl.GL_TRIANGLE_FAN

    _edge_vertices = []
    _edge_mode = gl.GL_LINE_LOOP

    _point_vertices = []
    _point_mode = gl.GL_POINTS

    def __init__(self):
        t_len = len(self._point_vertices) + len(self._edge_vertices) + len(self._surface_vertices)
        self.point_range = [0, len(self._point_vertices) // 3]
        self.edge_range = [sum(self.point_range), len(self._edge_vertices) // 3]
        self.surface_range = [sum(self.edge_range), len(self._surface_vertices) // 3]

        data = (c_float * t_len)(*self._point_vertices, *self._edge_vertices, *self._surface_vertices)
        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)
        self.vbo = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(data), data, gl.GL_STATIC_DRAW)
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

        gl.glBindVertexArray(0)

    def render(
            self,
            program,
            transform: glm.mat4,
            mvp: glm.mat4,
            surface: glm.vec4 = None,
            edge: glm.vec4 = None, line_width: float = 3.0,
            point: glm.vec4 = None, point_size: float = 5.0
    ):
        gl.glPushMatrix()
        gl.glUseProgram(program)

        gl.glUniformMatrix4fv(
            gl.glGetUniformLocation(program, "transform"),
            1, gl.GL_FALSE, glm.value_ptr(transform)
        )
        gl.glUniformMatrix4fv(
            gl.glGetUniformLocation(program, "mvp"),
            1, gl.GL_FALSE, glm.value_ptr(mvp)
        )

        gl.glBindVertexArray(self.vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        color_location = gl.glGetUniformLocation(program, "inColor")

        if surface is not None:
            gl.glUniform4fv(color_location, 1, glm.value_ptr(surface))
            gl.glDrawArrays(self._surface_mode, *self.surface_range)

        if edge is not None:
            gl.glUniform4fv(color_location, 1, glm.value_ptr(edge))
            gl.glLineWidth(line_width)
            gl.glDrawArrays(self._edge_mode, *self.edge_range)

        if point is not None:
            gl.glUniform4fv(color_location, 1, glm.value_ptr(point))
            gl.glPointSize(point_size)
            gl.glDrawArrays(self._point_mode, *self.point_range)

        self.ex_render(transform, surface, edge, line_width, point, point_size, color_location)

        gl.glBindVertexArray(0)
        gl.glUseProgram(0)
        gl.glPopMatrix()

    def ex_render(self,
                  transform: glm.mat4,
                  surface: glm.vec4,
                  edge: glm.vec4, line_width: float,
                  point: glm.vec4, point_size: float, color_location):
        pass


class Line(BaseModel3d):
    _edge_vertices = [
        0, 0, 0,
        0, 0, 1
    ]
    _edge_mode = gl.GL_LINE_STRIP
    _point_vertices = _edge_vertices


class Point(BaseModel3d):
    _point_vertices = [0, 0, 0]


class PlaneXZ(BaseModel3d):
    _surface_vertices = [
        -.5, 0.0, 0,
        .5, 0.0, 0,
        .5, 0.0, 1,
        -.5, 0.0, 1
    ]
    _edge_vertices = _surface_vertices
    _point_vertices = _surface_vertices


class PlaneXZWithBack(BaseModel3d):
    _surface_vertices = [
        -.5, 0.0, -1,
        .5, 0.0, -1,
        .5, 0.0, 1,
        -.5, 0.0, 1
    ]
    _edge_vertices = _surface_vertices
    _point_vertices = _surface_vertices


circle_steps = 64
circle_vertices = []
for i in range(circle_steps):
    angle = 2 * math.pi * i / circle_steps
    circle_vertices.extend([math.cos(angle), 0, math.sin(angle)])


class Circle(BaseModel3d):
    _surface_vertices = circle_vertices
    _edge_vertices = circle_vertices
    _point_vertices = circle_vertices


class Donut(BaseModel3d):
    _inner_edge_vertices = []
    _surface_mode = gl.GL_TRIANGLE_STRIP

    def __init__(self):
        super().__init__()
        data = (c_float * len(self._inner_edge_vertices))(*self._inner_edge_vertices)
        self.inner_edge_range = [0, len(self._inner_edge_vertices) // 3]
        self.inner_vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.inner_vao)
        self.inner_vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.inner_vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(data), data, gl.GL_STATIC_DRAW)
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glBindVertexArray(0)

    def ex_render(self,
                  transform: glm.mat4,
                  surface: glm.vec4,
                  edge: glm.vec4, line_width: float,
                  point: glm.vec4, point_size: float, color_location):
        gl.glBindVertexArray(self.inner_vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.inner_vbo)
        if edge is not None:
            gl.glUniform4fv(color_location, 1, glm.value_ptr(edge))
            gl.glLineWidth(line_width)
            gl.glDrawArrays(self._edge_mode, *self.inner_edge_range)


class Arrow(BaseModel3d):
    _surface_vertices = [
        0, 0, 0,
        -1, 0, -1,
        -1, 0, 0,
        0, 0, 1,
        1, 0, 0,
        1, 0, -1,
    ]
    _edge_vertices = _surface_vertices
    _point_vertices = _surface_vertices


class Triangle(BaseModel3d):
    _surface_vertices = [
        1, 0, 0,
        -1, 0, 0,
        0, 0, 1,
    ]
    _edge_vertices = _surface_vertices
    _point_vertices = _surface_vertices


class Models:
    def __init__(self):
        self.line = Line()
        self.point = Point()
        self.arrow = Arrow()
        self.triangle = Triangle()
        self.plane_xz = PlaneXZ()
        self.plane_xz_with_back = PlaneXZWithBack()
        self.circle = Circle()
        self.donut_cache = {}
        self.sector_cache = {}

    def get_donut(self, _percent: int) -> BaseModel3d:
        if _percent not in self.donut_cache:
            percent = _percent / 0xffff
            if percent <= 0 or percent > 1:
                raise ValueError("Percent must be between 0 and 1")
            vertices = []
            for i in range(circle_steps):
                angle = 2 * math.pi * i / circle_steps
                c_angle = math.cos(angle)
                s_angle = math.sin(angle)
                vertices.extend([
                    c_angle, 0, s_angle,
                    c_angle * percent, 0, s_angle * percent
                ])

            edge_vertices = []
            inner_edge_vertices = []
            for i in range(circle_steps):
                s = i * 6
                edge_vertices.extend(vertices[s:s + 3])
                inner_edge_vertices.extend(vertices[s + 3:s + 6])

            self.donut_cache[_percent] = type(f'Donut_{_percent}', (Donut,), {
                '_surface_vertices': vertices + vertices[:6],
                '_edge_vertices': edge_vertices,
                '_inner_edge_vertices': inner_edge_vertices,
                '_point_vertices': vertices
            })()
        return self.donut_cache[_percent]

    def get_sector(self, degree: int) -> BaseModel3d:
        if degree not in self.sector_cache:
            if degree > 360 or degree < 0:
                raise ValueError("Degree must be between 0 and 360")
            arc_percent = degree / 360
            start_angle = math.pi * (.5 - arc_percent)
            arc_step = math.ceil(arc_percent * circle_steps)
            arc_rad = math.radians(degree)
            vertices = [0, 0, 0]
            for i in range(arc_step + 1):
                angle = start_angle + arc_rad * i / arc_step
                vertices.extend([math.cos(angle), 0, math.sin(angle)])
            self.sector_cache[degree] = type(f'Sector_{degree}', (BaseModel3d,), {
                '_surface_vertices': vertices,
                '_edge_vertices': vertices,
                '_point_vertices': vertices
            })()
        return self.sector_cache[degree]
