import OpenGL.GL as gl
from OpenGL.GL import shaders


def loadShaders(strVS, strFS):
    """load vertex and fragment shaders from strings"""
    # compile vertex shader
    shaderV = shaders.compileShader([strVS], gl.GL_VERTEX_SHADER)
    # compiler fragment shader
    shaderF = shaders.compileShader([strFS], gl.GL_FRAGMENT_SHADER)

    # create the program object
    program = gl.glCreateProgram()
    if not program:
        raise RuntimeError('glCreateProgram faled!')

    # attach shaders
    gl.glAttachShader(program, shaderV)
    gl.glAttachShader(program, shaderF)

    # Link the program
    gl.glLinkProgram(program)

    # Check the link status
    linked = gl.glGetProgramiv(program, gl.GL_LINK_STATUS)
    if not linked:
        infoLen = gl.glGetProgramiv(program, gl.GL_INFO_LOG_LENGTH)
        infoLog = ""
        if infoLen > 1:
            infoLog = gl.glGetProgramInfoLog(program, infoLen, None)
        gl.glDeleteProgram(program)
        raise RuntimeError("Error linking program:\n%s\n", infoLog)

    return program
