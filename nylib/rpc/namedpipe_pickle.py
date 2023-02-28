import logging
import pickle
import threading
import traceback
import types
import typing

from nylib.name_pipe.win32 import PipeServer, PipeServerHandler, PipeClient
from nylib.utils import ResEventList, Counter, AsyncEvtList

CLIENT_CALL = 0
CLIENT_SUBSCRIBE = 1
CLIENT_UNSUBSCRIBE = 2

SERVER_RETURN = 0
SERVER_EVENT = 1

RETURN_NORMAL = 0
RETURN_EXCEPTION = 1
RETURN_GENERATOR = 2
RETURN_GENERATOR_END = 3

REMOTE_TRACE_KEY = '_remote_trace'


class RpcHandler(PipeServerHandler):
    server: 'RpcServer'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscribed = set()

    def on_data_received(self, data: bytes):
        cmd, *arg = pickle.loads(data)
        if cmd == CLIENT_CALL:  # call
            threading.Thread(target=self.handle_call, args=arg).start()
        elif cmd == CLIENT_SUBSCRIBE:  # subscribe
            key, = arg
            if key not in self.subscribed:
                self.subscribed.add(key)
                self.server.add_subscribe(key, self.client_id)
        elif cmd == CLIENT_UNSUBSCRIBE:  # unsubscribe
            key, = arg
            if key in self.subscribed:
                self.subscribed.remove(key)
                self.server.remove_subscribe(key, self.client_id)

    def on_close(self, e: Exception | None):
        for k in self.subscribed:
            self.server.remove_subscribe(k, self.client_id)

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

    def reply_call_normal(self, reply_id, res):
        self.send(pickle.dumps((SERVER_RETURN, reply_id, RETURN_NORMAL, res)))

    def reply_call_exc(self, reply_id, exc):
        self.send(pickle.dumps((SERVER_RETURN, reply_id, RETURN_EXCEPTION, (exc, traceback.format_exc()))))

    def reply_call_gen(self, reply_id, gen):
        try:
            for res in gen:
                self.send(pickle.dumps((SERVER_RETURN, reply_id, RETURN_GENERATOR, res)))
            self.send(pickle.dumps((SERVER_RETURN, reply_id, RETURN_GENERATOR_END, None)))
        except Exception as e:
            self.reply_call_exc(reply_id, e)

    def send_event(self, event_id, event):
        self.send(pickle.dumps((SERVER_EVENT, event_id, event)))


class RpcServer(PipeServer[RpcHandler]):

    def __init__(self, name, call_map, *args, **kwargs):
        super().__init__(name, *args, handler_class=RpcHandler, **kwargs)
        self.subscribe_map = {}
        if isinstance(call_map, (tuple, list,)):
            call_map = {i.__name__: i for i in call_map}
        self.call_map = call_map

    def push_event(self, event_id, data):
        cids = self.subscribe_map.get(event_id, set())
        for cid in list(cids):
            if client := self.handlers.get(cid):
                client.send_event(event_id, data)
            else:
                try:
                    cids.remove(cid)
                except KeyError:
                    pass

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


def empty_iterator():
    yield from ()


async def async_empty_iterator():
    return
    yield


class RpcClient(PipeClient):
    reply_map: typing.Dict[int, ResEventList | AsyncEvtList]
    logger = logging.getLogger('RpcClient')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reply_map = {}
        self.subscribe_map = {}
        self.counter = Counter()

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

    def on_data_received(self, data: bytes):
        cmd, *args = pickle.loads(data)
        if cmd == SERVER_RETURN:
            reply_id, reply_type, res = args
            if l := self.reply_map.get(reply_id):
                l.put((reply_type, res))
        elif cmd == SERVER_EVENT:
            key, data = args
            s = self.subscribe_map.get(key, set())
            if s:
                for c in s:
                    try:
                        c(key, data)
                    except Exception as e:
                        self.logger.error(f'error in rpc client [{self.name}] event',exc_info=e)
            else:
                self.send(pickle.dumps((CLIENT_UNSUBSCRIBE, key)))

    def subscribe(self, key, call):
        if key not in self.subscribe_map:
            self.subscribe_map[key] = set()
            self.send(pickle.dumps((CLIENT_SUBSCRIBE, key)))
        self.subscribe_map[key].add(call)

    def unsubscribe(self, key, call):
        s = self.subscribe_map.get(key, set())
        try:
            s.remove(call)
        except KeyError:
            pass
        if not s:
            self.subscribe_map.pop(key, None)
            self.send(pickle.dumps((CLIENT_UNSUBSCRIBE, key)))

    def res_iterator(self, reply_id, evt_list, first_res):
        try:
            yield first_res
            while True:
                reply_type, res = evt_list.get()
                if reply_type == RETURN_EXCEPTION: raise set_exc(*res)
                if reply_type == RETURN_GENERATOR_END: break
                yield res
        finally:
            self.reply_map.pop(reply_id, None)

    async def async_res_iterator(self, reply_id, evt_list, first_res):
        try:
            yield first_res
            while True:
                reply_type, res = await evt_list.get()
                if reply_type == RETURN_EXCEPTION: raise set_exc(*res)
                if reply_type == RETURN_GENERATOR_END: break
                yield res
        finally:
            self.reply_map.pop(reply_id, None)

    def remote_call(self, key, args, kwargs):
        if not self.is_connected.is_set():
            self.connect()
        reply_id = self.counter.get()
        self.reply_map[reply_id] = evt_list = ResEventList()
        self.send(pickle.dumps((CLIENT_CALL, reply_id, key, args, kwargs)))
        reply_type, res = evt_list.get()
        if reply_type == RETURN_NORMAL:  # normal
            self.reply_map.pop(reply_id, None)
            return res
        if reply_type == RETURN_EXCEPTION:  # exc
            self.reply_map.pop(reply_id, None)
            raise set_exc(*res)
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
        self.send(pickle.dumps((CLIENT_CALL, reply_id, key, args, kwargs)))
        reply_type, res = await evt_list.get()
        if reply_type == RETURN_NORMAL:  # normal
            self.reply_map.pop(reply_id, None)
            return res
        if reply_type == RETURN_EXCEPTION:  # exc
            self.reply_map.pop(reply_id, None)
            raise set_exc(*res)
        if reply_type == RETURN_GENERATOR:  # generator
            return self.async_res_iterator(reply_id, evt_list, res)
        if reply_type == RETURN_GENERATOR_END:  # end of generator
            self.reply_map.pop(reply_id, None)
            return async_empty_iterator()


def format_exc(e):
    return getattr(e, REMOTE_TRACE_KEY, None) or traceback.format_exc()


def set_exc(e, tb):
    setattr(e, REMOTE_TRACE_KEY, tb)
    return e
