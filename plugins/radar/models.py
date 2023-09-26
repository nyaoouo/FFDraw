import math
from ctypes import *
import glm
import OpenGL.GL as gl

circle_steps = 32
circle_vertices = []
for i in range(circle_steps):
    angle = 2 * math.pi * i / circle_steps
    circle_vertices.extend([math.cos(angle), 0, math.sin(angle)])

c_xy = .5 ** .5


def create_buffers(**vertices: list[float]):
    vertices_flat = list(vertices.items())
    buffer = (c_float * sum(len(v) for k, v in vertices_flat))()
    ranges = {}
    start_range = 0
    for key, vert in vertices_flat:
        for i in range(len(vert)):
            buffer[start_range + i] = vert[i]
        ranges[key] = (start_range // 3, len(vert) // 3)
        start_range += len(vert)

    vao = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(vao)
    vbo = gl.glGenBuffers(1)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(buffer), buffer, gl.GL_STATIC_DRAW)
    gl.glEnableVertexAttribArray(0)
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
    gl.glBindVertexArray(0)

    return vao, vbo, ranges


class HitBox:
    def __init__(self):
        self.vao, self.vbo, self.ranges = create_buffers(
            center=[
                0, 0, 0,
            ],
            ring=circle_vertices,
            cross=[
                c_xy, 0, c_xy,
                -c_xy, 0, -c_xy,
                -c_xy, 0, c_xy,
                c_xy, 0, -c_xy,
            ],
            arrow_from=[
                0, 0, .5,
                -.5, 0, 0,
                -.5, 0, .5,
                0, 0, 1,
                .5, 0, .5,
                .5, 0, 0,
            ],
            arrow_to=[
                0, 0, -.5,
                -.5, 0, -1,
                -.5, 0, -.5,
                0, 0, 0,
                .5, 0, -.5,
                .5, 0, -1,
            ]

        )

    def render(
            self,
            program,
            transform: glm.mat4,
            mvp: glm.mat4,
            surface: glm.vec4 = None,
            edge: glm.vec4 = None, line_width: float = 3.0,
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
            gl.glDrawArrays(gl.GL_TRIANGLE_FAN, *self.ranges["arrow_from"])

        if edge is not None:
            gl.glUniform4fv(color_location, 1, glm.value_ptr(edge))
            gl.glLineWidth(line_width)
            gl.glDrawArrays(gl.GL_LINES, *self.ranges["cross"])
            gl.glDrawArrays(gl.GL_LINE_LOOP, *self.ranges["arrow_from"])
            gl.glDrawArrays(gl.GL_LINE_LOOP, *self.ranges["ring"])

        gl.glBindVertexArray(0)
        gl.glUseProgram(0)
        gl.glPopMatrix()


class TargetLine:
    def __init__(self):
        self.vao, self.vbo, self.ranges = create_buffers(
            line=[
                0, 0, 0,
                0, 0, .7,
            ],
            head=[
                0, 0, 1,
                .2, 0, .7,
                -.2, 0, .7,
            ],
        )

    def render(
            self,
            program,
            transform: glm.mat4,
            mvp: glm.mat4,
            surface: glm.vec4 = None,
            edge: glm.vec4 = None, line_width: float = 3.0,
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
            gl.glDrawArrays(gl.GL_TRIANGLES, *self.ranges["head"])

        if edge is not None:
            gl.glUniform4fv(color_location, 1, glm.value_ptr(edge))
            gl.glLineWidth(line_width)
            gl.glDrawArrays(gl.GL_LINES, *self.ranges["line"])
            gl.glDrawArrays(gl.GL_LINE_LOOP, *self.ranges["head"])

        gl.glBindVertexArray(0)
        gl.glUseProgram(0)
        gl.glPopMatrix()
