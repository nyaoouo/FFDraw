import glfw
from win32gui import GetWindowRect
import OpenGL.GL as gl


def set_window_cover(window, hwnd):
    try:
        x1, y1, x2, y2 = GetWindowRect(hwnd)
    except Exception:
        raise SystemExit()
    glfw.set_window_pos(window, x1, y1)
    x_size = abs(x2 - x1)
    y_size = abs(y2 - y1)
    glfw.set_window_size(window, x_size, y_size)
    gl.glViewport(0, 0, x_size, y_size)


def init_window(hwnd):
    if not glfw.init():
        raise Exception("glfw can not be initialized")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE)
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
    glfw.window_hint(glfw.FLOATING, glfw.TRUE)
    glfw.window_hint(glfw.DECORATED, glfw.FALSE)
    glfw.window_hint(glfw.MOUSE_PASSTHROUGH, glfw.TRUE)

    window = glfw.create_window(1024, 980, "ff_draw", None, None)
    glfw.make_context_current(window)
    if not window:
        glfw.terminate()
        raise Exception("glfw can not create window")
    set_window_cover(window, hwnd)
    return window
