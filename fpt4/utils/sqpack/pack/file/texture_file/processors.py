import io
import struct
import typing

from .utils import TextureFormat

if typing.TYPE_CHECKING:
    from PIL import Image


def get_pil_img():
    try:
        from PIL import Image
    except ImportError:
        raise ImportError('Please install pillow to process images')
    return Image


def process_R5G5B5A1_UNorm(src: bytes, width: int, height: int):
    pil_img = get_pil_img()
    with io.BytesIO() as dst:
        for v, in struct.iter_unpack('H', src):
            a = v & 0x8000
            r = v & 0x7C00
            g = v & 0x03E0
            b = v & 0x001F
            rgb = ((r << 9) | (g << 6) | (b << 3))
            argb_value = (a * 0x1FE00 | rgb | ((rgb >> 5) & 0x070707))
            dst.write(bytes((
                (argb_value >> 16) & 0xFF,
                (argb_value >> 8) & 0xFF,
                (argb_value) & 0xFF,
                (argb_value >> 24) & 0xFF,
            )))
        return pil_img.frombytes('RGBA', (width, height), dst.getvalue())


def process_R4G4B4A4_UNorm(src: bytes, width: int, height: int):
    pil_img = get_pil_img()
    with io.BytesIO() as dst:
        for v, in struct.iter_unpack('H', src):
            dst.write(bytes((
                ((v >> 8) & 0x0F) << 4,
                ((v >> 4) & 0x0F) << 4,
                ((v) & 0x0F) << 4,
                ((v >> 12) & 0x0F) << 4,
            )))
        return pil_img.frombytes('RGBA', (width, height), dst.getvalue())


def process_R8G8B8A8_UNorm(src: bytes, width: int, height: int):
    pil_img = get_pil_img()
    with io.BytesIO() as dst:
        for v, in struct.iter_unpack('L', src):
            dst.write(bytes((
                (v >> 16) & 0xFF,
                (v >> 8) & 0xFF,
                (v) & 0xFF,
                (v >> 24) & 0xFF,
            )))
        return pil_img.frombytes('RGBA', (width, height), dst.getvalue())


def process_L8_UNorm(src: bytes, width: int, height: int):
    pil_img = get_pil_img()
    with io.BytesIO() as dst:
        for v, in struct.iter_unpack('L', src):
            r = v & 0xE0
            g = v & 0x1C
            b = v & 0x03
            dst.write(bytes((
                (r | (r << 3) | (r << 6)) & 0xFF,
                (g | (g << 3) | (g << 6)) & 0xFF,
                (b | (b << 2) | (b << 4) | (b << 6)) & 0xFF,
            )))
        return pil_img.frombytes('RGB', (width, height), dst.getvalue())


def process_DXT1(src: bytes, width: int, height: int):
    return get_pil_img().open(io.BytesIO(struct.pack(
        '<4sLLLL56xLL4s20xL16x',
        b'DDS ', 124, 0x1007, height, width,
        32, 0x04, b'DXT1', 0x1000
    ) + src))


def process_DXT3(src: bytes, width: int, height: int):
    return get_pil_img().open(io.BytesIO(struct.pack(
        '<4sLLLL56xLL4s20xL16x',
        b'DDS ', 124, 0x1007, height, width,
        32, 0x04, b'DXT3', 0x1000
    ) + src))


def process_DXT5(src: bytes, width: int, height: int):
    return get_pil_img().open(io.BytesIO(struct.pack(
        '<4sLLLL56xLL4s20xL16x',
        b'DDS ', 124, 0x1007, height, width,
        32, 0x04, b'DXT5', 0x1000
    ) + src))


format_processors: 'typing.Dict[int,typing.Callable[[bytes,int,int],Image.Image]]' = {
    TextureFormat.R5G5B5A1_UNorm: process_R5G5B5A1_UNorm,
    TextureFormat.R4G4B4A4_UNorm: process_R4G4B4A4_UNorm,
    TextureFormat.R8G8B8A8_UNorm: process_R8G8B8A8_UNorm,
    TextureFormat.A8_UNorm: process_R8G8B8A8_UNorm,
    TextureFormat.R32_FLOAT: process_R8G8B8A8_UNorm,
    TextureFormat.L8_UNorm: process_L8_UNorm,
    TextureFormat.DXT1: process_DXT1,
    TextureFormat.DXT3: process_DXT3,
    TextureFormat.DXT5: process_DXT5,
}


def process(fmt: int, src: bytes, width: int, height: int) -> 'Image.Image':
    if f := format_processors.get(fmt):
        return f(src, width, height)
    raise NotImplementedError(f'0x{fmt:04X} doesnt implement processor')
