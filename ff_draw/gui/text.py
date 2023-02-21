import glm


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
            return glm.vec2(*pos)
        elif key == 1:  # left_bottom
            return glm.vec2(pos.x, pos.y - text_size.y)
        else:  # center_top
            return glm.vec2(pos.x - text_size.x / 2, pos.y)
    elif key > 3:
        if key == 4:  # right_top
            return glm.vec2(pos.x - text_size.x, pos.y)
        else:  # right_bottom
            return glm.vec2(pos.x - text_size.x, pos.y - text_size.y)
    else:  # center_bottom
        return glm.vec2(pos.x - text_size.x / 2, pos.y - text_size.y)
