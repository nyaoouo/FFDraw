import ctypes
import functools
import struct
import typing

from nylib.struct import set_fields_from_annotations, fctypes
from ..utils import find_binary_by_chunk_id, offset_string

if typing.TYPE_CHECKING:
    from fpt4.utils.sqpack import SqPack


@set_fields_from_annotations
class SharedGroup(ctypes.Structure):
    _size_ = 0X10

    @classmethod
    def get(cls, sq_pack: 'SqPack', path) -> 'SharedGroup':
        if (c := getattr(sq_pack, '__cached_shared_group', None)) is None:
            setattr(sq_pack, '__cached_shared_group', c := {})
        if path not in c:
            c[path] = res = cls.from_buffer(find_binary_by_chunk_id(
                memoryview(sq_pack.pack.get_file(path).data_buffer),
                b'SCN1', b'SGB1'
            ))
            res.path = path
            return res
        return c[path]
