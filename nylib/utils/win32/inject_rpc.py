import logging
import os
import pathlib
import sys
import threading
import time

from nylib.utils import Mutex, wait_until, ResEvent
from nylib.rpc.namedpipe_pickle import RpcClient
from nylib.utils.win32 import injection, process


class Handle:
    logger = logging.getLogger('InjectHandler')
    res_events: dict[int, ResEvent]

    def __init__(self, pid, process_handle):
        self.pid = pid
        self.process_handle = process_handle
        self.pipe_name = r'\\.\\pipe\\NyLibInjectPipe-pid-' + str(pid)
        tmp_dir = pathlib.Path(os.environ['TEMP'])
        self.exc_dir = tmp_dir / f'NyLibInjectErr{self.pid}.txt'
        self.lock_file = Mutex(tmp_dir / f'NyLibInjectLock-{pid}.lck')
        self.client = RpcClient(self.pipe_name)
        self.is_starting_server = False
        self.res_events = {}

    def is_active(self):
        return self.lock_file.is_lock()

    def is_python_load(self):
        return process.get_module_by_name(self.process_handle, injection.python_dll_name) is not None

    def start_server(self):
        assert not self.is_active()
        self.is_starting_server = True
        start_at = time.time()
        exc_file = (self.exc_dir / f'err_{self.pid}_{time.time()}.log').absolute()
        shell_code = f'''
def run_rpc_server_main(lock_name, pipe_name):
    import threading
    from nylib.utils import Mutex, Counter
    from nylib.rpc.namedpipe_pickle import RpcServer
    res_id_counter = Counter()

    def run_call(code, res_key='res'):
        exec(code, namespace := {{'inject_server': server}})
        return namespace.get(res_key)

    server = RpcServer(pipe_name, {{"run": run_call}})
    with Mutex(lock_name):
        server.serve()
try:
    import sys
    for _p in {repr(sys.path)}:
        if _p not in sys.path:
            sys.path.append(_p)
    run_rpc_server_main({repr(str(self.lock_file.name))}, {repr(self.pipe_name)})
except Exception:
    import traceback
    with open({repr(str(exc_file))}, 'w', encoding='utf-8') as f:
        f.write(traceback.format_exc())
'''
        # compile(shell_code, 's', 'exec')
        injection.exec_shell_code(self.process_handle, shell_code.encode('utf-8'), True)
        if exc_file.exists():
            self.logger.error('error occurred in injection:\n' + exc_file.read_text('utf-8'))
        elif (rt := time.time() - start_at) < 5:
            self.logger.warning(f'server end in {rt:.2f}s, maybe error?')
        else:
            self.logger.debug(f'server end in {rt:.2f}s')
        self.is_starting_server = False

    def wait_inject(self):
        if not self.is_active():
            self.logger.debug(f"python base {injection.get_python_base_address(self.process_handle, True):#x}")
            if not self.is_starting_server:
                threading.Thread(target=self.start_server, daemon=True).start()
            time.sleep(.1)
            wait_until(self.is_active)
        if not self.client.is_connected.is_set():
            self.client.connect()

    def on_run_res(self, _, args):
        rid, is_success, data = args
        if res := self.res_events.pop(rid, None):
            if is_success:
                res.set(data)
            else:
                res.set_exception(data)

    def run(self, code, res_key='res'):
        self.wait_inject()
        return self.client.rpc.run(code, res_key)


def clean_locks(p: pathlib.Path):
    for f in p.glob('lock-*.lck'):
        try:
            f.unlink()
        except PermissionError:
            pass


def test():
    from nylib.utils.win32 import process
    process.enable_privilege()
    p_handle = process.open_process(pid := next(process.pid_by_executable(b'ffxiv_dx11.exe')))
    d = pathlib.Path('.test_injection').absolute()
    d.mkdir(exist_ok=True, parents=True)
    clean_locks(d)
    print(Handle(pid, p_handle).run('import os;res=os.getpid()'))


if __name__ == '__main__':
    test()
