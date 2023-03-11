import logging
import os
import pathlib
import shutil
import sys
import threading
import time

from nylib.utils import Mutex, wait_until
from nylib.rpc.namedpipe_pickle import RpcClient
from nylib.utils.win32 import injection, process


class Handle:
    logger = logging.getLogger('InjectHandler')

    def __init__(self, pid, process_handle):
        self.pid = pid
        self.process_handle = process_handle
        self.pipe_name = r'\\.\\pipe\\NyLibInjectPipe-pid-' + str(pid)
        tmp_dir = pathlib.Path(os.environ['TEMP'])
        self.exc_file = tmp_dir / f'NyLibInjectErr{self.pid}-{time.time()}.txt'
        self.lock_file = Mutex(tmp_dir / f'NyLibInjectLock-{pid}.lck')
        self.client = RpcClient(self.pipe_name)
        self.is_starting_server = False
        self.paths = []

    def is_active(self):
        return self.lock_file.is_lock()

    def is_python_load(self):
        return process.get_module_by_name(self.process_handle, injection.python_dll_name) is not None

    def start_server(self):
        assert not self.is_active()
        self.is_starting_server = True
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
import traceback
import ctypes
try:
    import sys
    for _p in {repr(sys.path + self.paths)}:
        if _p not in sys.path:
            sys.path.append(_p)
    run_rpc_server_main({repr(str(self.lock_file.name))}, {repr(self.pipe_name)})
except Exception:
    # ctypes.windll.user32.MessageBoxW(0, 'error:\\n'+traceback.format_exc() ,'error' , 0x40010)
    with open({repr(str(self.exc_file))},'w',encoding='utf-8') as f:
        f.write(traceback.format_exc())
'''
        # compile(shell_code, 's', 'exec')
        res = injection.exec_shell_code(self.process_handle, shell_code.encode('utf-8'), True)
        if self.exc_file.exists():
            self.logger.error('error occurred in injection:\n' + self.exc_file.read_text('utf-8'))
            self.exc_file.unlink(missing_ok=True)
        elif res != 0:
            self.logger.warning(f'server fail, res:{res:x}')
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

    def add_path(self, path):
        if self.is_active():
            p = repr(str(path))
            self.run(f'''
import sys
if {p} not in sys.path:
    sys.path.append({p})
''')
        else:
            self.paths.append(str(path))
        return self

    def run(self, code, res_key='res'):
        self.wait_inject()
        return self.client.rpc.run(code, res_key)


def pywin32_dll_place():
    dll_suffix = f"{sys.version_info.major}{sys.version_info.minor}.dll"
    target_dir = pathlib.Path(os.environ['SystemDrive'] + os.sep) / 'Windows' / 'System32'
    for prefix in ('pythoncom', 'pywintypes'):
        dll_name = prefix + dll_suffix
        target_path = target_dir / dll_name
        if target_path.exists(): continue
        for p in sys.path:
            if (source_path := pathlib.Path(p) / dll_name).exists() or (source_path := pathlib.Path(p) / 'pywin32_system32' / dll_name).exists():
                break
        else:
            logging.warning(f'can find {dll_name} in paths:\n' + '\n'.join(sys.path))
            raise Exception(f'Cant find dll {dll_name}')
        shutil.copy(source_path, target_path)
        logging.debug(f'place {source_path} => {target_path}')


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
    print(Handle(pid, p_handle).run('import os;res=os.getpid()'))


if __name__ == '__main__':
    test()
