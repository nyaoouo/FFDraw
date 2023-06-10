import glfw
from win32gui import ClientToScreen, GetClientRect
import OpenGL.GL as gl


def set_window_cover(window, hwnd):
    x1, y1, x2, y2 = GetClientRect(hwnd)
    glfw.set_window_pos(window, *ClientToScreen(hwnd, (x1, y1)))
    x_size = abs(x2 - x1)
    y_size = abs(y2 - y1)
    glfw.set_window_size(window, x_size, y_size)
    gl.glViewport(0, 0, x_size, y_size)


def init_window(title: str, past_through=False, parent=None, game_hwnd=None):
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE)
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
    glfw.window_hint(glfw.DECORATED, glfw.FALSE)
    if past_through:
        glfw.window_hint(glfw.FLOATING, glfw.TRUE)
        glfw.window_hint(glfw.MOUSE_PASSTHROUGH, glfw.TRUE)

    window = glfw.create_window(1024, 980, title, None, parent)
    if past_through:
        glfw.window_hint(glfw.FLOATING, glfw.FALSE)
        glfw.window_hint(glfw.MOUSE_PASSTHROUGH, glfw.FALSE)
    glfw.make_context_current(window)
    if not window:
        glfw.terminate()
        raise Exception("glfw can not create window")
    if game_hwnd:
        set_window_cover(window, game_hwnd)
    return window
