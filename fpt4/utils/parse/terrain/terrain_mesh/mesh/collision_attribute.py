def get_id(n):
    return n >> 0x0 & 0b1111111


def is_env_set(n):
    return n >> 0x7 & 0b111


def is_navi_mesh_collision_disabled(n):
    return n >> 0xa & 0b1


def is_water_surface(n):
    return n >> 0xb & 0b1


def is_camera(n):
    return n >> 0xc & 0b1


def is_character_collision(n):
    return n >> 0xd & 0b1


def is_eye_collision(n):
    return n >> 0xe & 0b1


def is_fishing(n):
    return n >> 0xf & 0b1


def is_housing(n):
    return n >> 0x10 & 0b1


def is_gimmick(n):
    return n >> 0x11 & 0b1


def is_room(n):
    return n >> 0x12 & 0b1


def is_table(n):
    return n >> 0x13 & 0b1


def is_wall(n):
    return n >> 0x14 & 0b1


def is_keep_out_for_flying(n):
    return n >> 0x15 & 0b1


def is_swimming(n):
    return n >> 0x16 & 0b1


def is_dive(n):
    return n >> 0x17 & 0b1


def is_surface(n):
    return n >> 0x18 & 0b1


def is_game_contents(n):
    return n >> 0x19 & 0b1


def is_game_contents2(n):
    return n >> 0x1a & 0b1


def is_battle_watch(n):
    return n >> 0x1b & 0b1


def is_camera_distance_collision(n):
    return n >> 0x1c & 0b1
