import collections
import dataclasses
import io
import typing
import enum
import struct
from fpt4.utils.sqpack import SqPack

T = typing.TypeVar('T')
BinaryHeader = collections.namedtuple('BinaryHeader', ('guid', 'size'))
BinaryHeaderStruct = struct.Struct('<II')

s_int8 = struct.Struct('<b')
s_uint8 = struct.Struct('<B')
s_int16 = struct.Struct('<h')
s_uint16 = struct.Struct('<H')
s_int32 = struct.Struct('<i')
s_uint32 = struct.Struct('<I')
s_float = struct.Struct('<f')

aligned4 = lambda v: (v + 0x3) & (~0x3)
aligned16 = lambda v: (v + 0xf) & (~0xf)


def enum_property(t: T, real_name) -> T:
    return property(
        lambda self: t(getattr(self, real_name)),
        lambda self, v: setattr(self, real_name, v.value if isinstance(v, enum.Enum) else v)
    )


def binary_header(buf, offset=0):
    guid, size = BinaryHeaderStruct.unpack_from(buf, offset)
    return BinaryHeader(struct.pack(b'>I', guid).lstrip(b'\0'), size)


def pack_binary_header(guid: bytes, data):
    l_data = len(data)
    pad_data = aligned4(l_data) - l_data
    return BinaryHeaderStruct.pack(int.from_bytes(guid, 'big'), l_data) + data + (b'\0' * pad_data)


class GuidTriggerProtocol(typing.Protocol):

    def load(self, instance: 'AVfxStruct', buf, off, size): ...

    def pack(self, instance: 'AVfxStruct') -> typing.Iterable[bytes]: ...


class KeyAttr(typing.Generic[T]):
    @classmethod
    def struct(
            cls,
            guid: bytes,
            default: typing.Type[T]
    ) -> T:
        return cls(guid, default.load, default.pack, None)

    @classmethod
    def make(
            cls,
            guid: bytes,
            loader: 'typing.Callable[[bytes, int, int], T]',
            packer: 'typing.Callable[[T], bytes]',
            default: T
    ) -> T:
        return cls(guid, loader, packer, default)

    def __init__(
            self,
            guid: bytes,
            loader: 'typing.Callable[[bytes, int, int], T]',
            packer: 'typing.Callable[[T], bytes]',
            default: T
    ):
        self.guid = guid
        self.name = None
        self.loader = loader
        self.packer = packer
        self.type = type(default)
        self.default = default

    def load(self, instance, buf, off, size):
        assert self.name, 'name is None'
        setattr(instance, '__is_name_set__' + self.name, 1)
        setattr(instance, self.name, self.loader(buf, off, size))

    def pack(self, instance):
        if getattr(instance, '__is_name_set__' + self.name, 0) == 1:
            yield pack_binary_header(self.guid, self.packer(getattr(instance, self.name)))

    def __get__(self, instance, owner):
        if instance is None: return self
        return self.default

    def __set_name__(self, owner, name):
        self.name = name
        if name.startswith('_'):
            owner._attr_list.append(name[1:])
        else:
            owner._attr_list.append(name)
        owner._guid_map[self.guid] = self

    @classmethod
    def simple(cls, guid, default: T, t) -> T:
        return cls(guid, lambda buf, off, size: t.unpack_from(buf, off)[0], lambda v: t.pack(v), default)

    @classmethod
    def bool(cls, guid, default: bool, t=s_int8) -> 'KeyAttr[bool]':
        return cls(guid, lambda buf, off, size: t.unpack_from(buf, off)[0] != 0, lambda v: t.pack(int(v)), default)

    @classmethod
    def string(cls, guid) -> 'KeyAttr[bytes]':
        return cls(guid, lambda buf, off, size: buf[off:off + size], lambda v: v, b'')


class KeyNativeList(typing.Generic[T]):
    @classmethod
    def make(cls, cnt_key: bytes, el_key: bytes, s: struct.Struct, dc: typing.Type[T], cnt_t=s_int32, ) -> typing.List[T]:
        return cls(cnt_key, el_key, s, dc, cnt_t)

    def __init__(self, cnt_key: bytes, el_key: bytes, s: struct.Struct, dc: typing.Type[T], cnt_t=s_int32):
        self.cnt_key = cnt_key
        self.el_key = el_key
        self.s = s
        self.dc = dc
        self.name = None
        self.cnt_t = cnt_t

    def __get__(self, instance, owner):
        if instance is None: return self
        setattr(instance, self.name, res := [])
        return res

    def __set_name__(self, owner, name):
        self.name = name

        def cnt_load(instance, buf, off, size):
            setattr(instance, "__nlist_attr_count__" + self.name, self.cnt_t.unpack_from(buf, off)[0])

        def cnt_pack(instance):
            yield from ()

        def el_load(instance, buf, off, size):
            setattr(instance, self.name, list(self.dc(*d) for d in self.s.iter_unpack(buf[off:off + size])))

        def el_pack(instance):
            data = getattr(instance, self.name, ())
            yield pack_binary_header(self.cnt_key, self.cnt_t.pack(len(data)))
            yield pack_binary_header(self.el_key, b''.join(self.s.pack(*dataclasses.astuple(el)) for el in data))

        owner._attr_list.append(name)
        owner._guid_map[self.cnt_key] = type(f'{name}_cnt', (), {'load': cnt_load, 'pack': cnt_pack, 'guid': self.cnt_key})
        owner._guid_map[self.el_key] = type(f'{name}_el', (), {'load': el_load, 'pack': el_pack, 'guid': self.el_key})


