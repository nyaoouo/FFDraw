import enum
import json
import struct

from .define import MacroType, MACRODEFPARAM

# region utils

_int_masks = [
    1 << 3,
    1 << 2,
    1 << 1,
    1 << 0,
]


def read_buffer(buffer: bytearray, size: int):
    res = buffer[:size]
    del buffer[:size]
    return res


def to_string(d, quote_str=True):
    if isinstance(d, str): return repr(d) if quote_str else d
    if isinstance(d, (int, Macro, SeString)): return str(d)
    if isinstance(d, (bytes, bytearray)): return d.hex(' ')
    if isinstance(d, enum.Enum): return d.name
    raise TypeError(f'not support type {type(d)}')


# endregion

# region encode

def encode_integer(value: int, cutoff=0xCF) -> bytearray:
    res = bytearray(1)
    if -1 < value < cutoff:
        res[0] = value + 1
        return res
    res[0] = 0xff
    for _mask, _v in zip(_int_masks, struct.pack(b'>i', value)):
        if _v:
            res.append(_v)
        else:
            res[0] ^= _mask
    res[0] -= 1
    return res


def encode_string(string: 'str|SeString|Macro', encoding='utf-8') -> bytearray:
    res = string.encode(encoding=encoding)
    return bytearray((0xff,)) + encode_integer(len(res)) + res


def encode_any(d, encoding='utf-8'):
    if isinstance(d, int): return encode_integer(d)
    if isinstance(d, (str, SeString, Macro)): return encode_string(d, encoding=encoding)
    if isinstance(d, (bytes, bytearray)): return bytearray(d)
    if isinstance(d, MACRODEFPARAM): return bytearray((d.value,))
    raise TypeError(f"not support type {type(d)}")


# endregion

# region decode
def decode_integer(buffer: bytearray, marker=None):
    if marker is None:
        marker = buffer.pop(0)
    if marker < 0xF0: return marker - 1
    marker += 1
    _buffer = bytearray(4)
    for i, mask in enumerate(_int_masks):
        if marker & mask: _buffer[i] = buffer.pop(0)
    return struct.unpack('>i', _buffer)[0]


def decode_any(buffer: bytearray, marker=None, encoding='utf-8'):
    marker = buffer.pop(0) if marker is None else marker
    if marker == 0xFF:
        return SeString.from_buffer(read_buffer(buffer, decode_integer(buffer)), encoding=encoding)
    elif marker < 0xD0:
        return marker - 1
    elif marker < 0xF0:
        return MACRODEFPARAM(marker)
    else:
        return decode_integer(buffer, marker)


# endregion


class Macro(list):
    def __init__(self, name: MacroType | int, *args):
        self.macro_code = name
        super().__init__(args)

    @classmethod
    def from_buffer(cls, buffer: bytearray, encoding='utf-8'):
        # backup = buffer[:]
        assert buffer.pop(0) == MacroType.BEGIN.value, Exception("Macro must BEGIN with BEGIN")
        obj = cls(MacroType(buffer.pop(0)))
        data = read_buffer(buffer, decode_integer(buffer))
        assert buffer.pop(0) == MacroType.END.value
        v = None
        while data:
            obj.append(decode_any(data, encoding=encoding))
        return obj

    def calc_size(self, encoding='utf-8'):
        data = bytearray()
        for a in self: data.extend(encode_any(a, encoding))
        return len(data)

    def encode(self, encoding='utf-8'):
        data = bytearray()
        for a in self: data.extend(encode_any(a, encoding))
        res = bytearray((
            MacroType.BEGIN.value,
            (self.macro_code if isinstance(self.macro_code, int) else self.macro_code.value),
        )) + encode_integer(len(data)) + data
        res.append(MacroType.END.value)
        return res

    @property
    def name(self):
        return self.macro_code.name if isinstance(self.macro_code, MacroType) else str(self.macro_code)

    def __repr__(self):
        if self:
            args = ', '.join(map(to_string, self))
            return f'<{self.name} ({args})>'
        else:
            return f'<{self.name}>'

    def __add__(self, other):
        if isinstance(other, SeString):
            return SeString(self, *other)
        else:
            return SeString(self, other)


class SeString(list):
    def __init__(self, *args):
        super().__init__(args)

    @classmethod
    def from_buffer(cls, buffer: bytearray, encoding='utf-8') -> 'SeString|str|Macro':
        obj = cls()
        while buffer:
            sep = buffer.find(MacroType.BEGIN.value)
            if sep == -1:
                obj.append(buffer.decode(encoding, 'ignore'))
                buffer.clear()
                break
            elif sep:
                obj.append(read_buffer(buffer, sep).decode(encoding, 'ignore'))
            obj.append(Macro.from_buffer(buffer))
        if len(obj) > 1:
            return obj
        elif not obj:
            return ""
        return obj[0]

    def encode(self, encoding='utf-8'):
        res = bytearray()
        for a in self:
            if isinstance(a, (str, Macro)):
                res.extend(a.encode(encoding=encoding))
            else:
                raise TypeError(f"not support type {type(a)}")
        return res

    def __repr__(self):
        return ''.join(to_string(a, False) for a in self)

    def __add__(self, other):
        if isinstance(other, SeString):
            return SeString(*self, *other)
        else:
            return SeString(*self, other)
