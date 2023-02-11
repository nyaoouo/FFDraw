import typing

_T = typing.TypeVar('_T')


def missing(v): return classmethod(lambda cls, _: cls(v))


def auto_missing(e: typing.Type[_T]) -> typing.Type[_T]:
    *_, _e = e
    setattr(e, '_missing_', classmethod(lambda cls, _: _e))
    return e
