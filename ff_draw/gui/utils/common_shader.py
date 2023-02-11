from .util import loadShaders

strVS = """
#version 330 core
layout (location = 0) in vec3 aPos;


out vec4 outColor;
uniform mat4 transform;
uniform mat4 mvp;
uniform vec4 inColor;

void main()
{
    gl_Position = mvp * transform * vec4(aPos, 1.0);
    outColor = inColor;
}
"""

strFS = """
#version 330 core

out vec4 outColor;
uniform vec4 inColor;

void main(){
    outColor = inColor;
}
"""


def get_common_shader():
    return loadShaders(strVS, strFS)
