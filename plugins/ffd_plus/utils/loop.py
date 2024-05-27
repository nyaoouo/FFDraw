import logging
import threading
import time


class BasicUpdateLoop:
    thread: threading.Thread | None = None

    def __init__(self, interval=0.05):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.interval = interval
        self.calls = []
        self._work = False

    def add_call(self, func):
        self.calls.append(func)
        return self

    def remove_call(self, func):
        self.calls.remove(func)
        return self

    def safe_call(self, func):
        try:
            func()
        except Exception as e:
            self.logger.error(f'error in call {func.__name__}', exc_info=e)
            return e

    def work(self):
        while self._work:
            start = time.time()
            for call in self.calls.copy():
                if self.safe_call(call):
                    self.logger.warning(f'removing an error call')
                    try:
                        self.calls.remove(call)
                    except ValueError:
                        pass
            work_time = time.time() - start
            if (sleep_time := self.interval - work_time) > 0:
                time.sleep(sleep_time)
            else:
                self.logger.warning(f'work time {work_time:.4f} is longer then interval {self.interval:.4f}')

    def start(self):
        assert not (self.thread and self.thread.is_alive()), 'loop is already start'
        self._work = True
        self.thread = threading.Thread(target=self.work, daemon=True)
        self.thread.start()
        return self

    def close(self):
        assert self.thread and self.thread.is_alive(), 'loop is not alive'
        self._work = False
        self.thread.join()
        return self


class NULL: pass


def _parse_res(_res):
    res, exc = _res
    if exc is not None:
        raise exc
    return res


class AsyncCall:
    def __init__(self):
        self._threads = {}
        self._res = {}
        self._call_id = 0

    def is_finish(self, call_id):
        return call_id not in self._threads

    def pop_res(self, call_id, default=NULL):
        if default is NULL:
            del self._res[call_id]
            res = self._res[call_id]
        else:
            res = self._res.pop(call_id, (default, None))
        return _parse_res(res)

    def get_res(self, call_id, default=NULL):
        return _parse_res(self._res[call_id] if default is NULL else self._res.get(call_id, default))

    def _call(self, call_id, func, *args, **kwargs):
        try:
            self._res[call_id] = func(*args, **kwargs), None
        except Exception as e:
            self._res[call_id] = (None, e)
        finally:
            self._threads.pop(call_id, None)

    def call(self, func, *args, **kwargs):
        call_id = self._call_id
        self._call_id += 1
        self._threads[call_id] = t = threading.Thread(target=self._call, args=(call_id, func, *args), daemon=True, kwargs=kwargs)
        t.start()
        return call_id
