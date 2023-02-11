from typing import Type, TypeVar
from .simple import safe

_T = TypeVar('_T')


class Matcher:
    def __init__(self, _checker=None, **kwargs):
        self.checker = _checker
        self.things = list(kwargs.items())

    def match(self, t): return safe(all, (
        v == getattr(t, k) for k, v in self.things
    ), _handle=AttributeError, _default=False) and (self.checker is None or self.checker(t))

    def __eq__(self, other): return self.match(other)

    def __class_getitem__(cls, item: Type): return lambda **kwargs: MatcherCheckInstance(item, **kwargs)

    def filter(self, iterable): return filter(self.match, iterable)


class MatcherCheckInstance(Matcher):
    def __init__(self, class_: Type, **kwargs):
        self.class_ = class_
        super().__init__(**kwargs)

    def match(self, t): return isinstance(t, self.class_) and super().match(t)


class DictMatcher(Matcher):
    def match(self, t): return isinstance(t, dict) and safe(all, (
        k in t and v == t.get(k) for k, v in self.things
    ), _handle=AttributeError, _default=False) and (self.checker is None or self.checker(t))
