import enum
from ctypes import *

from nylib.struct import set_fields_from_annotations, fctypes


class CompressType(enum.Enum):
    none = 0X0
    zip = 0X1
    oodle = 0X2


@set_fields_from_annotations
class BundleHeader(Structure):
    _size_ = 0X28

    magic: 'c_char*16' = eval('0X0')
    timestamp_ms: 'fctypes.c_uint64' = eval('0X10')
    size: 'fctypes.c_uint32' = eval('0X18')
    proto_type: 'fctypes.c_uint16' = eval('0X1C')
    element_count: 'fctypes.c_uint16' = eval('0X1E')
    unk: 'fctypes.c_uint8' = eval('0X20')
    compress_type: 'fctypes.c_uint8' = eval('0X21')
    size_before_compress: 'fctypes.c_uint32' = eval('0X24')


@set_fields_from_annotations
class ElementHeader(Structure):
    _size_ = 0X10

    size: 'fctypes.c_uint32' = eval('0X0')
    source_id: 'fctypes.c_uint32' = eval('0X4')
    target_id: 'fctypes.c_uint32' = eval('0X8')
    type: 'fctypes.c_uint16' = eval('0XC')


@set_fields_from_annotations
class IpcHeader(Structure):
    _size_ = 0X10
    unk: 'fctypes.c_uint8' = eval('0X0')
    size: 'fctypes.c_uint8' = eval('0X1')
    proto_no: 'fctypes.c_uint16' = eval('0X2')
    packet_count: 'fctypes.c_uint16' = eval('0X4')
    timestamp_s: 'fctypes.c_uint32' = eval('0X8')
