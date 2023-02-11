import json
import threading
import time
import traceback
import socket
import types
import typing
import socketserver

from nylib.utils import Counter, ResEventList, AsyncEvtList

CLIENT_CALL = 0
CLIENT_SUBSCRIBE = 1
CLIENT_UNSUBSCRIBE = 2

SERVER_RETURN = 0
SERVER_EVENT = 1

RETURN_NORMAL = 0
RETURN_EXCEPTION = 1
RETURN_GENERATOR = 2
RETURN_GENERATOR_END = 3


class RpcHandler(socketserver.StreamRequestHandler):
    server: 'RpcServer'

    def __init__(self, request, client_address, server, client_id):
        self.client_id = client_id
        self.send_lock = threading.Lock()
        self.subscribed = set()
        super().__init__(request, client_address, server)

    def send(self, data):
        msg = json.dumps(data).encode('utf8') + b'\n'
        with self.send_lock: self.wfile.write(msg)

    def send_event(self, event_id, event):
        self.send({
            'cmd': SERVER_EVENT,
            'key': event_id,
            'data': event
        })

    def reply_call_normal(self, reply_id, res):
        self.send({
            'cmd': SERVER_RETURN,
            'reply_id': reply_id,
            'type': RETURN_NORMAL,
            'data': res
        })

    def reply_call_exc(self, reply_id, exc):
        self.send({
            'cmd': SERVER_RETURN,
            'reply_id': reply_id,
            'type': RETURN_EXCEPTION,
            'data': {
                'type': type(exc).__name__,
                'str': str(exc),
                'trace': traceback.format_exc(),
            },
        })

    def reply_call_gen(self, reply_id, gen):
        try:
            for res in gen:
                self.send({
                    'cmd': SERVER_RETURN,
                    'reply_id': reply_id,
                    'type': RETURN_GENERATOR,
                    'data': res,
                })
            self.send({
                'cmd': SERVER_RETURN,
                'reply_id': reply_id,
                'type': RETURN_GENERATOR_END,
            })
        except Exception as e:
            self.reply_call_exc(reply_id, e)

    def handle_call(self, reply_id, key, arg, kwargs):
        try:
            res = self.server.call_map[key](*arg, *kwargs)
        except Exception as e:
            self.reply_call_exc(reply_id, e)
        else:
            if isinstance(res, types.GeneratorType):
                self.reply_call_gen(reply_id, res)
            else:
                self.reply_call_normal(reply_id, res)

    def _process(self, data):
        cmd = data.get('cmd')
        if cmd == CLIENT_CALL:  # call
            self.handle_call(data.get('reply_id', -1), data.get('key'), data.get('args', []), data.get('kwargs', {}))
        elif cmd == CLIENT_SUBSCRIBE:  # subscribe
            if (key := data.get('key')) not in self.subscribed:
                self.subscribed.add(key)
                self.server.add_subscribe(key, self.client_id)
        elif cmd == CLIENT_UNSUBSCRIBE:  # unsubscribe
            if (key := data.get('key')) in self.subscribed:
                self.subscribed.remove(key)
                self.server.remove_subscribe(key, self.client_id)

    def process(self, line):
        try:
            self._process(json.loads(line))
        except Exception as e:
            self.reply_call_exc(-1, e)

    def handle(self):
        self.server.handlers[self.client_id] = self
        threads = []
        try:
            for _line in self.rfile:
                threads.append(t := threading.Thread(target=self.process, args=(_line,)))
                t.start()
        except ConnectionError:
            pass
        finally:
            for t in threads: t.join()
            self.server.handlers.pop(self.client_id, None)


class RpcServer(socketserver.ThreadingTCPServer):
    handlers: typing.Dict[int, 'RpcHandler']
    allow_reuse_address = True

    def __init__(self, server_address, call_map, **kwargs):
        super().__init__(server_address, RpcHandler, **kwargs)
        self.client_counter = Counter()
        self.subscribe_map = {}
        self.handlers = {}
        if isinstance(call_map, (tuple, list,)):
            call_map = {i.__name__: i for i in call_map}
        self.call_map = call_map
        self.serve_thread = threading.Thread(target=self.serve)

    def finish_request(self, request, client_address) -> None:
        self.RequestHandlerClass(request, client_address, self, self.client_counter.get())

    def push_event(self, key, event):
        if key not in self.subscribe_map: return
        if s := self.subscribe_map.get(key, set()):
            for client_id in s.copy():
                try:
                    client = self.handlers[client_id]
                except KeyError:
                    try:
                        s.remove(client_id)
                    except ValueError:
                        pass
                else:
                    client.send_event(key, event)

    def add_subscribe(self, key, cid):
        if not (s := self.subscribe_map.get(key)):
            self.subscribe_map[key] = s = set()
        s.add(cid)

    def remove_subscribe(self, key, cid):
        if s := self.subscribe_map.get(key):
            try:
                s.remove(cid)
            except KeyError:
                pass
            if not s:
                self.subscribe_map.pop(key, None)

    def send_all(self, s):
        for c in self.handlers.values():
            c.send(s)

    def serve(self):
        return self.serve_forever()


def empty_iterator():
    yield from ()


async def async_empty_iterator():
    return
    yield


