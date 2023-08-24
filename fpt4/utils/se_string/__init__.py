import enum
import struct
import typing

from .define import MacroType, MACRODEFPARAM

if typing.TYPE_CHECKING:
    from ..sqpack import SqPack

_sq_pack: 'SqPack|None' = None


def get_sq_pack():
    global _sq_pack
    if _sq_pack is not None:
        return _sq_pack
    try:
        from fpt4.utils.sqpack import SqPack
        _sq_pack = SqPack.get()
    except (ImportError, StopIteration):
        pass
    return _sq_pack


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
        return encode_macro(self)

    def __add__(self, other):
        if isinstance(other, SeString):
            return SeString(self, *other)
        else:
            return SeString(self, other)


_encode_macro_map = {}
add_encode_macro = lambda macro_type: lambda func: _encode_macro_map.__setitem__(macro_type, func)
default_encode_macro = lambda macro: f"<{macro.name} ({', '.join(map(to_string, macro))})>" if macro else f'<{macro.name}>'
encode_macro = lambda macro: _encode_macro_map.get(macro.macro_code, default_encode_macro)(macro)

_special_fixed = [None for _ in range(12)]
add_special_fixed = lambda special_type: lambda func: _special_fixed.__setitem__(special_type - 1, func)


@add_special_fixed(1)
def encode_special_fixed_name(args):
    sq_pack = get_sq_pack()
    world_id, name, *_ = args
    if not world_id: return str(name)
    try:
        world_str = sq_pack.sheets.world_sheet[world_id].display_name
    except KeyError:
        world_str = world_id
    return f'{name}@{world_str}'


@add_special_fixed(2)
def encode_special_fixed_job(args):
    sq_pack = get_sq_pack()
    job_id, level, *_ = args
    try:
        job = sq_pack.sheets.class_job_sheet[job_id].text_name
    except KeyError:
        job = f'JOB({job_id})'
    return f'{job}-lv{level}'


def map_to_game_coord(pos, scale, offset):
    return (pos - 1 - 2050 / scale) / (41 / 2048) - offset


@add_special_fixed(3)
def encode_special_fixed_pos(args):
    sq_pack = get_sq_pack()
    t_id, map_id, x, z, y, *_ = args
    try:
        territory = sq_pack.sheets.territory_type_sheet[t_id]
    except KeyError:
        territory = f'TERRITORY({t_id})'
    else:
        territory = f'{territory.region.text_sgl} - {territory.sub_region.text_sgl} - {territory.area.text_sgl}'
    try:
        map_ = sq_pack.sheets.map_sheet[map_id]
    except KeyError:
        map_s = f'MAP({map_id})'
    else:
        map_s = map_.floor_name_ui.text_sgl
        if map_s: map_s = f'[{map_s}]'
    y = 'inv' if y == -30000 else f'{y:.2f}'
    return f'{territory}{map_s} ({x / 1000:.2f}, {y}, {z / 1000:.2f})'


@add_special_fixed(4)
def encode_special_fixed_item(args):
    sq_pack = get_sq_pack()
    item_id, *_ = args  # item_id, param, rarity, _, _, display name
    if item_id >= 2000000:
        try:
            item = f"{sq_pack.sheets.event_item_sheet[item_id].text_ui_name}#{item_id}"
        except KeyError:
            item = f'EITEM({item_id})'
    else:
        if hq := item_id >= 1000000:
            item_id -= 1000000
        if collectable := item_id >= 500000:
            item_id -= 500000
        try:
            item = f"{sq_pack.sheets.item_sheet[item_id].text_ui_name}#{item_id}"
        except KeyError:
            item = f'ITEM({item_id})'
        if collectable:
            item += "[Collectable]"
        if hq:
            item += "[HQ]"
    return item


@add_special_fixed(5)
def encode_special_fixed_se(args):
    return f'SE#{args[0]}'


@add_special_fixed(6)
def encode_special_fixed_obj(args):
    sq_pack = get_sq_pack()
    name_id = args[0]
    try:
        return f"NpcName#{sq_pack.sheets.b_npc_name_sheet[name_id].singular}"
    except KeyError:
        return f'NpcName#{name_id}'


@add_special_fixed(8)
def encode_special_fixed_recast(args):
    sec = args[0]
    return f'Recast#{sec}s'


mentor_name = ['None', 'beginner', 'returner', 'big mentor', 'pve mentor', 'live mentor', 'pvp mentor', 'need update']


@add_special_fixed(9)
def encode_special_fixed_mentor(args):
    return f'Mentor#{mentor_name[args[0]]}'


@add_special_fixed(10)
def encode_special_fixed_status(args):
    sq_pack = get_sq_pack()
    status_id = args[0]
    try:
        return f'Status#{sq_pack.sheets.status_sheet[status_id][0]}#{status_id}'
    except KeyError:
        return f'Status#{status_id}#{status_id}'


@add_special_fixed(11)
def encode_special_fixed_finder(args):
    id1, id2, id3, is_world, *_ = args
    finder_id = id3 << 48 | id2 << 24 | id1
    if is_world:
        return f'LocalWorldFinder#{finder_id:X}'
    else:
        return f'CrossWorldFinder#{finder_id:X}'


@add_special_fixed(12)
def encode_special_fixed_quest(args):
    sq_pack = get_sq_pack()
    quest_id = args[0]
    try:
        return f'Quest#{sq_pack.sheets.quest_sheet[0x10000 | quest_id][0]}'
    except KeyError:
        return f'Quest#{quest_id}'


@add_encode_macro(MacroType.FIXED)
def encode_fixed(macro: Macro):
    sq_pack = get_sq_pack()
    if sq_pack is None: return default_encode_macro(macro)
    if not hasattr(sq_pack, '__completion_group_cache__'):
        cache = {}
        completion_sheet = sq_pack.sheets.completion_sheet
        for row in completion_sheet:
            lt = str(row.lookup_table)
            if lt and lt[0] != '@':
                cache[row.group] = sq_pack.exd.get_sheet_raw(lt.split('[', 1)[0])
        setattr(sq_pack, '__completion_group_cache__', cache)
    else:
        cache = getattr(sq_pack, '__completion_group_cache__')
    group, key, *args = macro
    if group == 200:
        try:
            if 1 <= key <= 12 and (encoder := _special_fixed[key - 1]):
                return f"<{macro.name} ({encoder(args)})>"
        except:
            pass
        return default_encode_macro(macro)
    if sheet := cache.get(group + 1):
        try:
            row = sheet[key]
        except KeyError:
            return f"<{macro.name} ({sheet.name}#{key})>"
        else:
            return f"<{macro.name} ({sheet.name}#{row[0]})>"
    return f"<{macro.name} ({sq_pack.sheets.completion_sheet[key].text})>"


class SeString(list):
    def __init__(self, *args):
        super().__init__(args)

    @classmethod
    def from_buffer(cls, buffer: bytearray | bytes, encoding='utf-8') -> 'SeString|str|Macro':
        if isinstance(buffer, bytes): buffer = bytearray(buffer)
        obj = cls()
        if (end := buffer.find(0)) != -1: del buffer[end:]
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
