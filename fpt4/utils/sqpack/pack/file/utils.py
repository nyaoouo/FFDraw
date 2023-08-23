import io
import struct
from logging import getLogger
import zlib
from typing import IO, TypeVar, TYPE_CHECKING, Any
from ctypes import Structure
from nylib.struct import fctypes, set_fields_from_annotations

if TYPE_CHECKING:
    from ..indexfile import FileInfo

_t = TypeVar("_t")

BLOCK_INFO = struct.Struct(f'<IIII')
BLOCK_INFO_SIZE = BLOCK_INFO.size
BLOCK_PADDING = 0x80
COMPRESSION_THRESHOLD = 0x7D00


@set_fields_from_annotations
class FileCommonHeader(Structure):
    _size_ = 0X14

    size: 'fctypes.c_uint32' = eval('0X0')
    type: 'fctypes.c_uint32' = eval('0X4')
    file_size: 'fctypes.c_uint32' = eval('0X8')
    number_of_block: 'fctypes.c_uint32' = eval('0XC')
    used_number_of_block: 'fctypes.c_uint32' = eval('0X10')


def read_data_block(src: IO, dst: IO):
    size, version, compressed_size, uncompressed_size = BLOCK_INFO.unpack(src.read(BLOCK_INFO_SIZE))  # CompressionBlockInfo16
    assert size == BLOCK_INFO_SIZE
    is_compressed = compressed_size < COMPRESSION_THRESHOLD
    block_size = uncompressed_size if is_compressed else compressed_size
    if is_compressed and ((block_size + BLOCK_INFO_SIZE) % BLOCK_PADDING) != 0:
        block_size += BLOCK_PADDING - ((block_size + BLOCK_INFO_SIZE) % BLOCK_PADDING)
    buffer = src.read(block_size)
    if is_compressed:
        assert uncompressed_size == dst.write(zlib.decompress(buffer, -15)), RuntimeError("Inflated block does not match indicated size")
    else:
        dst.write(buffer)


class File:
    header: FileCommonHeader
    info: 'FileInfo'
    data: Any
    logger = getLogger(f'SqPack/File')

    def __init__(self, info: 'FileInfo', header_data: bytes):
        self.info = info
        self.header_buffer = bytearray(header_data)
        self.header = FileCommonHeader.from_buffer(self.header_buffer)
        self.data_size = self.header.file_size - self.header.size
        self._data_buffer: bytearray | None = None

    def get_data_buffer(self, stream: IO) -> bytearray:
        return bytearray(stream.read(self.data_size))

    @property
    def data_buffer(self) -> bytearray:
        if self._data_buffer is None:
            self.logger.log(9, 'reading %s...', self.info.full_path)
            self._data_buffer = self.get_data_buffer(self.data_stream)
        return self._data_buffer

    @property
    def data_stream(self) -> IO:
        stream = self.info.dir.index.pack.get_data_stream(self.info.info.data_file_id)
        stream.seek(self.info.offset + self.header.size)
        return stream