class RpcClient(object):
    def __init__(self, address, retry=0, sleep_delay=1, on_end=None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start = False
        self.buffer_size = 1024 * 1024
        self.counter = Counter()
        self.reply_map = {}
        self.subscribe_map = {}

        class Rpc:
            def __getattr__(_self, item):
                def func(*_args, **_kwargs):
                    return self.remote_call(item, _args, _kwargs)

                func.__name__ = item
                return func

        class AsyncRpc:
            def __getattr__(_self, item):
                def func(*_args, **_kwargs):
                    return self.async_remote_call(item, _args, _kwargs)

                func.__name__ = item
                return func

        self.rpc = Rpc()
        self.async_rpc = AsyncRpc()
        self.serve_thread = threading.Thread(target=self.serve)
        self.on_end = on_end
        self.address = address
        self.retry = retry
        self.sleep_delay = sleep_delay
        self.is_connected = threading.Event()

    def close(self):
        self.sock.close()

    def connect(self):
        while True:
            try:
                self.sock.connect(self.address)
            except socket.error:
                if self.retry:
                    self.retry -= 1
                    time.sleep(self.sleep_delay)
                else:
                    raise
            else:
                self.is_connected.set()
                self.serve_thread.start()
                break

    def send(self, data):
        self.sock.send(json.dumps(data).encode('utf-8') + b'\n')

    def serve(self):
        buffer = bytearray()
        try:
            while True:
                buffer.extend(self.sock.recv(self.buffer_size))
                while True:
                    try:
                        idx = buffer.index(10)
                    except ValueError:
                        break
                    else:
                        threading.Thread(target=self.process, args=(buffer[:idx],)).start()
                        buffer = buffer[idx + 1:]
        except Exception as e:
            if self.on_end:
                self.on_end(e)
        finally:
            self.is_connected.clear()

    def process(self, line):
        data = json.loads(line)
        cmd = data.get('cmd')
        if cmd == SERVER_RETURN:
            if l := self.reply_map.get(data.get('reply_id', -1)):
                l.put((data.get('type'), data.get('data')))
        elif cmd == SERVER_EVENT:
            if s := self.subscribe_map.get(key := data.get('key'), set()):
                data = data.get('data')
                for c in s: c(key, data)
            else:
                self._remove_subscribe(key)

    def _remove_subscribe(self, key):
        self.subscribe_map.pop(key, None)
        self.send({
            'cmd': CLIENT_UNSUBSCRIBE,
            'key': key,
        })

    def subscribe(self, key, call):
        if key not in self.subscribe_map:
            self.subscribe_map[key] = set()
            self.send({
                'cmd': CLIENT_SUBSCRIBE,
                'key': key,
            })
        self.subscribe_map[key].add(call)

    def unsubscribe(self, key, call):
        s = self.subscribe_map.get(key, set())
        try:
            s.remove(call)
        except KeyError:
            pass
        if not s:
            self._remove_subscribe(key)

    def res_iterator(self, reply_id, evt_list, first_res):
        try:
            yield first_res
            while True:
                reply_type, res = evt_list.get()
                if reply_type == RETURN_EXCEPTION: raise set_exc(res)
                if reply_type == RETURN_GENERATOR_END: break
                yield res
        finally:
            self.reply_map.pop(reply_id, None)

    async def async_res_iterator(self, reply_id, evt_list, first_res):
        try:
            yield first_res
            while True:
                data = await evt_list.get()
                reply_type = data.get('type')
                if reply_type == RETURN_EXCEPTION: raise set_exc(data.get('data'))
                if reply_type == RETURN_GENERATOR_END: break
                yield data.get('data')
        finally:
            self.reply_map.pop(reply_id, None)

    def send_call(self, reply_id, key, args, kwargs):
        self.send({
            'cmd': CLIENT_CALL,
            'reply_id': reply_id,
            'key': key,
            'args': args,
            'kwargs': kwargs,
        })

    def remote_call(self, key, args, kwargs):
        if not self.is_connected.is_set():
            self.connect()
        reply_id = self.counter.get()
        self.reply_map[reply_id] = evt_list = ResEventList()
        self.send_call(reply_id, key, args, kwargs)
        reply_type, res = evt_list.get()
        if reply_type == RETURN_NORMAL:  # normal
            self.reply_map.pop(reply_id, None)
            return res
        if reply_type == RETURN_EXCEPTION:  # exc
            self.reply_map.pop(reply_id, None)
            raise set_exc(res)
        if reply_type == RETURN_GENERATOR:  # generator
            return self.res_iterator(reply_id, evt_list, res)
        if reply_type == RETURN_GENERATOR_END:  # end of generator
            self.reply_map.pop(reply_id, None)
            return empty_iterator()

    async def async_remote_call(self, key, args, kwargs):
        if not self.is_connected.is_set():
            self.connect()
        reply_id = self.counter.get()
        self.reply_map[reply_id] = evt_list = AsyncEvtList()
        self.send_call(reply_id, key, args, kwargs)
        reply_type, res = await evt_list.get()
        if reply_type == RETURN_NORMAL:  # normal
            self.reply_map.pop(reply_id, None)
            return res
        if reply_type == RETURN_EXCEPTION:  # exc
            self.reply_map.pop(reply_id, None)
            raise set_exc(res)
        if reply_type == RETURN_GENERATOR:  # generator
            return self.async_res_iterator(reply_id, evt_list, res)
        if reply_type == RETURN_GENERATOR_END:  # end of generator
            self.reply_map.pop(reply_id, None)
            return async_empty_iterator()


REMOTE_TRACE_KEY = '_remote_trace'


class RemoteException(Exception):pass


def format_exc(e):
    return getattr(e, REMOTE_TRACE_KEY, None) or traceback.format_exc()


def set_exc(data):
    if not data:return RemoteException()
    try:
        exc_t = eval(data.get('type'))
    except:
        exc_t = RemoteException
    setattr(e := exc_t(data.get('str')),REMOTE_TRACE_KEY,data.get('trace'))
    return e
