import ctypes
from nylib.hook import create_hook


class CommandHookConfig(ctypes.Structure):
    _fields_ = [
        ('prefix', ctypes.c_char * 0x10),
    ]


class CommandHook:
    def __init__(self, kwargs, cb):
        self.kwargs = kwargs
        self.cb = cb
        self.cfg = CommandHookConfig()
        self.hook = create_hook(
            self.kwargs['on_command'], ctypes.c_void_p,
            [ctypes.c_int64, ctypes.c_int, ctypes.c_int64, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int64]
        )(self.on_command).install_and_enable()

    def on_command(self, hook, a1, a2, a3, cmd_ptr, a5):
        inp = cmd_ptr[0]
        prefix = self.cfg.prefix
        if prefix:
            for c1, c2 in zip(inp, prefix):
                if c1 != c2: break
            else:
                return self.cb(inp[len(prefix):])
        hook.original(a1, a2, a3, cmd_ptr, a5)

    def uninstall(self):
        self.hook.uninstall()
