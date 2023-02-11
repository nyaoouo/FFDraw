import ctypes


def auto() -> int: return globals()['Auto']()


class Auto: pass


class EnumType(type(ctypes.Structure)):

    def __new__(cls, name, bases, namespace):
        try:
            p = Enum in bases
        except NameError:
            p = False
        if p:
            name_to_value = {}
            value_to_name = {}
            default: str | None = None
            last_value = -1
            for k, v in list(namespace.items()):
                if isinstance(v, Auto):
                    namespace[k] = v = last_value + 1
                if isinstance(v, int):
                    name_to_value[k] = v
                    value_to_name.setdefault(v, k)
                    last_value = v
                    default = k

            default = namespace.setdefault('default', default)
            if isinstance(default, str):
                namespace['_default_name'] = default
                namespace['_default_value'] = name_to_value[default]
            else:
                namespace['_default_name'] = value_to_name[default]
                namespace['_default_value'] = default
            namespace['_fields_'] = [('_value', namespace.get('_base_', Enum._base_))]
            namespace['_name_to_value'] = name_to_value
            namespace['_value_to_name'] = value_to_name
        return super().__new__(cls, name, bases, namespace)


class Enum(ctypes.Structure, metaclass=EnumType):
    _base_ = ctypes.c_int
    default: str | int
    _default_name: str
    _default_value: int
    _name_to_value = {}
    _value_to_name = {}

    def __init__(self, value=None):
        super().__init__(_value=self._default_value if value is None else value)

    def __class_getitem__(cls, item: str):
        return cls(cls._name_to_value.get(item, cls._default_value))

    @classmethod
    def iter(cls):
        return cls._name_to_value.items()

    @property
    def value(self) -> int:
        return self._value

    @property
    def name(self) -> str:
        return self._value_to_name.get(self._value, self._default_name)

    @classmethod
    def get_name(cls, value: int) -> str:
        return cls._value_to_name.get(value, cls._default_name)

    @classmethod
    def get_value(cls, name: str) -> int:
        return cls._name_to_value.get(name, cls._default_value)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, str):
            return self.name == other
        else:
            return super().__eq__(other)
