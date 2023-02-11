import io
import struct
from ctypes import Structure

from nylib.struct import fctypes, set_fields_from_annotations
from .utils import FileCommonHeader, read_data_block, File


@set_fields_from_annotations
class FileCompressedData(FileCommonHeader):
    @set_fields_from_annotations
    class CompressedDataBlockInfo(Structure):
        _size_ = 0X8
        compressed_data_block_offset: 'fctypes.c_uint32' = eval('0X0')
        compressed_data_block_size: 'fctypes.c_uint16' = eval('0X4')
        uncompressed_data_block_size: 'fctypes.c_uint16' = eval('0X6')

    _size_ = 0X18
    number_of_compressed_data_block_info: 'fctypes.c_uint32' = eval('0X14')
    compressed_data_block_info: 'CompressedDataBlockInfo*1' = eval('0X18')


COMPRESSED_DATA_BLOCK_INFO_OFFSET = 0x18  # FileCompressedData.compressed_data_block_info
COMPRESSED_DATA_BLOCK_INFO_SIZE = 0x8  # CompressedDataBlockInfo


class CompressedFile(File):
    header: FileCompressedData

    def __init__(self, info, header_data: bytes):
        super().__init__(info, header_data)
        self.header = FileCompressedData.from_buffer(self.header_buffer)

    def get_data_buffer(self, stream):
        data_pos = stream.tell()
        with io.BytesIO() as data_stream:
            for i in range(self.header.number_of_compressed_data_block_info):
                offset, compressed_size, uncompressed_size = struct.unpack_from(
                    f'<IHH', self.header_buffer,
                    COMPRESSED_DATA_BLOCK_INFO_OFFSET + i * COMPRESSED_DATA_BLOCK_INFO_SIZE
                )  # CompressedDataBlockInfo
                stream.seek(data_pos + offset)
                read_data_block(stream, data_stream)
            return bytearray(data_stream.getvalue())
