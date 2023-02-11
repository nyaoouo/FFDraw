class ChainHook(list):
    class HookCall:
        def __init__(self, stack: list, func):
            self.stack = stack
            self.func = func

        def __call__(self, *args, **kwargs):
            if self.stack:
                return self.stack.pop()(self if self.stack else self.func, *args, **kwargs)
            elif self.func:
                return self.func(*args, **kwargs)

    def __init__(self, func=None):
        self.func = func
        super().__init__()

    def __call__(self, *args, **kwargs):
        if self:
            return self.HookCall(self.copy(), self.func)(*args, **kwargs)
        elif self.func:
            return self.func(*args, **kwargs)

    def remove(self, __value) -> bool:
        try:
            super().remove(__value)
        except ValueError:
            return False
        else:
            return True


class ChainHookAsync(ChainHook):
    class HookCall(ChainHook.HookCall):
        async def __call__(self, *args, **kwargs):
            if self.stack:
                return await self.stack.pop()(self if self.stack else self.func, *args, **kwargs)
            elif self.func:
                return await self.func(*args, **kwargs)

    async def __call__(self, *args, **kwargs):
        if self:
            return await self.HookCall(self.copy(), self.func)(*args, **kwargs)
        elif self.func:
            return await self.func(*args, **kwargs)


class BroadcastHook(list):
    def __call__(self, *args, **kwargs):
        return [f(*args, **kwargs) for f in self]

    def remove(self, __value) -> bool:
        try:
            super().remove(__value)
        except ValueError:
            return False
        else:
            return True


class BroadcastHookAsync(BroadcastHook):
    async def __call__(self, *args, **kwargs):
        return [await f(*args, **kwargs) for f in self]
