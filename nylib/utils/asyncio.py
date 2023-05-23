import asyncio
import inspect
import threading
from functools import wraps, partial
from .threading import terminate_thread


def to_async_func(func):
    if inspect.iscoroutinefunction(func):
        return func

    @wraps(func)
    async def run(*args, **kwargs):
        return await asyncio.get_event_loop().run_in_executor(None, partial(func, *args, **kwargs))

    return run


async def sub_thread_async(func, *args, _timeout: float | None = None, **kwargs):
    res = AsyncResEvent()

    def f():
        try:
            res.set(func(*args, **kwargs))
        except Exception as e:
            res.set_exception(e)
        except SystemExit:
            res.set_exception(TimeoutError)

    (t := threading.Thread(target=f)).start()
    try:
        return await res.wait(_timeout)
    except TimeoutError:
        raise TimeoutError
    finally:
        if not res.is_set():
            terminate_thread(t)


class AsyncResEvent(asyncio.Event):
    def __init__(self):
        super().__init__()
        self.res = None
        self.is_exc = False
        self._loop = asyncio.get_event_loop()
        self.is_waiting = False

    def set(self, data=None) -> None:
        assert not self.is_set()
        self.res = data
        self.is_exc = False
        self._loop.call_soon_threadsafe(super().set)

    def set_exception(self, exc) -> None:
        assert not self.is_set()
        self.res = exc
        self.is_exc = True
        self._loop.call_soon_threadsafe(super().set)

    async def wait(self, timeout: float | None = None):
        self.is_waiting = True
        try:
            await asyncio.wait_for(super().wait(), timeout)
            if self.is_exc:
                raise self.res
            else:
                return self.res
        finally:
            self.is_waiting = False


class AsyncEvtList:

    def __init__(self):
        self.queue = [AsyncResEvent()]

    def put(self, data):
        if not self.queue or self.queue[-1].is_set():
            self.queue.append(AsyncResEvent())
        self.queue[-1].set(data)

    async def get(self):
        if not self.queue:
            self.queue.append(AsyncResEvent())
        evt = self.queue[0]
        res = await evt.wait()
        if self.queue and self.queue[0] is evt:
            self.queue.pop(0)
        return res
