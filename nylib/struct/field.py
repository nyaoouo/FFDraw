import functools
import ctypes, _ctypes
import copy
from typing import TypeVar, Type, Generic, Any, Callable

_t = TypeVar('_t')


@functools.cache
def parse_type(type_):
    # if issubclass(type_, Enum): return type_, default_get, enum_set
    if issubclass(type_, _ctypes._SimpleCData): return type_, simple_c_get, simple_c_set
    if issubclass(type_, _ctypes.Array):
        if type_._type_ == ctypes.c_char or type_._type_ == ctypes.c_wchar: return type_, simple_c_get, simple_c_set
        return type_, default_get, array_set
    return type_, default_get, default_set


def default_get(type_, address): return type_.from_address(address)


def default_set(type_, address, val): ctypes.cast(address, ctypes.POINTER(type_))[0] = val


# def enum_set(type_, address, val):  type_._base_.from_address(address).value = val.value if isinstance(val, Enum) else val


def simple_c_get(type_, address): return type_.from_address(address).value


def simple_c_set(type_, address, val): type_.from_address(address).value = val


def array_set(type_, address, val): type_.from_address(address)[:len(val)] = val


class FieldBase(Generic[_t]):
    offset: int
    name: str

    def __get__(self, instance, owner) -> _t: ...

    def __set__(self, instance, owner) -> _t: ...

    def __add__(self, offset: int):
        new_f = copy.deepcopy(self)
        new_f.offset += offset
        return new_f

    def __set_name__(self, owner, name):
        self.name = name


class Field(FieldBase[_t]):
    _real_d_type = None
    _getter = None
    _setter = None

    def __init__(self, d_type: Type[_t] | str, offset: int | None = None, str_eval: Callable[[Any], Type] = None):
        self._d_type = d_type
        self.offset = offset
        self.str_eval = str_eval

    def __class_getitem__(cls, item):
        return cls(item)

    def init_type(self):
        self._real_d_type, self._getter, self._setter = res = parse_type(self.str_eval(self._d_type))
        return res

    d_type = property(lambda self: self.init_type()[0] if self._real_d_type is None else self._real_d_type)
    getter = property(lambda self: self.init_type()[1] if self._getter is None else self._getter)
    setter = property(lambda self: self.init_type()[2] if self._setter is None else self._setter)

    def __get__(self, instance, owner) -> _t:
        if instance is None: return self
        return self.getter(self.d_type, ctypes.addressof(instance) + self.offset)

    def __set__(self, instance, value: _t) -> None:
        if instance is None: return
        return self.setter(self.d_type, ctypes.addressof(instance) + self.offset, value)

    def __repr__(self):
        return f'<Field type={self._d_type}, ofs={self.offset}>'


def field(tp: Type[_t] | Any, offset=None) -> _t:
    return Field(tp, offset)


class BitField(FieldBase[int]):
    def __init__(self, offset=None, bit_offset=None, field_type=ctypes.c_ubyte, bit_size=1):
        self.offset = offset
        self.bit_offset = bit_offset
        self.bit_size = bit_size
        self.field_type = field_type
        self.mask = (1 << bit_size) - 1

    def __get__(self, instance, owner):
        if instance is None: return self
        return (self.field_type.from_address(
            ctypes.addressof(instance) + self.offset
        ).value >> self.bit_offset) & self.mask

    def __set__(self, instance, value):
        if instance is None: return self
        v = self.field_type.from_address(ctypes.addressof(instance) + self.offset)
        v.value = (v.value & ~(self.mask << self.bit_offset) )|(value << self.bit_offset)

    def __repr__(self):
        return f'<Field type={self.field_type.__name__}, ofs={self.offset}:{self.bit_offset}, bits={self.bit_size}>'


def bit_field(offset=None, bit_offset=None, field_type=ctypes.c_ubyte, bit_size=1) -> int:
    return BitField(offset, bit_offset, field_type, bit_size)
