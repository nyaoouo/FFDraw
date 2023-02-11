import glm


class View:
    def __init__(self):
        self.projection_view = None
        self.screen_size = None

        self._camera_pos = None
        self._camera_rot = None

    def init_camera_data(self, projection_matrix: glm.mat4, screen_size: glm.vec2):
        self.projection_view = projection_matrix
        self.screen_size = screen_size

    def world_to_screen(self, x, y, z) -> tuple[glm.vec2, bool]:
        mvp = self.projection_view * glm.vec4(x, y, z, 1)
        pos = glm.vec2(mvp.x, mvp.y) / abs(mvp.w)
        out_of_screen = mvp.w < 0 or pos.x < -1 or pos.x > 1 or pos.y < -1 or pos.y > 1
        return pos, not out_of_screen

    def cut_point_at_border(self, start_x, start_y, end_x, end_y):
        if (abs(start_x) > 1 or abs(start_y) > 1) and (abs(end_x) > 1 or abs(end_y) > 1):
            return None
        if start_x == end_x:
            if start_y == end_y: return glm.vec2(start_x, start_y)
            return glm.vec2(start_x, (1 if end_y > start_y else -1))
        elif start_y == end_y:
            return glm.vec2((1 if end_x > start_x else -1), start_y)
        else:
            slope = (end_y - start_y) / (end_x - start_x)
            x_border = 1 if end_x > start_x else -1
            y_at_x_border = (x_border - start_x) * slope + start_y
            if 1 >= y_at_x_border >= -1:
                return glm.vec2(x_border, y_at_x_border)
            else:
                y_border = 1 if end_y > start_y else -1
                return glm.vec2((y_border - start_y) / slope + start_x, y_border)
