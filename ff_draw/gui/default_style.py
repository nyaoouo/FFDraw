import imgui
import win32api, win32con


def rgba_to_float(r, g, b, alpha=255):
    r = r / 255
    g = g / 255
    b = b / 255
    alpha = alpha / 255
    r = r if r >= 0 else 0
    g = g if g >= 0 else 0
    b = b if b >= 0 else 0
    alpha = alpha if alpha >= 0 else 0
    r = r if r <= 1 else 1
    g = g if g <= 1 else 1
    b = b if b <= 1 else 1
    alpha = alpha if alpha <= 1 else 1
    rgb = (r, g, b, alpha)
    return rgb


def float_to_rgba(r, g, b, alpha=1):
    r = r * 255
    g = g * 255
    b = b * 255
    alpha = alpha * 255
    r = r if r >= 0 else 0
    g = g if g >= 0 else 0
    b = b if b >= 0 else 0
    alpha = alpha if alpha >= 0 else 0
    r = r if r <= 255 else 255
    g = g if g <= 255 else 255
    b = b if b <= 255 else 255
    alpha = alpha if alpha <= 255 else 255
    rgb = (r, g, b, alpha)
    return rgb


# 字号分辨率自适配
stlye_font_size: int
screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # windows缩放后的分辨率，非实际屏幕分辨率
screen_heigh = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
if screen_width <= (1920 + 2560) / 2:
    stlye_font_size = 22
elif (1920 + 2560) / 2 < screen_width <= (2560 + 3840) / 2:
    stlye_font_size = 24
else:
    stlye_font_size = 26

# 设置默认颜色
style_color_default = {}
style_color_default['color_main'] = rgba_to_float(121, 39, 87)
style_color_default['color_main_up'] = rgba_to_float(161, 47, 114)
style_color_default['color_main_up_up'] = rgba_to_float(188, 43, 128)
style_color_default['color_minor'] = rgba_to_float(84, 26, 60)
style_color_default['color_minor_up'] = rgba_to_float(101, 32, 73)
style_color_default['color_control'] = rgba_to_float(81, 81, 81)
style_color_default['color_control_up'] = rgba_to_float(114, 114, 114)
style_color_default['color_input'] = rgba_to_float(47, 47, 47)
style_color_default['color_input_up'] = rgba_to_float(64, 64, 64)
style_color_default['color_background'] = rgba_to_float(15, 15, 15)
style_color_default['color_background2'] = rgba_to_float(26, 26, 26)
style_color_default['alpha'] = 1
style_color_default['alpha_background'] = 1


def set_default_color(style_color):
    for name, value in style_color_default.items():
        style_color.setdefault(name, value)
    return style_color


def set_color(style_color: dict, mainColor: tuple, darkColor: tuple):
    """输入亮色调和暗色调，改变style_color整体的值"""
    style_color['color_main_up'] = mainColor
    style_color['color_background'] = darkColor

    def change(name: str, r=0, g=0, b=0, a=0):
        base_color: tuple
        if name in ['color_main', 'color_main_up_up', 'color_minor', 'color_minor_up']:
            base_color = float_to_rgba(*mainColor)
        else:
            base_color = float_to_rgba(*darkColor)
        temp_color = (base_color[0] + r, base_color[1] + g, base_color[2] + b, base_color[3] + a)
        style_color[name] = rgba_to_float(*temp_color)

    change('color_main', -40, -8, -27)
    change('color_main_up_up', 16, 4, 14)
    change('color_minor', -77, -21, -54)
    change('color_minor_up', -60, -15, -41)

    change('color_control', 66, 66, 66)
    change('color_control_up', 99, 99, 99)
    change('color_input', 32, 32, 32)
    change('color_input_up', 49, 49, 49)
    change('color_background2', 11, 11, 11)


