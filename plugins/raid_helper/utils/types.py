import threading
import time


class CallOnce:
    def __init__(self, func, elp_sec=1):
        self.func = func
        self.last_call = 0
        self.elp_sec = elp_sec
        self.lock = threading.Lock()

    def __call__(self, *args):
        with self.lock:
            current = time.time()
            if current - self.elp_sec < self.last_call: return
            self.last_call = current
        return self.func(*args)


def call_once(elp_sec=1):
    return lambda f: DelayCallOnce(f, elp_sec)


class DelayCallOnce:
    def __init__(self, func, delay_sec):
        self.args = []
        self.thread = None
        self.lock = threading.Lock()
        self.func = func
        self.delay_sec = delay_sec

    def __call__(self, *args):
        with self.lock:
            self.args.append(args)
            if self.thread is None:
                self.thread = threading.Thread(target=self.run, daemon=True)
                self.thread.start()

    def run(self):
        time.sleep(self.delay_sec)
        with self.lock:
            args = self.args.copy()
            self.args.clear()
            self.thread = None
        self.func(args)


def delay_call_once(delay_sec: float | int = 1):
    return lambda f: DelayCallOnce(f, delay_sec)


class TimeList(list):
    def __init__(self, *args, **kwargs):
        self._last_save = 0
        self._safe_time = kwargs.pop('safe_time', 1)
        self._lock = threading.Lock()
        super().__init__(*args, **kwargs)

    def append(self, __object) -> None:
        with self._lock:
            current = time.time()
            if self._last_save + self._safe_time < current: self.clear()
            self._last_save = current
            super().append(__object)


class TimeSet(set):
    def __init__(self, *args, **kwargs):
        self._last_save = 0
        self._safe_time = kwargs.pop('safe_time', 1)
        self._lock = threading.Lock()
        super().__init__(*args, **kwargs)

    def add(self, element) -> None:
        with self._lock:
            current = time.time()
            if self._last_save + self._safe_time < current: self.clear()
            self._last_save = current
            super().add(element)


class TimeCounter:
    def __init__(self, start_v=0, safe_time=1):
        self._last_save = 0
        self._safe_time = safe_time
        self._lock = threading.Lock()
        self.start_v = start_v - 1
        self.v = self.start_v

    def get(self) -> int:
        with self._lock:
            current = time.time()
            if self._last_save + self._safe_time < current:
                self.v = self.start_v
            self._last_save = current
            self.v += 1
            return self.v
