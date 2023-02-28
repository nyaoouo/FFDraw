import queue
import threading
import time
import typing

import win32api
import win32event
import win32file
import win32pipe
import winerror

if typing.TYPE_CHECKING:
    import pywintypes
    import pythoncom

active_pipe_handler = {}

class PipeHandlerBase:
    buf_size = 64 * 1024
    handle = None
    period = .001

    def __init__(self):
        self.serve_thread = threading.Thread(target=self.serve, daemon=False)
        self.work = False
        self.is_connected = threading.Event()
        self.read_overlapped = win32file.OVERLAPPED()
        self.read_overlapped.hEvent = win32event.CreateEvent(None, True, False, None)

    def send(self, s: str | bytes):
        win32file.WriteFile(self.handle, s.encode('utf-8') if isinstance(s, str) else s, win32file.OVERLAPPED())

    def _serve(self):
        tid = threading.get_ident()
        active_pipe_handler[tid] = self
        try:
            self.is_connected.set()
            self.work = True
            while self.work:
                err, buf = win32file.ReadFile(self.handle, self.buf_size, self.read_overlapped)
                num_read = win32file.GetOverlappedResult(self.handle, self.read_overlapped, True)
                self.on_data_received(buf[:num_read])
        finally:
            if active_pipe_handler[tid] is self:
                active_pipe_handler.pop(tid,None)

    def serve(self):
        try:
            self.on_connect()
            self._serve()
        except Exception as e:
            self.on_close(e)
        else:
            self.on_close(None)
        finally:
            try:
                win32file.CloseHandle(self.handle)
            except Exception:
                pass

    def close(self, block=True):
        self.work = False
        win32file.CloseHandle(self.handle)
        if block: self.serve_thread.join()

    def on_connect(self):
        pass

    def on_close(self, e: Exception | None):
        pass

    def on_data_received(self, data: bytes):
        pass


class PipeServerHandler(PipeHandlerBase):
    def __init__(self, server: 'PipeServer', handle, client_id):
        self.server = server
        self.handle = handle
        self.client_id = client_id
        self.buf_size = server.buf_size
        super().__init__()

    def serve(self):
        self.server.handlers[self.client_id] = self
        super().serve()
        self.server.handlers.pop(self.client_id, None)


_T = typing.TypeVar('_T', bound=PipeServerHandler)


class PipeServer(typing.Generic[_T]):
    handlers: typing.Dict[int, _T]

    def __init__(self, name, buf_size=64 * 1024, handler_class=PipeServerHandler):
        self.name = name
        self.buf_size = buf_size
        self.handler_class = handler_class
        self.serve_thread = threading.Thread(target=self.serve)
        self.client_counter = 0
        self.handlers = {}
        self.work = False

    def serve(self):
        self.work = True
        while self.work:
            handle = win32pipe.CreateNamedPipe(
                self.name,
                win32pipe.PIPE_ACCESS_DUPLEX | win32file.FILE_FLAG_OVERLAPPED,
                win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                win32pipe.PIPE_UNLIMITED_INSTANCES, self.buf_size, self.buf_size,
                0, None
            )
            win32pipe.ConnectNamedPipe(handle)
            self.handler_class(self, handle, self.client_counter).serve_thread.start()
            self.client_counter += 1

    def close(self):
        self.work = False

        while self.handlers:
            next_key = next(iter(self.handlers.keys()))
            self.handlers.pop(next_key).close(False)
        try:
            _FlushClient(self.name, timeout=1).serve()
        except TimeoutError:
            pass

    def send_all(self, s):
        for c in self.handlers.values():
            c.send(s)


class PipeClient(PipeHandlerBase):
    def __init__(self, name: str, buf_size=64 * 1024, timeout=0):
        self.name = name
        self.buf_size = buf_size
        self.timeout = timeout
        super().__init__()

    def _connect(self):
        start = time.perf_counter()
        while True:
            if self.timeout and time.perf_counter() - start > self.timeout:
                raise TimeoutError()
            try:
                self.handle = win32file.CreateFile(
                    self.name,
                    win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                    0,
                    None,
                    win32file.OPEN_EXISTING,
                    win32file.FILE_FLAG_OVERLAPPED,
                    None
                )
            except Exception as e:
                if e.winerror == winerror.ERROR_PIPE_BUSY:
                    time.sleep(1)
                    continue
                if e.winerror == winerror.ERROR_FILE_NOT_FOUND:
                    time.sleep(1)
                    continue
                raise
            else:
                break
        if win32pipe.SetNamedPipeHandleState(self.handle, win32pipe.PIPE_READMODE_MESSAGE, None, None):
            raise Exception(f"SetNamedPipeHandleState return code: {win32api.GetLastError()}")

    def serve(self):
        self._connect()
        super().serve()

    def connect(self):
        self.serve_thread.start()
        self.is_connected.wait()


class _FlushClient(PipeClient):
    def on_connect(self):
        self.close()
