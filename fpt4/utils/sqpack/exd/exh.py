import struct
from collections import namedtuple
from typing import List, Set

Header = namedtuple('ExhHeader', [
    # Common::Component::Excel::EXHeader::EXH
    'magic',
    'version',
    'binary_data_length',
    'column_count',
    'block_count',
    'lang_count',
    'cache',
    'subkey_count',
    'reserved2',
    'row_count',
    'reserved3',
    'reserved4',
])
Column = namedtuple('ExhColumn', [
    'type',
    'offset',
])


class ExhFile:
    header: Header
    columns: List[Column]
    blocks: List[range]
    langs: Set[int]

    def __init__(self, buffer: bytearray):
        self.header = Header._make(struct.unpack_from('>4s8H3I', buffer, 0))
        assert self.header.magic == b'EXHF', 'exh header magic unpair'
        offset = 0x20
        columns = []
        for i in range(self.header.column_count):
            columns.append(Column._make(struct.unpack_from('>2H', buffer, offset)))
            offset += 0x4
        blocks = []
        for i in range(self.header.block_count):
            off, size = struct.unpack_from('>2l', buffer, offset)
            blocks.append(range(off, off + size))
            offset += 0x8
        langs = set()
        for i in range(self.header.lang_count):
            lang = buffer[offset]
            if lang: langs.add(lang)
            offset += 0x2
        self.columns = columns
        self.blocks = blocks
        self.langs = langs
