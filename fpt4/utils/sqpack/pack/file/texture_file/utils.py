import ctypes
import struct

from nylib.struct import fctypes, set_fields_from_annotations, Enum
from nylib.utils.serialize import struct_to_dict
from ..utils import FileCommonHeader


@set_fields_from_annotations
class Attribute(ctypes.Structure):
    _size_ = 0x4
    DISCARD_PER_FRAME: 'fctypes.c_uint|1' = eval("0,0")
    DISCARD_PER_MAP: 'fctypes.c_uint|1' = eval("0,1")
    MANAGED: 'fctypes.c_uint|1' = eval("0,2")
    USER_MANAGED: 'fctypes.c_uint|1' = eval("0,3")
    CPU_READ: 'fctypes.c_uint|1' = eval("0,4")
    LOCATION_MAIN: 'fctypes.c_uint|1' = eval("0,5")
    NO_GPU_READ: 'fctypes.c_uint|1' = eval("0,6")
    ALIGNED_SIZE: 'fctypes.c_uint|1' = eval("0,7")
    EDGE_CULLING: 'fctypes.c_uint|1' = eval("0,8")
    LOCATION_ONION: 'fctypes.c_uint|1' = eval("0,9")
    READ_WRITE: 'fctypes.c_uint|1' = eval("0,10")
    IMMUTABLE: 'fctypes.c_uint|1' = eval("0,11")
    IMMUTABLE_CPU_READ: 'fctypes.c_uint|1' = eval("0,12")
    DYNAMIC_NO_DISCARD: 'fctypes.c_uint|1' = eval("0,13")
    DISCARD_DIRECT_CONSTANT: 'fctypes.c_uint|1' = eval("0,14")
    CPU_READ_WRITE: 'fctypes.c_uint|1' = eval("0,15")
    TEXTURE_RENDER_TARGET: 'fctypes.c_uint|1' = eval("0,20")
    TEXTURE_DEPTH_STENCIL: 'fctypes.c_uint|1' = eval("0,21")
    TEXTURE_TYPE_1D: 'fctypes.c_uint|1' = eval("0,22")
    TEXTURE_TYPE_2D: 'fctypes.c_uint|1' = eval("0,23")
    TEXTURE_TYPE_3D: 'fctypes.c_uint|1' = eval("0,24")
    TEXTURE_TYPE_CUBE: 'fctypes.c_uint|1' = eval("0,25")
    TEXTURE_SWIZZLE: 'fctypes.c_uint|1' = eval("0,26")
    TEXTURE_NO_TILED: 'fctypes.c_uint|1' = eval("0,27")
    TEXTURE_TYPE_2D_ARRAY: 'fctypes.c_uint|1' = eval("0,28")
    TEXTURE_NO_SWIZZLE: 'fctypes.c_uint|1' = eval("0,31")

    def _serialize_(self):
        return {
            'value': struct.unpack('<I', self)[0],
            'flags': tuple(k for k, v in struct_to_dict(self).items() if v),
        }


FMT_INTEGER = 0X1
FMT_FLOAT = 0X2
FMT_DXT = 0X3
FMT_DEPTH_STENCIL = 0X4
FMT_SPECIAL = 0X5
FMT_BC = 0X6
FMT_FLOAT_UNorm = 0X7


def _tf(t, a1, a2, a3):
    return (t << 12) | (a1 << 8) | (a2 << 4) | a3


class TextureFormat(Enum):
    NULL = _tf(FMT_SPECIAL, 1, 0, 0)

    R8G8B8A8_UNorm = _tf(FMT_INTEGER, 4, 5, 0)
    R8G8B8X8_UNorm = _tf(FMT_INTEGER, 4, 5, 1)
    R4G4B4A4_UNorm = _tf(FMT_INTEGER, 4, 4, 0)
    R5G5B5A1_UNorm = _tf(FMT_INTEGER, 4, 4, 1)

    L8_UNorm = _tf(FMT_INTEGER, 1, 3, 0)
    A8_UNorm = _tf(FMT_INTEGER, 1, 3, 1)
    R8_UNorm = _tf(FMT_INTEGER, 1, 3, 2)
    R8_INT = _tf(FMT_INTEGER, 1, 3, 3)

    R16_INT = _tf(FMT_INTEGER, 1, 4, 0)
    R16_FLOAT = _tf(FMT_FLOAT, 1, 4, 0)
    R16_UNorm = _tf(FMT_FLOAT_UNorm, 1, 4, 0)

    R32_INT = _tf(FMT_INTEGER, 1, 5, 0)
    R32_FLOAT = _tf(FMT_FLOAT, 1, 5, 0)
    R32G32_FLOAT = _tf(FMT_FLOAT, 2, 6, 0)
    R32G32B32A32_FLOAT = _tf(FMT_FLOAT, 4, 7, 0)

    R8G8_UNorm = _tf(FMT_INTEGER, 2, 4, 0)

    R16G16_FLOAT = _tf(FMT_FLOAT, 2, 5, 0)
    R16G16_UNorm = _tf(FMT_FLOAT_UNorm, 2, 5, 0)
    R16G16B16A16_FLOAT = _tf(FMT_FLOAT, 4, 6, 0)

    DXT1 = _tf(FMT_DXT, 4, 2, 0)
    DXT3 = _tf(FMT_DXT, 4, 3, 0)
    DXT5 = _tf(FMT_DXT, 4, 3, 1)

    BC5 = _tf(FMT_BC, 2, 3, 0)
    BC7 = _tf(FMT_BC, 4, 3, 2)

    D16 = _tf(FMT_DEPTH_STENCIL, 1, 4, 0)
    D24S8 = _tf(FMT_DEPTH_STENCIL, 2, 5, 0)
    SHADOW16 = _tf(FMT_SPECIAL, 1, 4, 0)
    SHADOW24 = _tf(FMT_SPECIAL, 1, 5, 0)


@set_fields_from_annotations
class FileTexture(FileCommonHeader):
    _size_ = 0X18

    output_lod_num: 'fctypes.c_uint32' = eval('0X14')


@set_fields_from_annotations
class TextureHeader(ctypes.Structure):
    _size_ = 0X50

    type: 'Attribute' = eval('0X0')
    format: 'TextureFormat' = eval('0X4')
    width: 'fctypes.c_uint16' = eval('0X8')
    height: 'fctypes.c_uint16' = eval('0XA')
    depth: 'fctypes.c_uint16' = eval('0XC')
    mip_levels: 'fctypes.c_uint8' = eval('0XE')
    array_size: 'fctypes.c_uint8' = eval('0XF')
    lod_offset: 'fctypes.c_uint32*3' = eval('0X10')
    offset_to_surface: 'fctypes.c_uint32*13' = eval('0X1C')


@set_fields_from_annotations
class LodBlock(ctypes.Structure):
    _size_ = 0X14

    comp_offset: 'fctypes.c_uint32' = eval('0X0')
    comp_size: 'fctypes.c_uint32' = eval('0X4')
    decomp_size: 'fctypes.c_uint32' = eval('0X8')
    block_offset: 'fctypes.c_uint32' = eval('0XC')
    block_num: 'fctypes.c_uint32' = eval('0X10')
