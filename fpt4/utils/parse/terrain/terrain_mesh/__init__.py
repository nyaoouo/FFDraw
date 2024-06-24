import dataclasses
import struct
import typing
from .mesh import Mesh

if typing.TYPE_CHECKING:
    from fpt4.utils.sqpack import SqPack


@dataclasses.dataclass
class TerrainHeader:
    mesh_num: int
    min_x: float
    min_y: float
    min_z: float
    max_x: float
    max_y: float
    max_z: float
    __pad: int
    struct_ = struct.Struct(b'I6fI')


@dataclasses.dataclass
class TerrainData:
    mesh_id: int
    min_x: float
    min_y: float
    min_z: float
    max_x: float
    max_y: float
    max_z: float
    __pad: int
    mesh: Mesh = None
    struct_ = struct.Struct(b'I6fI')


class TerrainMesh:
    @classmethod
    def get(cls, sq_pack: 'SqPack', path) -> 'TerrainMesh':
        if (c := getattr(sq_pack, '__cached_terrain_mesh', None)) is None:
            setattr(sq_pack, '__cached_terrain_mesh', c := {})
        if path not in c: c[path] = cls(sq_pack, path)
        return c[path]

    def __init__(self, sq_pack: 'SqPack', terrain_path: bytes):
        self.sq_pack = sq_pack
        self.index_view = memoryview(self.sq_pack.pack.get_file(terrain_path + b'/list.pcb').data_buffer)
        self.index_header = TerrainHeader(*TerrainHeader.struct_.unpack_from(self.index_view))
        self.state_table = [
            TerrainData(*TerrainHeader.struct_.unpack_from(
                self.index_view, i * TerrainData.struct_.size + TerrainHeader.struct_.size
            ))
            for i in range(self.index_header.mesh_num)
        ]
        for m in self.state_table:
            m.mesh = Mesh.get(self.sq_pack, b'%s/tr%04d.pcb' % (terrain_path, m.mesh_id))
