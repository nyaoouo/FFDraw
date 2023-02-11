import io
import struct
from ctypes import Structure

from nylib.struct import fctypes, set_fields_from_annotations
from .utils import FileCommonHeader, read_data_block, File


@set_fields_from_annotations
class FileModel(FileCommonHeader):
    _size_ = 0XD4

    version: 'fctypes.c_uint32' = eval('0X14')
    stack_memory_size: 'fctypes.c_uint32' = eval('0X18')
    runtime_memory_size: 'fctypes.c_uint32' = eval('0X1C')
    vertex_buffer_size: 'fctypes.c_uint32*3' = eval('0X20')
    edge_geometry_vertex_buffer_size: 'fctypes.c_uint32*3' = eval('0X2C')
    index_buffer_size: 'fctypes.c_uint32*3' = eval('0X38')
    compressed_stack_memory_size: 'fctypes.c_uint32' = eval('0X44')
    compressed_runtime_memory_size: 'fctypes.c_uint32' = eval('0X48')
    compressed_vertex_buffer_size: 'fctypes.c_uint32*3' = eval('0X4C')
    compressed_edge_geometry_vertex_buffer_size: 'fctypes.c_uint32*3' = eval('0X58')
    compressed_index_buffer_size: 'fctypes.c_uint32*3' = eval('0X64')
    stack_memory_offset: 'fctypes.c_uint32' = eval('0X70')
    runtime_memory_offset: 'fctypes.c_uint32' = eval('0X74')
    vertex_buffer_offset: 'fctypes.c_uint32*3' = eval('0X78')
    edge_geometry_vertex_buffer_offset: 'fctypes.c_uint32*3' = eval('0X84')
    index_buffer_offset: 'fctypes.c_uint32*3' = eval('0X90')
    stack_data_block_index: 'fctypes.c_uint16' = eval('0X9C')
    runtime_data_block_index: 'fctypes.c_uint16' = eval('0X9E')
    vertex_buffer_data_block_index: 'fctypes.c_uint16*3' = eval('0XA0')
    edge_geometry_vertex_buffer_data_block_index: 'fctypes.c_uint16*3' = eval('0XA6')
    index_buffer_data_block_index: 'fctypes.c_uint16*3' = eval('0XAC')
    stack_data_block_num: 'fctypes.c_uint16' = eval('0XB2')
    runtime_data_block_num: 'fctypes.c_uint16' = eval('0XB4')
    vertex_buffer_data_block_num: 'fctypes.c_uint16*3' = eval('0XB6')
    edge_geometry_vertex_buffer_data_block_num: 'fctypes.c_uint16*3' = eval('0XBC')
    index_buffer_data_block_num: 'fctypes.c_uint16*3' = eval('0XC2')
    vertex_declaration_num: 'fctypes.c_uint16' = eval('0XC8')
    material_num: 'fctypes.c_uint16' = eval('0XCA')
    lod_num: 'fctypes.c_uint8' = eval('0XCC')
    enable_index_buffer_streaming: 'fctypes.c_int8' = eval('0XCD')
    enable_edge_geometry: 'fctypes.c_int8' = eval('0XCE')
    compressed_block_size: 'fctypes.c_uint16*1' = eval('0XD0')


class ModelFile(File):
    header: FileModel

    def __init__(self, info, header_data: bytes):
        super().__init__(info, header_data)
        self.header = FileModel.from_buffer(self.header_buffer)
