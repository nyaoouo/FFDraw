import imgui


def format_rgba(r, g, b, alpha=255):
    """6进制颜色格式颜色转换为RGBA格式"""
    r = r / 255
    g = g / 255
    b = b / 255
    alpha = alpha / 255
    rgb = (r, g, b, alpha)
    return rgb


color_main = format_rgba(121, 39, 87)
color_main_up = format_rgba(161, 47, 114)
color_main_up_up = format_rgba(188, 43, 128)
color_minor = format_rgba(84, 26, 60)
color_minor_up = format_rgba(101, 32, 73)
color_control = format_rgba(81, 81, 81)
color_control_up = format_rgba(114, 114, 114)
color_input = format_rgba(47, 47, 47)
color_input_up = format_rgba(64, 64, 64)


def set_default_style():
    io = imgui.get_io()
    io.font_global_scale = 1.3

    imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 5)
    imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0)
    imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (10, 10))
    imgui.push_style_var(imgui.STYLE_POPUP_ROUNDING, 5)
    imgui.push_style_var(imgui.STYLE_POPUP_BORDERSIZE, 0)
    imgui.push_style_var(imgui.STYLE_FRAME_ROUNDING, 5)
    imgui.push_style_var(imgui.STYLE_FRAME_PADDING, (5, 5))
    imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (10, 6))
    imgui.push_style_var(imgui.STYLE_ITEM_INNER_SPACING, (5, 6))
    imgui.push_style_var(imgui.STYLE_SCROLLBAR_SIZE, 20)
    imgui.push_style_var(imgui.STYLE_INDENT_SPACING, 22)

    imgui.push_style_color(imgui.COLOR_TEXT, *format_rgba(255, 255, 255, 255))
    imgui.push_style_color(imgui.COLOR_TEXT_DISABLED, *format_rgba(128, 128, 128, 255))
    imgui.push_style_color(imgui.COLOR_POPUP_BACKGROUND, *format_rgba(20, 20, 20, 240))
    imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, *format_rgba(15, 15, 15, 255))
    imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, *format_rgba(0, 0, 0, 0))
    imgui.push_style_color(imgui.COLOR_BORDER_SHADOW, *format_rgba(0, 0, 0, 0))
    imgui.push_style_color(imgui.COLOR_BORDER, *format_rgba(110, 110, 128, 255))
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, *color_input)
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_ACTIVE, *color_control_up)
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_HOVERED, *color_input_up)
    imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND, *format_rgba(6, 6, 6, 255))
    imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE, *color_main_up)
    imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_COLLAPSED, *color_minor_up)
    imgui.push_style_color(imgui.COLOR_MENUBAR_BACKGROUND, *format_rgba(36, 36, 36, 255))
    imgui.push_style_color(imgui.COLOR_SCROLLBAR_BACKGROUND, *format_rgba(0, 0, 0, 0))
    imgui.push_style_color(imgui.COLOR_SCROLLBAR_GRAB, *color_input_up)
    imgui.push_style_color(imgui.COLOR_SCROLLBAR_GRAB_HOVERED, *color_control)
    imgui.push_style_color(imgui.COLOR_SCROLLBAR_GRAB_ACTIVE, *color_control_up)
    imgui.push_style_color(imgui.COLOR_CHECK_MARK, *color_main_up_up)
    imgui.push_style_color(imgui.COLOR_SLIDER_GRAB, *color_main)
    imgui.push_style_color(imgui.COLOR_SLIDER_GRAB_ACTIVE, *color_main_up)
    imgui.push_style_color(imgui.COLOR_BUTTON, *color_control)
    imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, *color_main_up)
    imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, *color_main)
    imgui.push_style_color(imgui.COLOR_RESIZE_GRIP, *color_minor)
    imgui.push_style_color(imgui.COLOR_RESIZE_GRIP_ACTIVE, *color_main)
    imgui.push_style_color(imgui.COLOR_RESIZE_GRIP_HOVERED, *color_minor_up)
    imgui.push_style_color(imgui.COLOR_HEADER, *color_main)
    imgui.push_style_color(imgui.COLOR_HEADER_HOVERED, *color_main_up)
    imgui.push_style_color(imgui.COLOR_HEADER_ACTIVE, *color_main_up_up)
    imgui.push_style_color(imgui.COLOR_SEPARATOR, *color_control)
    imgui.push_style_color(imgui.COLOR_SEPARATOR_HOVERED, *color_main)
    imgui.push_style_color(imgui.COLOR_SEPARATOR_ACTIVE, *color_main_up)
    imgui.push_style_color(imgui.COLOR_TAB, *color_input_up)
    imgui.push_style_color(imgui.COLOR_TAB_ACTIVE, *color_main_up)
    imgui.push_style_color(imgui.COLOR_TAB_HOVERED, *color_main)


def pop_default_style():
    imgui.pop_style_var(11)

    imgui.pop_style_color(36)
