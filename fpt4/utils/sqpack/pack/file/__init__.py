import struct
from typing import IO, TYPE_CHECKING

from .utils import File
from .compressed_file import CompressedFile
from .model_file import ModelFile
from .texture_file import TextureFile

if TYPE_CHECKING:
    from ..indexfile import FileInfo

file_handlers = {
    0: File,  # 0:fallback
    1: File,  # NormalFile # 1:FILE_TYPE_NORMAL
    2: CompressedFile,  # 2:TYPE_SPURS_COMPRESSED
    3: ModelFile,  # 3:FILE_TYPE_MODEl
    4: TextureFile,  # 4:FILE_TYPE_TEXTURE
}


def file_from_stream(info: 'FileInfo', stream: IO) -> File:
    header_size, file_type = struct.unpack(b'<II', stream.read(0x8))
    stream.seek(-8,1)
    return file_handlers.get(file_type, File)(info, stream.read(header_size))
