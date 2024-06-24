import struct
import ctypes

from glm import vec3

from nylib.struct import set_fields_from_annotations, fctypes


@set_fields_from_annotations
class Color(ctypes.Structure):
    _size_ = 0X4
    red: 'fctypes.c_uint8' = eval('0X0')
    green: 'fctypes.c_uint8' = eval('0X1')
    blue: 'fctypes.c_uint8' = eval('0X2')
    alpha: 'fctypes.c_uint8' = eval('0X3')


@set_fields_from_annotations
class ColorHDRI(ctypes.Structure):
    _size_ = 0X8
    red: 'fctypes.c_uint8' = eval('0X0')
    green: 'fctypes.c_uint8' = eval('0X1')
    blue: 'fctypes.c_uint8' = eval('0X2')
    alpha: 'fctypes.c_uint8' = eval('0X3')
    intensity: 'fctypes.c_float' = eval('0X4')


FileHeaderStruct = struct.Struct(b'4s2i')
ChunkHeaderStruct = struct.Struct(b'4si')


def find_binary_by_chunk_id(view: memoryview, chunk_id: bytes, file_id: bytes = None):
    file_id_, file_size, total_chunk_count = FileHeaderStruct.unpack_from(view)
    if file_id: assert file_id_ == file_id, f"file id not match require:{file_id} given {file_id_}"
    offset = FileHeaderStruct.size
    for i in range(total_chunk_count):
        chunk_id_, chunk_size = ChunkHeaderStruct.unpack_from(view, FileHeaderStruct.size)
        if chunk_id_ == chunk_id:
            return view[offset + ChunkHeaderStruct.size:]
        offset += chunk_size
    raise ModuleNotFoundError(f'binary with chunk id {chunk_id} not found')


def vec3_from_buffer(buf, off):
    return vec3.from_bytes(bytes(buf[off:off + 12]))


def offset_string(name):
    return property(lambda self: ctypes.c_char_p(ctypes.addressof(self) + getattr(self, name)).value)
