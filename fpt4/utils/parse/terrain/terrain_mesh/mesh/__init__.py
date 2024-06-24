import typing
import struct
from .node import NodeV1, NodeV0

if typing.TYPE_CHECKING:
    from fpt4.utils.sqpack import SqPack


class PcbHeader(typing.NamedTuple):
    magic: int
    version: int
    node_num: int
    poly_num: int
    struct_ = struct.Struct(b'4I')


class Mesh:
    nodes: list[NodeV1]

    @classmethod
    def get(cls, sq_pack: 'SqPack', path) -> 'Mesh':
        if (c := getattr(sq_pack, '__cached_pcb_mesh', None)) is None:
            setattr(sq_pack, '__cached_pcb_mesh', c := {})
        if path not in c:
            c[path] = cls(sq_pack, path)
        return c[path]

    def __init__(self, sq_pack: 'SqPack', mesh_path: bytes):
        self.path = mesh_path
        self.sq_pack = sq_pack
        view = memoryview(sq_pack.pack.get_file(mesh_path).data_buffer)
        self.header = PcbHeader._make(PcbHeader.struct_.unpack_from(view))
        self.nodes = []
        version = self.header.version
        if version == 1 or version == 4:
            self.__add_node(NodeV1(view[PcbHeader.struct_.size:]))
        elif version == 0:
            self.__add_node(NodeV0(view[PcbHeader.struct_.size:]))
        else:
            raise NotImplementedError(f'unknown version {version}')

    def __add_node(self, _node: NodeV1 | NodeV0):
        if _node.vertex or _node.polygons:
            self.nodes.append(_node)
        if _node.child0:
            self.__add_node(_node.child0)
        if _node.child1:
            self.__add_node(_node.child1)
