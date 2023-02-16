import math

import glm

pi2 = math.pi * 2
pi_2 = math.pi / 2


def is_circle_hit(scale: glm.vec3, ignore_percent: float, src: glm.vec3, dst: glm.vec3, height=math.inf):
    assert scale.x == scale.z, "not support oval"
    effect_range = scale.x
    return abs(src.y - dst.y) < height and effect_range * ignore_percent <= glm.distance(src.xz, dst.xz) <= effect_range


def is_fan_hit(scale: glm.vec3, angle_rad: float, facing_rad: float, src: glm.vec3, dst: glm.vec3, height=math.inf):
    assert scale.x == scale.z, "not support oval"
    if abs(src.y - dst.y) > height: return False
    return glm.distance(src.xz, dst.xz) <= scale.x and (glm.polar(dst - src).y - (facing_rad - angle_rad / 2)) % pi2 <= angle_rad


def is_rect_hit(scale: glm.vec3, src: glm.vec3, facing: float, dst: glm.vec3, height=math.inf, back=False):
    if abs(src.y - dst.y) > height: return False
    cos_f = math.cos(facing)
    sin_f = math.sin(facing)
    rw = glm.vec2(cos_f, -sin_f) * scale.x
    rh = glm.vec2(sin_f, cos_f) * scale.z
    dst_2 = dst.xz
    if back:
        p1 = src.xz + (rw / 2) - rh
        rh *= 2
        p2 = p1 + rh
        p3 = p2 - rw
        p4 = p3 - rh
    else:
        p1 = src.xz + (rw / 2)
        p2 = p1 + rh
        p3 = p2 - rw
        p4 = p3 - rh
    return (
            glm.dot(dst_2 - p1, p1 - p2) <= 0 and
            glm.dot(dst_2 - p2, p2 - p3) <= 0 and
            glm.dot(dst_2 - p3, p3 - p4) <= 0 and
            glm.dot(dst_2 - p4, p4 - p1) <= 0
    )


def hit_check(shape: int, scale: glm.vec3, src: glm.vec3, facing: float, dst: glm.vec3, height=math.inf):
    shape_type = shape >> 16
    shape_value = shape & 0xFFFF
    match shape_type:
        case 1:  # circle/donut
            return is_circle_hit(scale, shape_value / 0xffff, src, dst, height)
        case 2:  # rect
            return is_rect_hit(scale, src, facing, dst, height, bool(shape_value)) or (shape_value == 2 and is_rect_hit(scale, src, facing + pi_2, dst, height, True))
        case 5:  # fan
            return is_fan_hit(scale, math.radians(shape_value), facing, src, dst, height)
    return False
