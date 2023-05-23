import threading
import typing
import ctypes


def terminate_thread(t: threading.Thread, exc_type=SystemExit):
    if not t.is_alive(): return
    try:
        tid = next(tid for tid, tobj in threading._active.items() if tobj is t)
    except StopIteration:
        raise ValueError("tid not found")
    if ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type)) != 1:
        raise SystemError("PyThreadState_SetAsyncExc failed")


class ResEvent(threading.Event):
    def __init__(self):
        super().__init__()
        self.res = None
        self.is_exc = False
        self.is_waiting = False

    def set(self, data=None) -> None:
        assert not self.is_set()
        self.res = data
        self.is_exc = False
        super().set()

    def set_exception(self, exc) -> None:
        assert not self.is_set()
        self.res = exc
        self.is_exc = True
        super().set()

    def wait(self, timeout: float | None = None) -> typing.Any:
        self.is_waiting = True
        try:
            if super().wait(timeout):
                if self.is_exc:
                    raise self.res
                else:
                    return self.res
            else:
                raise TimeoutError()
        finally:
            self.is_waiting = False


class ResEventList:
    queue: typing.List[ResEvent]

    def __init__(self):
        self.queue = [ResEvent()]
        self.lock = threading.Lock()

    def put(self, data):
        with self.lock:
            if not self.queue or self.queue[-1].is_set():
                self.queue.append(ResEvent())
            self.queue[-1].set(data)

    def get(self):
        with self.lock:
            if not self.queue:
                self.queue.append(ResEvent())
            evt = self.queue[0]
        res = evt.wait()
        with self.lock:
            if self.queue and self.queue[0] is evt:
                self.queue.pop(0)
        return res
