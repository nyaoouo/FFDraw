import imgui


def format_rgba(r, g, b, alpha=255):
    """6进制颜色格式颜色转换为RGBA格式"""
    r = r / 255
    g = g / 255
    b = b / 255
    alpha = alpha / 255
    rgb = (r, g, b, alpha)
    return rgb


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
    # 10
    imgui.push_style_var(imgui.STYLE_BUTTON_TEXT_ALIGN, (10, 10))
    imgui.push_style_var(imgui.STYLE_INDENT_SPACING, 22)

    imgui.push_style_color(imgui.COLOR_TEXT, *format_rgba(255, 255, 255, 255))
    imgui.push_style_color(imgui.COLOR_TEXT_DISABLED, *format_rgba(128, 128, 128, 255))
    imgui.push_style_color(imgui.COLOR_POPUP_BACKGROUND, *format_rgba(20, 20, 20, 240))
    imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, *format_rgba(15, 15, 15, 255))
    imgui.push_style_color(imgui.COLOR_CHILD_BACKGROUND, *format_rgba(0, 0, 0, 0))
    imgui.push_style_color(imgui.COLOR_POPUP_BACKGROUND, *format_rgba(20, 20, 20, 240))
    imgui.push_style_color(imgui.COLOR_BORDER_SHADOW, *format_rgba(0, 0, 0, 0))
    imgui.push_style_color(imgui.COLOR_BORDER, *format_rgba(110, 110, 128, 128))
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, *format_rgba(47, 47, 47, 255))
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_ACTIVE, *format_rgba(114, 114, 114, 255))
    # 10
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_HOVERED, *format_rgba(64, 64, 64, 255))
    imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND, *format_rgba(6, 6, 6, 255))
    imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE, *format_rgba(161, 47, 114, 255))
    imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_COLLAPSED, *format_rgba(161, 47, 114, 255))
    imgui.push_style_color(imgui.COLOR_MENUBAR_BACKGROUND, *format_rgba(36, 36, 36, 255))
    imgui.push_style_color(imgui.COLOR_SCROLLBAR_BACKGROUND, *format_rgba(0, 0, 0, 0))
    imgui.push_style_color(imgui.COLOR_SCROLLBAR_GRAB, *format_rgba(79, 79, 79, 255))
    imgui.push_style_color(imgui.COLOR_SCROLLBAR_GRAB_HOVERED, *format_rgba(105, 105, 105, 255))
    imgui.push_style_color(imgui.COLOR_SCROLLBAR_GRAB_ACTIVE, *format_rgba(130, 130, 130, 255))
    imgui.push_style_color(imgui.COLOR_CHECK_MARK, *format_rgba(161, 47, 114, 255))
    # 20
    imgui.push_style_color(imgui.COLOR_SLIDER_GRAB, *format_rgba(138, 138, 138, 255))
    imgui.push_style_color(imgui.COLOR_SLIDER_GRAB_ACTIVE, *format_rgba(171, 171, 171, 255))
    imgui.push_style_color(imgui.COLOR_BUTTON, *format_rgba(81, 81, 81, 255))
    imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, *format_rgba(161, 47, 114, 255))
    imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, *format_rgba(160, 42, 111, 255))
    imgui.push_style_color(imgui.COLOR_RESIZE_GRIP, *format_rgba(161, 47, 114, 255))
    imgui.push_style_color(imgui.COLOR_RESIZE_GRIP_ACTIVE, *format_rgba(161, 47, 114, 255))
    imgui.push_style_color(imgui.COLOR_RESIZE_GRIP_HOVERED, *format_rgba(161, 47, 114, 255))
    imgui.push_style_color(imgui.COLOR_HEADER, *format_rgba(160, 42, 111, 255))
    imgui.push_style_color(imgui.COLOR_HEADER_HOVERED, *format_rgba(179, 32, 118, 255))
    # 30
    imgui.push_style_color(imgui.COLOR_HEADER_ACTIVE, *format_rgba(189, 34, 125, 255))


def pop_default_style():
    imgui.pop_style_var(12)

    imgui.pop_style_color(31)
