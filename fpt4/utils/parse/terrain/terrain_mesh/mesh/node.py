import typing
import struct
from glm import vec3
from ...utils import vec3_from_buffer

CompVertex3Struct = struct.Struct(b'3H')


class Polygon(typing.NamedTuple):
    p0: int
    p1: int
    p2: int
    pad_: int
    attr: int
    struct_ = struct.Struct(b'!4BQ')


class HeaderV0(typing.NamedTuple):
    magic: int
    version: int
    child0: int
    child1: int
    aabb_min_x: float
    aabb_min_y: float
    aabb_min_z: float
    aabb_max_x: float
    aabb_max_y: float
    aabb_max_z: float
    vertex_num: int
    polygon_num: int
    struct_ = struct.Struct(b'4i6f2i')


class NodeV0:
    def __init__(self, view):
        self.header = HeaderV0._make(HeaderV0.struct_.unpack_from(view))
        print(self.header)
        if self.header.child0 > 0 and self.header.child1 > 0:
            self.child0 = NodeV0(view[self.header.child0:])
            self.child1 = NodeV0(view[self.header.child1:])
        else:
            self.child0 = None
            self.child1 = None
        comp_vertex_offset = HeaderV0.struct_.size
        polygon_offset = comp_vertex_offset + CompVertex3Struct.size * self.header.vertex_num

        self.polygons = [Polygon._make(t) for t in Polygon.struct_.iter_unpack(view[polygon_offset:polygon_offset + Polygon.struct_.size * self.header.polygon_num])]

        min_x = self.header.aabb_min_x
        min_y = self.header.aabb_min_y
        min_z = self.header.aabb_min_z
        scale_x = (self.header.aabb_max_x - min_x) / 65535
        scale_y = (self.header.aabb_max_y - min_y) / 65535
        scale_z = (self.header.aabb_max_z - min_z) / 65535
        self.vertex = [vec3(x * scale_x + min_x, y * scale_y + min_y, z * scale_z + min_z) for x, y, z in CompVertex3Struct.iter_unpack(view[comp_vertex_offset:polygon_offset])]


class HeaderV1(typing.NamedTuple):
    magic: int
    version: int
    child0: int
    child1: int
    aabb_min_x: float
    aabb_min_y: float
    aabb_min_z: float
    aabb_max_x: float
    aabb_max_y: float
    aabb_max_z: float
    vertex_num: int
    polygon_num: int
    float_vertex_num: int
    pad: int
    struct_ = struct.Struct(b'4i6f4H')


class NodeV1:
    def __init__(self, view):
        self.header = HeaderV1._make(HeaderV1.struct_.unpack_from(view))
        self.child0 = NodeV1(view[self.header.child0:]) if self.header.child0 > 0 else None
        self.child1 = NodeV1(view[self.header.child1:]) if self.header.child1 > 0 else None
        float_vertex_offset = HeaderV1.struct_.size
        comp_vertex_offset = float_vertex_offset + 12 * self.header.float_vertex_num
        polygon_offset = comp_vertex_offset + CompVertex3Struct.size * self.header.vertex_num
        self.vertex = [vec3_from_buffer(view, float_vertex_offset + i * 12) for i in range(self.header.float_vertex_num)]
        self.polygons = [Polygon._make(t) for t in Polygon.struct_.iter_unpack(view[polygon_offset:polygon_offset + Polygon.struct_.size * self.header.polygon_num])]

        min_x = self.header.aabb_min_x
        min_y = self.header.aabb_min_y
        min_z = self.header.aabb_min_z
        scale_x = (self.header.aabb_max_x - min_x) / 65535
        scale_y = (self.header.aabb_max_y - min_y) / 65535
        scale_z = (self.header.aabb_max_z - min_z) / 65535
        for x, y, z in CompVertex3Struct.iter_unpack(view[comp_vertex_offset:polygon_offset]):
            self.vertex.append(vec3(x * scale_x + min_x, y * scale_y + min_y, z * scale_z + min_z))
