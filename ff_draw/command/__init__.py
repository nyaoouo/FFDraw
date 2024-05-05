import logging
import pathlib
import shlex
import sys
import traceback
import typing

import imgui

from nylib.utils import imgui as ny_imgui, KeyRoute
import nylib.utils.win32.memory as ny_mem
from ..utils import EvtQueue
from .script import Script

if typing.TYPE_CHECKING:
    from ..main import FFDraw


def make_shell(key='#__commands__'):
    f = pathlib.Path(__file__).parent / 'shell.py'
    return f.read_text('utf-8') + f'''
def _install():
    if hasattr(inject_server, {key!r}):
        return ctypes.addressof(getattr(inject_server, {key!r}).cfg)
        getattr(inject_server, {key!r}).uninstall()
        delattr(inject_server, {key!r})
    hook = CommandHook(args[0], lambda inp: inject_server.push_event('command_inp', (inp, )))
    setattr(inject_server, {key!r}, hook)
    return ctypes.addressof(hook.cfg)
__file__ = {str(f)!r}\n
res = _install()
''', str(f)


class Command:
    logger = logging.getLogger('command')

    def __init__(self, main: 'FFDraw'):
        self.main = main
        self.handle = main.mem.handle
        self.handle = main.mem.handle
        shell, script_file = make_shell()
        main.mem.inject_handle.client.subscribe('command_inp', self._on_command_inp)
        self.p_cfg = main.mem.inject_handle.run(shell, {
            'on_command': main.mem.scanner_v2.find_address("40 ? 53 57 41 ? 41 ? 41 ? 48 ? ? ? ? 48 ? ? ? ? ? ? 48 ? ? ? ? ? ? 48 ? ? 48 89 45 ? 65")
        }, filename=script_file)
        self.data = self.main.config.setdefault('command', {})
        self.prefix = self.data.setdefault('prefix', '/#')
        self.on_command = KeyRoute(lambda cmd, args: cmd)
        self.evt_queue = EvtQueue(self.on_command, )
        self.on_command['script'].append(lambda _, args: Script(self, args[0]).run(args[1:]) if len(args) else None)

    @property
    def prefix(self):
        return ny_mem.read_string(self.handle, self.p_cfg, 0x10)

    @prefix.setter
    def prefix(self, value):
        if isinstance(value, str): value = value.encode('utf-8')
        assert len(value) < 0x10, 'prefix too long'
        ny_mem.write_bytes(self.handle, self.p_cfg, value)
        self.data['prefix'] = value.decode('utf-8')
        self.main.save_config()

    def _on_evt_queue_timeout(self, args, time_, q):
        cmd, args = args
        try:
            self.logger.warning(f'parse cmd {cmd=} {args=} run for {time_:.3f}s, for blocking event, please use async method\n' + ''.join(
                traceback.format_stack(sys._current_frames()[self.evt_queue.msg_loop_thread.ident])[10:]
            ))
        except Exception as e:
            self.logger.warning(f'exception when get overtime stack', exc_info=e)

    def _on_command_inp(self, _, args):
        inp, = args
        cmd, *args = shlex.split(inp.decode('utf-8', 'ignore'))
        self.evt_queue.put(cmd, args)
