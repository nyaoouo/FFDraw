import dataclasses
import inspect
import typing

from .call_hook import BroadcastHook, BroadcastHookAsync
from .asyncio import to_async_func


class KeyRoute:
    hook_type = BroadcastHook
    route: typing.Dict[typing.Any, hook_type]

    def __init__(self, get_key=lambda v: v):
        self.get_key = get_key
        self.route = {}
        self.any_call = self.hook_type()
        self.default_call = self.hook_type()

    def __getitem__(self, item):
        if (hook := self.route.get(item)) is None:
            self.route[item] = hook = self.hook_type()
        return hook

    def hook(self, key, func=None):
        if func is None:
            return lambda _func: self.hook(key, _func)
        if func in (hook := self[key]):
            raise ValueError(f'{func.__name__} is already exists in this hook')
        hook.append(func)
        return KeyRouteItem(self, key=key, func=func)

    def unhook(self, key, _func):
        if hook := self.route.get(key):
            hook.remove(_func)

    def __call__(self, *args, **kwargs):
        self.any_call(*args, **kwargs)
        if hook := self.route.get(self.get_key(*args, **kwargs)):
            hook(*args, **kwargs)
        elif self.default_call:
            self.default_call(*args, **kwargs)

    def any(self, _func):
        if _func in self.any_call:
            raise ValueError(f'{_func.__name__} is already exists in any hook')
        self.any_call.append(_func)
        return KeyRouteItem(self, type=2, func=_func)

    def unhook_any(self, _func):
        self.any_call.remove(_func)

    def default(self, _func):
        if _func in self.default_call:
            raise ValueError(f'{_func.__name__} is already exists in default hook')
        self.default_call.append(_func)
        return KeyRouteItem(self, type=1, func=_func)

    def unhook_default(self, _func):
        self.default_call.remove(_func)


class KeyRouteAsync(KeyRoute):
    hook_type = BroadcastHookAsync

    def hook(self, key, func=None):
        return super().hook(key, (to_async_func(func) if func and not inspect.iscoroutinefunction(func) else func))

    def default(self, _func):
        return super().default(_func if inspect.iscoroutinefunction(_func) else to_async_func(_func))

    def any(self, _func):
        return super().any(_func if inspect.iscoroutinefunction(_func) else to_async_func(_func))

    async def __call__(self, *args, **kwargs):
        await self.any_call(*args, **kwargs)
        if hook := self.route.get(self.get_key(*args, **kwargs)):
            await hook(*args, **kwargs)
        elif self.default_call:
            await self.default_call(*args, **kwargs)


@dataclasses.dataclass
class KeyRouteItem:
    route: 'KeyRoute'
    func: typing.Callable
    key: typing.Any = None
    type: int = 0

    def hook(self):
        match self.type:
            case 1:
                self.route.default(self.func)
            case 2:
                self.route.any(self.func)
            case _:
                self.route.hook(self.key, self.func)

    def unhook(self):
        match self.type:
            case 1:
                self.route.unhook_default(self.func)
            case 2:
                self.route.unhook_any(self.func)
            case _:
                self.route.unhook(self.key, self.func)
