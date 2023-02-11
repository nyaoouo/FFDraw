import ctypes
import dataclasses
import re
import typing
import sys
from . import field
from ..utils._lazy_chunk import lazy_chunks_key

_CData = ctypes.c_int.__mro__[2]
_CStruct = typing.TypeVar('_CStruct')
bf_regex = re.compile(r'\| *(\d+|0x[\da-fA-F]+|0o[0-7]+|0b[10]+) *$')


def set_fields_from_annotations(cls: typing.Type[_CStruct]) -> typing.Type[_CStruct]:
    if not (annotations := getattr(cls, '__annotations__', None)): return cls
    global_namespace = getattr(sys.modules.get(cls.__module__, None), '__dict__', {})
    global_namespace[cls.__name__] = cls
    local_namespace = dict(vars(cls))
    fields = []
    off_fields = []

    def str_eval(v):
        if isinstance(v, str):
            return eval(v, global_namespace, local_namespace)
        return v

    if True:  # hasattr(global_namespace, lazy_chunks_key):
        def str_eval_with_lazy(v):
            if isinstance(v, str):
                for chunk in global_namespace.pop(lazy_chunks_key, ()):
                    chunk._load()
                return eval(v, global_namespace, local_namespace)
            return v
    else:
        str_eval_with_lazy = str_eval

    for name, type_hint in annotations.items():
        if isinstance(type_hint, str) and (match := bf_regex.search(type_hint)):
            bit_size = eval(match.group(1))
            type_hint = str_eval(type_hint[:match.start()])
            desc = (name, type_hint, bit_size)
            if preset := getattr(cls, name, None):
                byte_offset, bit_offset = preset
                setattr(cls, name, field.BitField(byte_offset, bit_offset, type_hint, bit_size))
                off_fields.append(desc)
            else:
                fields.append(desc)
        # field
        elif (byte_offset := getattr(cls, name, None)) is not None:
            setattr(cls, name, field.Field(type_hint, byte_offset, str_eval_with_lazy))
            off_fields.append((name, type_hint))
        else:
            fields.append((name, str_eval(type_hint)))
    if size := cls.__dict__.get('_size_'):
        try:
            p_size = ctypes.sizeof(cls.__mro__[1])
        except TypeError:
            p_size = 0
        fields.append(('__nys_padding__', ctypes.c_char * (size - p_size)))
    cls._fields_ = fields
    cls._off_fields_ = off_fields
    return cls


def offset(off: int, cls: typing.Type = None):
    if cls is None: return lambda _cls: offset(off, _cls)
    new_fields = []
    for base in reversed(cls.__mro__):
        if '_use_broken_old_ctypes_structure_semantics_' in cls.__dict__:
            new_fields.clear()
        new_fields.extend(base.__dict__.get('_fields_', []))
        # new_fields.extend(getattr(base, '_fields_', []))
    # print(cls.__name__, new_fields)
    name_space = {
        '_use_broken_old_ctypes_structure_semantics_': True,
        '_fields_': [('__padding__', ctypes.c_uint8 * off), *new_fields]
    }
    new_off_fields = []
    for base in reversed(cls.__mro__):
        if '_use_broken_old_ctypes_structure_semantics_' in cls.__dict__:
            new_off_fields.clear()
        new_off_fields.extend(getattr(base, '_off_fields_', []))
    for name, *_ in new_off_fields:
        old_field: field.Field = getattr(cls, name)
        name_space[name] = field.Field(old_field._d_type, old_field.offset + off, old_field.str_eval)
    if new_off_fields:
        name_space['_off_fields_'] = new_off_fields
    return type(f'{cls.__name__}_off_{off}', (cls,), name_space)