def set_style(style_color):
    imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 5)
    imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0)
    imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (10, 10))
    imgui.push_style_var(imgui.STYLE_POPUP_ROUNDING, 5)
    imgui.push_style_var(imgui.STYLE_POPUP_BORDERSIZE, 0)
    imgui.push_style_var(imgui.STYLE_FRAME_ROUNDING, 5)
    imgui.push_style_var(imgui.STYLE_FRAME_PADDING, (5, 5))
    imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (12, 12))
    imgui.push_style_var(imgui.STYLE_ITEM_INNER_SPACING, (8, 6))
    imgui.push_style_var(imgui.STYLE_SCROLLBAR_SIZE, 20)
    imgui.push_style_var(imgui.STYLE_INDENT_SPACING, 22)
    imgui.push_style_var(imgui.STYLE_GRAB_ROUNDING, 5)
    imgui.push_style_var(imgui.STYLE_GRAB_MIN_SIZE, 10)

    imgui.push_style_color(imgui.COLOR_TEXT, *rgba_to_float(255, 255, 255, 255))
    imgui.push_style_color(imgui.COLOR_TEXT_DISABLED, *rgba_to_float(128, 128, 128, 255))
    imgui.push_style_color(imgui.COLOR_POPUP_BACKGROUND, *style_color['color_background2'])
    imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, *style_color['color_background'][:3],
                           style_color['alpha_background'])
    imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, *rgba_to_float(0, 0, 0, 0))
    imgui.push_style_color(imgui.COLOR_BORDER_SHADOW, *rgba_to_float(0, 0, 0, 0))
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, *style_color['color_input'])
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_ACTIVE, *style_color['color_control_up'])
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_HOVERED, *style_color['color_input_up'])
    imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND, *style_color['color_background2'])
    imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE, *style_color['color_main_up'])
    imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_COLLAPSED, *style_color['color_minor_up'])
    imgui.push_style_color(imgui.COLOR_MENUBAR_BACKGROUND, *rgba_to_float(36, 36, 36, 255))
    imgui.push_style_color(imgui.COLOR_SCROLLBAR_BACKGROUND, *rgba_to_float(0, 0, 0, 0))
    imgui.push_style_color(imgui.COLOR_SCROLLBAR_GRAB, *style_color['color_input_up'])
    imgui.push_style_color(imgui.COLOR_SCROLLBAR_GRAB_HOVERED, *style_color['color_control'])
    imgui.push_style_color(imgui.COLOR_SCROLLBAR_GRAB_ACTIVE, *style_color['color_control_up'])
    imgui.push_style_color(imgui.COLOR_CHECK_MARK, *style_color['color_main_up_up'])
    imgui.push_style_color(imgui.COLOR_SLIDER_GRAB, *style_color['color_main'])
    imgui.push_style_color(imgui.COLOR_SLIDER_GRAB_ACTIVE, *style_color['color_main_up'])
    imgui.push_style_color(imgui.COLOR_BUTTON, *style_color['color_control'])
    imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, *style_color['color_main_up'])
    imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, *style_color['color_main'])
    imgui.push_style_color(imgui.COLOR_RESIZE_GRIP, *style_color['color_minor'])
    imgui.push_style_color(imgui.COLOR_RESIZE_GRIP_ACTIVE, *style_color['color_main'])
    imgui.push_style_color(imgui.COLOR_RESIZE_GRIP_HOVERED, *style_color['color_minor_up'])
    imgui.push_style_color(imgui.COLOR_HEADER, *style_color['color_main'])
    imgui.push_style_color(imgui.COLOR_HEADER_HOVERED, *style_color['color_main_up'])
    imgui.push_style_color(imgui.COLOR_HEADER_ACTIVE, *style_color['color_main_up_up'])
    imgui.push_style_color(imgui.COLOR_SEPARATOR, *style_color['color_control'])
    imgui.push_style_color(imgui.COLOR_SEPARATOR_HOVERED, *style_color['color_main'])
    imgui.push_style_color(imgui.COLOR_SEPARATOR_ACTIVE, *style_color['color_main_up'])
    imgui.push_style_color(imgui.COLOR_TAB, *style_color['color_input_up'])
    imgui.push_style_color(imgui.COLOR_TAB_ACTIVE, *style_color['color_main'])
    imgui.push_style_color(imgui.COLOR_TAB_HOVERED, *style_color['color_main_up'])
    imgui.push_style_color(imgui.COLOR_SLIDER_GRAB, *style_color['color_main_up'])
    imgui.push_style_color(imgui.COLOR_SLIDER_GRAB_ACTIVE, *style_color['color_main_up_up'])


def pop_style():
    imgui.pop_style_var(13)

    imgui.pop_style_color(37)


def text_tip(text):
    """用于提示或补充类文字"""
    imgui.push_style_color(imgui.COLOR_TEXT, *rgba_to_float(114, 114, 114))
    imgui.text(text)
    imgui.pop_style_color()
