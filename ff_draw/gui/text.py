import logging
import struct

import glm
from OpenGL.GL import *
from OpenGL.GL import shaders

try:
    import freetype
except ImportError:
    use_text = False
else:
    use_text = True

font_buffer_struct = struct.Struct('16f')
font_buffer_size = font_buffer_struct.size

VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec4 vertex; // <vec2 pos, vec2 tex>
out vec2 TexCoords;

uniform mat4 projection;

void main()
{
    gl_Position = projection * vec4(vertex.xy, 0.0, 1.0);
    TexCoords = vertex.zw;
}
"""

FRAGMENT_SHADER = """
#version 330 core
in vec2 TexCoords;
out vec4 color;

uniform sampler2D text;
uniform vec3 textColor;

void main()
{    
    color = vec4(textColor, 1.0) * vec4(1.0, 1.0, 1.0, texture(text, TexCoords).r);
}
"""


class TextPosition:
    left_top = 0
    left_bottom = 1
    center_top = 2
    center_bottom = 3
    right_top = 4
    right_bottom = 5


def adjust(key, pos: glm.vec2, text_size: glm.vec2):
    if key < 3:
        if key == 0:  # left_top
            return glm.vec2(pos.x, pos.y + text_size.y)
        elif key == 1:  # left_bottom
            return glm.vec2(*pos)
        else:  # center_top
            return glm.vec2(pos.x - text_size.x / 2, pos.y + text_size.y)
    elif key > 3:
        if key == 4:  # right_top
            return glm.vec2(pos.x - text_size.x, pos.y + text_size.y)
        else:  # right_bottom
            return glm.vec2(pos.x - text_size.x, pos.y)
    else:  # center_bottom
        return glm.vec2(pos.x - text_size.x / 2, pos.y)


class TextManager:
    logger = logging.getLogger('TextManager')

    def __init__(self, font_path):
        if not use_text: return
        self.characters = {}
        self.face = freetype.Face(font_path)
        self.face.set_char_size(2048)

        # compiling shaders
        vertexshader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
        fragmentshader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        # creating shaderProgram
        self.program = shaders.compileProgram(vertexshader, fragmentshader)
        glUseProgram(self.program)
        glUseProgram(0)

        # disable byte-alignment restriction
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, 0)

        # configure VAO/VBO for texture quads
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, font_buffer_size, None, GL_DYNAMIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def _make_character(self, c):
        if not use_text: return
        self.face.load_char(c)
        glyph = self.face.glyph

        # generate texture
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, glyph.bitmap.width, glyph.bitmap.rows, 0, GL_RED, GL_UNSIGNED_BYTE, glyph.bitmap.buffer)
        # texture options
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)

        # now store character for later use
        self.characters[c] = res = texture, glm.vec2(glyph.bitmap.width, -glyph.bitmap.rows)
        return res

    def prepare_string(self, s):
        if not use_text: return
        for c in s:
            if c not in self.characters:
                yield self._make_character(c)
            else:
                yield self.characters[c]

    def string_size(self, s):
        if not use_text: return
        y = x = 0
        for _, (_x, _y) in self.prepare_string(s):
            x += _x
            y = min(_y, y)
        return glm.vec2(x, -y)

    def set_projection(self, projection: glm.mat4):
        if not use_text: return
        glUseProgram(self.program)
        glUniformMatrix4fv(glGetUniformLocation(self.program, "projection"), 1, GL_FALSE, glm.value_ptr(projection))
        glUseProgram(0)

    def render_text(self, text, text_pos: glm.vec2, scale=1, color=(1, 1, 1), at=TextPosition.left_bottom):
        if not use_text: return
        glUseProgram(self.program)
        glUniform3f(glGetUniformLocation(self.program, "textColor"), *color)

        glActiveTexture(GL_TEXTURE0)
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        text_pos = text_pos.__copy__() if at == 1 else adjust(at, text_pos, self.string_size(text))
        for texture, texture_size in self.prepare_string(text):
            glBindTexture(GL_TEXTURE_2D, texture)
            text_pos2 = text_pos + texture_size * scale
            glBufferSubData(GL_ARRAY_BUFFER, 0, font_buffer_size, font_buffer_struct.pack(
                text_pos.x, text_pos2.y, 0, 0,
                text_pos.x, text_pos.y, 0, 1,
                text_pos2.x, text_pos.y, 1, 1,
                text_pos2.x, text_pos2.y, 1, 0
            ))
            glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
            text_pos.x = text_pos2.x

        glBindTexture(GL_TEXTURE_2D, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        glUseProgram(0)
