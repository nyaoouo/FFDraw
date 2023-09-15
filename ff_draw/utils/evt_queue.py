import logging
import queue
import threading

import time


class EvtQueue:
    def __init__(self, cb, timeout_cb=None, cbexc_cb=None):
        self.cb = cb
        self.timeout_cb = timeout_cb
        self.cbexc_cb = cbexc_cb
        self.msg_queue = queue.Queue()
        self._msg_queue = queue.Queue()
        self._msg_evt = threading.Event()
        self.msg_loop_thread = threading.Thread(target=self.msg_loop, daemon=True)
        self.msg_loop_watcher_thread = threading.Thread(target=self.msg_loop_watcher, daemon=True)
        self.started = False

    def msg_loop_watcher(self):
        while True:
            args = self.msg_queue.get()
            self._msg_evt.clear()
            start_time = time.time()
            self._msg_queue.put(args)
            self._msg_evt.wait(.1)
            while not self._msg_evt.is_set():
                if self.timeout_cb:
                    self.timeout_cb(args, time.time() - start_time, self)
                self._msg_evt.wait(.5)

    def msg_loop(self):
        while True:
            args = self._msg_queue.get()
            try:
                self.cb(*args)
            except Exception as e:
                if self.cbexc_cb:
                    self.cbexc_cb(e, args)
                else:
                    logging.error(f'exception in cb, with {args=}', exc_info=e)
            self._msg_evt.set()

    def start(self):
        if not self.started:
            self.started = True
            self.msg_loop_thread.start()
            self.msg_loop_watcher_thread.start()

    def put(self, *args):
        self.start()
        self.msg_queue.put(args)
