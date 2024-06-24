import glm
import math


class SimpleShape:
    def __init__(self, vertex: list[glm.vec3], polygons: list[tuple[int, int, int]]):
        self.vertices = vertex
        self.indices = polygons


# cube from (-1, -1, -1) to (1, 1, 1)
cube = SimpleShape(
    [
        glm.vec3(-1, -1, -1), glm.vec3(-1, -1, 1), glm.vec3(1, -1, 1), glm.vec3(1, -1, -1),
        glm.vec3(-1, 1, -1), glm.vec3(-1, 1, 1), glm.vec3(1, 1, 1), glm.vec3(1, 1, -1),
    ],
    # 0,1,2,3
    # 4,5,6,7
    [
        (0, 2, 1), (0, 3, 2),
        (0, 1, 5), (0, 5, 4),
        (1, 2, 6), (1, 6, 5),
        (2, 3, 7), (2, 7, 6),
        (3, 0, 4), (3, 4, 7),
        (4, 5, 6), (4, 6, 7),
    ]
)

# board from (-1, -1, 0) to (1, 1, 0)
board = SimpleShape(
    [
        glm.vec3(-1, -1, 0), glm.vec3(-1, 1, 0), glm.vec3(1, 1, 0), glm.vec3(1, -1, 0),
    ],
    [
        (0, 1, 2), (0, 2, 3),
        (0, 2, 1), (0, 3, 2),
    ]
)


def generate_cylinder(radius, step, height):
    vertex = []
    polygons = []
    pt_in_circle = 360 // step

    # 生成圆柱体的顶点坐标
    vertex.append(glm.vec3(0, -height, 0))  # 0
    vertex.append(glm.vec3(0, height, 0))  # 1
    for i in range(pt_in_circle):
        theta = math.radians(i * step)
        x = radius * math.cos(theta)
        z = radius * math.sin(theta)
        vertex.append(glm.vec3(x, -height, z))  # 2 + i * 2
        vertex.append(glm.vec3(x, height, z))  # 3 + i * 2

    bottom = lambda i: 2 + i * 2
    top = lambda i: 3 + i * 2

    # 生成圆柱体的顶面和底面
    for i in range(pt_in_circle):
        polygons.append((bottom(i), bottom((i + 1) % pt_in_circle), 0))
        polygons.append((top((i + 1) % pt_in_circle), top(i), 1))

    # 生成圆柱体的侧面
    for i in range(pt_in_circle):
        polygons.append((bottom(i), top((i + 1) % pt_in_circle), bottom((i + 1) % pt_in_circle)))
        polygons.append((bottom(i), top(i), top((i + 1) % pt_in_circle)))

    return SimpleShape(vertex, polygons)


# cylinder height 1, radius 1
cylinder = generate_cylinder(1, 10, 1)


def generate_sphere(radius, step_in_degree):
    vertices = []
    indices = []
    pt_in_circle = 360 // step_in_degree

    assert pt_in_circle % 2 == 0
    vertices.append(glm.vec3(0, -radius, 0))  # 0
    vertices.append(glm.vec3(0, radius, 0))  # 1
    for i in range(1, (pt_in_circle // 2)):
        _a = math.radians(180 - (step_in_degree * i))
        y = radius * math.cos(_a)
        sin_r = radius * math.sin(_a)
        _vertices = []
        for j in range(pt_in_circle):
            _a = math.radians(step_in_degree * j)
            x = sin_r * math.cos(_a)
            z = sin_r * math.sin(_a)
            vertices.append(glm.vec3(x, y, z))

    pt = lambda col, row: col * pt_in_circle + row + 2

    last_col = (pt_in_circle // 2) - 2
    for j in range(pt_in_circle):
        indices.append((pt(0, j), pt(0, (j + 1) % pt_in_circle), 0))
        indices.append((pt(last_col, j), 1, pt(last_col, (j + 1) % pt_in_circle)))

    for i in range(0, last_col):
        i2 = i + 1
        for j in range(pt_in_circle):
            j2 = (j + 1) % pt_in_circle
            indices.append((pt(i, j), pt(i2, j2), pt(i, j2)))
            indices.append((pt(i, j), pt(i2, j), pt(i2, j2)))

    return SimpleShape(vertices, indices)


# Sphere radius 1
sphere = generate_sphere(1, 10)
