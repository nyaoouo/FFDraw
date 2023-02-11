import io
import struct
import ctypes

from ..utils import read_data_block, File
from .utils import FileTexture, TextureHeader, LodBlock
from .processors import process

HEADER_SIZE = ctypes.sizeof(FileTexture)
TEXTURE_HEADER_SIZE = ctypes.sizeof(TextureHeader)


class TextureFile(File):
    header: FileTexture

    def __init__(self, info, header_data: bytes):
        super().__init__(info, header_data)
        self.header = FileTexture.from_buffer(self.header_buffer)
        self.lod_blocks = (LodBlock * self.header.output_lod_num).from_buffer(self.header_buffer, HEADER_SIZE)
        self.texture_header = TextureHeader.from_buffer_copy(self.data_stream.read(TEXTURE_HEADER_SIZE))

    def get_data_buffer(self, stream):
        stream.seek(TEXTURE_HEADER_SIZE, 1)
        pos = stream.tell()
        with io.BytesIO() as data_stream:
            for _len, in struct.iter_unpack(
                    '<H', self.header_buffer[HEADER_SIZE + ctypes.sizeof(self.lod_blocks):]
            ):
                if not _len: break
                stream.seek(pos)
                read_data_block(stream, data_stream)
                pos += _len
            return bytearray(data_stream.getvalue())

    def get_image(self):
        th = self.texture_header
        return process(th.format.value, self.data_buffer, th.width, th.height)
