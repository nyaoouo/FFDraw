import ctypes
import dataclasses
import functools


def struct_to_dict(data, show_us=False):
    d = {}
    for base in data.__class__.__mro__[-4::-1]:
        base_dict = base.__dict__
        for n, *_ in base_dict.get('_fields_', []):
            if (show_us or not n[0] == '_') and n != '__nys_padding__':
                d[n] = serialize_data(getattr(data, n))
        for n, *_ in base_dict.get('_off_fields_', []):
            if show_us or not n[0] == '_':
                d[n] = serialize_data(getattr(data, n))
        if (pf := base_dict.get('_properties_field_')) is None:
            setattr(base, '_properties_field_', pf := [k for k, v in base_dict.items() if isinstance(v, (property, functools.cached_property))])
        for n in pf:
            if show_us or not n.startswith('_'):
                d[n] = serialize_data(getattr(data, n))
    return d


def array_to_list(data, show_us=False):
    base_type = data.__class__._type_
    if base_type == ctypes.c_uint8 or base_type == ctypes.c_int8 or base_type == ctypes.c_char:
        return bytes(data)
    if issubclass(base_type, ctypes.Array):
        return [array_to_list(v, show_us) for v in data]
    if issubclass(base_type, ctypes.Structure):
        return [struct_to_dict(v, show_us) for v in data]
    return data[:]


def is_us(k):
    if isinstance(k, str):
        return k[0] == '_'
    if isinstance(k, bytes):
        return k[0] == 95
    return False


def serialize_data(data, show_us=False):
    if hasattr(data, '_serialize_'):
        return data._serialize_()
    if isinstance(data, ctypes.Array):
        return array_to_list(data, show_us)
    if isinstance(data, ctypes.Structure):
        return struct_to_dict(data, show_us)
    if isinstance(data, list):
        return [serialize_data(d, show_us) for d in data]
    if isinstance(data, dict):
        return {
            k: serialize_data(v, show_us)
            for k, v in data.items()
            if show_us or not is_us(k)
        }
    if dataclasses.is_dataclass(data):
        return {
            k.name: serialize_data(getattr(data, k.name))
            for k in dataclasses.fields(data)
        }
    return data
