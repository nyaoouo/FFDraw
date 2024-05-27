import typing
from nylib.utils import BroadcastHook, ResEvent
from ff_draw.mem import XivMem

from . import utils

if typing.TYPE_CHECKING:
    from .. import Api

_T = typing.TypeVar('_T')


class ProtoNoHolder:
    def __init__(self, worker: 'PktWorker', proto_nos):
        self.worker = worker
        self.proto_nos = proto_nos

    def __enter__(self): ...

    def __exit__(self, exc_type, exc_val, exc_tb): ...


class PktWorker:
    exists = False

    def __init__(self, work: 'PktWork'):
        self.work = work
        self.send = work.send

    def __enter__(self):
        assert not PktWorker.exists, "PktWorker already initialized"
        PktWorker.exists = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        PktWorker.exists = False

    def hold(self, *proto_no):
        return ProtoNoHolder(self, proto_no)


class ReplyListener(typing.Generic[_T]):
    res: ResEvent[_T]

    def __init__(self, reply_route: typing.Iterable[BroadcastHook] | BroadcastHook, filter_func=None):
        self.reply_route = reply_route if reply_route.__class__ in (list,tuple) else (reply_route, )
        self.filter_func = filter_func or (lambda *args, **kwargs: True)
        self.res = ResEvent()
        self.is_installed = False
        self.install()

    def listen(self, msg):
        if self.filter_func(msg):
            self.res.set(msg)
            self.uninstall()

    def install(self):
        if self.is_installed: return
        for r in self.reply_route:
            r.append(self.listen)
        self.is_installed = True

    def uninstall(self):
        if not self.is_installed: return
        for r in self.reply_route:
            try:
                r.remove(self.listen)
            except ValueError:
                pass
        self.is_installed = False

    def wait(self, timeout: float | None = None) -> _T:
        if not self.is_installed: raise RuntimeError("Listener not installed")
        try:
            return self.res.wait(timeout=timeout)
        finally:
            self.uninstall()


class PktWork:
    def __init__(self, is_zone):
        self.is_zone = is_zone
        self.cached_black_proto_no = None
        self._block_pno_shell = utils.add_black_proto_shell(is_zone)
        self._unblock_pno_shell = utils.remove_black_proto_shell(is_zone)
        self._get_pno_shell = utils.get_black_proto_shell(is_zone)
        if is_zone:
            self._sender = utils.send_zone_packet
        else:
            self._sender = utils.send_chat_packet

    def block_proto_no(self, *proto_no):
        self.cached_black_proto_no = XivMem.instance.inject_handle.run(self._block_pno_shell, proto_no)

    def unblock_proto_no(self, *proto_no):
        self.cached_black_proto_no = XivMem.instance.inject_handle.run(self._unblock_pno_shell, proto_no)

    @property
    def blocked_proto_no(self):
        if self.cached_black_proto_no is None:
            self.cached_black_proto_no = XivMem.instance.inject_handle.run(self._get_pno_shell)
        return self.cached_black_proto_no

    def send(self, *data: bytes, route: typing.Iterable[BroadcastHook] | BroadcastHook = None, filter=None, wait=5., immediate=False):
        if route is None:
            return self._sender(*data, immediate=immediate)
        listener = ReplyListener(route, filter)
        self._sender(*data, immediate=immediate)
        return listener.wait(wait)


class PktWorks:
    instance: 'PktWorks' = None

    def __init__(self, api: 'Api'):
        assert PktWorks.instance is None, "PktWorks already initialized"
        PktWorks.instance = self
        self.api = api
        self.zone = PktWork(True)
        self.chat = PktWork(False)