class KeyListAttr(typing.Generic[T]):
    @classmethod
    def struct(cls, cnt_key: bytes, el_key: bytes, t: typing.Type[T], cnt_t=s_int32, ) -> typing.List[T]:
        return cls(cnt_key, el_key, t.load, t.pack, cnt_t)

    @classmethod
    def make(
            cls,
            cnt_key: bytes,
            el_key: bytes,
            loader: 'typing.Callable[[bytes, int, int], T]',
            packer: 'typing.Callable[[T], bytes]',
            cnt_t=s_int32,
    ) -> typing.List[T]:
        return cls(cnt_key, el_key, loader, packer, cnt_t)

    def __init__(
            self,
            cnt_key: bytes,
            el_key: bytes,
            loader: 'typing.Callable[[bytes, int, int], T]',
            packer: 'typing.Callable[[T], bytes]',
            cnt_t=s_int32,
    ):
        self.cnt_key = cnt_key
        self.el_key = el_key
        self.loader = loader
        self.packer = packer
        self.name = None
        self.cnt_t = cnt_t

    def __get__(self, instance, owner) -> typing.Iterable[T]:
        return ()

    def __set_name__(self, owner, name):
        self.name = name

        def cnt_load(instance, buf, off, size):
            setattr(instance, "__list_attr_count__" + self.name, self.cnt_t.unpack_from(buf, off))
            setattr(instance, self.name, [])

        def cnt_pack(instance):
            yield from ()

        def el_load(instance, buf, off, size):
            if getattr(instance, "__list_attr_count__" + self.name, 0):
                getattr(instance, self.name).append(self.loader(buf, off, size))

        def el_pack(instance):
            data = getattr(instance, self.name, ())
            if isinstance(data, list):
                yield pack_binary_header(self.cnt_key, self.cnt_t.pack(len(data)))
                for el in data:
                    yield pack_binary_header(self.el_key, self.packer(el))

        owner._attr_list.append(name)
        owner._guid_map[self.cnt_key] = type(f'{name}_cnt', (), {'load': cnt_load, 'pack': cnt_pack, 'guid': self.cnt_key})
        owner._guid_map[self.el_key] = type(f'{name}_el', (), {'load': el_load, 'pack': el_pack, 'guid': self.el_key})


class AvfxMeta(type):
    def __getattr__(self, item):
        if item == '_guid_map':
            default = {}
        elif item == '_attr_list':
            default = []
        else:
            raise AttributeError
        if item in self.__dict__:
            return self.__dict__[item]
        setattr(self, item, default)
        return default


class AVfxStruct(metaclass=AvfxMeta):
    _guid_map: typing.Dict[bytes, GuidTriggerProtocol]
    _attr_list: typing.List[str]

    @classmethod
    def load(cls, buf, offset, data_size) -> 'AVfxStruct':
        data = cls()
        end_process = offset + data_size
        while offset < end_process:
            part_header = binary_header(buf, offset)
            offset += BinaryHeaderStruct.size
            if attr := cls._guid_map.get(part_header.guid):
                attr.load(data, buf, offset, part_header.size)
            else:
                print('unk guid', cls.__name__, offset, part_header.guid)
            offset += aligned4(part_header.size)
        return data

    def pack(self):
        with io.BytesIO() as buf:
            for giud, attr in self._guid_map.items():
                for _d in attr.pack(self):
                    size = len(_d)
                    buf.write(_d + b'\0' * (aligned4(size) - size))
            return buf.getvalue()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and all(getattr(self, a) == getattr(other, a) for a in self._attr_list)

    def _dif_(self, other):
        if type(self) != type(other):
            yield '_type_', self.__class__, type(other)
            return
        for a in self._attr_list:
            for p, v1, v2 in dif(getattr(self, a), getattr(other, a)):
                yield concat_path(a, p), v1, v2

    def _serialize_(self):
        return {a: serialize(getattr(self, a)) for a in self._attr_list}


def dumb_loader(buf, off, size): return buf[off:off + size]


def dumb_packer(v): return v


def concat_path(p, s): return str(p) if s is None else f'{p}.{s}'


def dif(a, b):
    if type(a) != type(a):
        yield '_type_', type(a), type(a)
        return
    elif hasattr(a, '_dif_'):
        for d in getattr(a, '_dif_')(b):
            yield d
    elif isinstance(a, list):
        if len(a) != len(b):
            yield '_size_', len(a), len(b)
            return
        for i, (v1, v2) in enumerate(zip(a, b)):
            for p, _v1, _v2 in dif(v1, v2):
                yield concat_path(i, p), _v1, _v2
    elif isinstance(a, dict):
        if not ((ak := set(a.keys())) - (bk := set(b.keys()))):
            yield '_keys', ak, bk
            return
        for k, v1 in a.items():
            for p, _v1, _v2 in dif(v1, b[k]):
                yield concat_path(k, p), _v1, _v2
    elif a != b:
        yield None, a, b


def serialize(data):
    if hasattr(data, '_serialize_'):
        return data._serialize_()
    if isinstance(data, list):
        return [serialize(el) for el in data]
    if isinstance(data, dict):
        return {k: serialize(v) for k, v in data.items()}
    return data


class DataClassImpl:
    def _dif_(self, other):
        if type(self) != type(other):
            yield '_type_', self.__class__, type(other)
            return
        for field in dataclasses.fields(self):
            a = field.name
            for p, v1, v2 in dif(getattr(self, a), getattr(other, a)):
                yield concat_path(a, p), v1, v2

    def _serialize_(self):
        return {field.name: serialize(getattr(self, field.name)) for field in dataclasses.fields(self)}
