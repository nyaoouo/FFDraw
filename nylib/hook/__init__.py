from ctypes import *
from typing import Annotated, Callable, List, Optional, Iterable, Type
from . import easy_hook


class EasyHookException(Exception):
    def __init__(self):
        self.code = easy_hook.rtl_get_last_error()
        self.err_msg = easy_hook.rtl_get_last_error_string()

    def __str__(self):
        return f"EasyHookException {self.code:#X}:{self.err_msg}"


def default_orig(*args): return args


class Hook(object):

    def __init__(self, at: int, hook_func: Callable, restype: Type = c_void_p, argtypes: Iterable[Type] = ()):
        """
        创建一个 hook， 注意需要手动调用 install() 以及 enable()

        :param at: 该函数的内存地址
        :param hook_func: 钩子函数
        :param restype: 返回类型
        :param argtypes: 参数类型（列表）
        """
        self.at = at
        self.interface = CFUNCTYPE(restype, *argtypes)
        self.hook_func = hook_func

        self._enabled = False
        self._installed = False
        self.hook_info = easy_hook.HOOK_TRACE_INFO()
        self._hook_function = self.interface(lambda *args: self.hook_func(self, *args))
        self.call = self.interface(at)

        self.original = None
        self.ACL_entries = (c_ulong * 1)(1)

    def install(self) :
        """
        安装hook到内存中
        """

        if self._installed: return
        if easy_hook.lh_install_hook(self.at, self._hook_function, None, byref(self.hook_info)):
            raise EasyHookException()
        self._installed = True

        original_func_p = c_void_p()
        if easy_hook.lh_get_bypass_address(byref(self.hook_info), byref(original_func_p)):
            raise EasyHookException()
        self.original = self.interface(original_func_p.value)
        return self

    def uninstall(self):
        """
        uninstall the hook
        """
        if not self._installed: return
        easy_hook.lh_uninstall_hook(byref(self.hook_info))
        easy_hook.lh_wait_for_pending_removals()
        self._installed = False
        return self

    def enable(self):
        """
        enable the hook
        """
        if not self._installed: return
        if easy_hook.lh_set_exclusive_acl(byref(self.ACL_entries), 1, byref(self.hook_info)):
            raise EasyHookException()
        self._enabled = True
        return self

    def disable(self):
        """
        disable the hook
        """
        if not self._installed: return
        if easy_hook.lh_set_inclusive_acl(byref(self.ACL_entries), 1, byref(self.hook_info)):
            raise EasyHookException()
        self._enabled = False
        return self

    def install_and_enable(self):
        return self.install().enable()

    def __del__(self):
        self.uninstall()

    def __call__(self, *args):
        return self.call(*args)


def create_hook(at: int, restype: Type = c_void_p, argtypes: Iterable[Type] = (), auto_install=False):
    """
    创建一个hook， 注意需要调用 install() 以及 enable()

    :param at: 该函数的内存地址
    :param restype: 返回类型
    :param argtypes: 参数类型（列表）
    :param auto_install: 是否自动调用 install_and_enable
    :return:
    """
    if auto_install:
        return lambda func: Hook(at, func, restype, argtypes).install_and_enable()
    else:
        return lambda func: Hook(at, func, restype, argtypes)


def test():
    from ctypes.wintypes import HWND, LPCWSTR, UINT, INT

    @create_hook(at=CDLL('User32.dll').MessageBoxW, restype=INT, argtypes=[HWND, LPCWSTR, LPCWSTR, UINT])
    def message_box_hook(_hook, handle, title, message, flag):
        res = _hook.original(handle, "hooked " + title, "hooked " + message, flag)
        print(f"hooked: {title} - {message}, return {res}")
        return res

    message_box_hook(None, 'hi content!', 'hi title!', 0)
    message_box_hook.install_and_enable()
    message_box_hook(None, 'hi content!', 'hi title!', 0)
    message_box_hook.uninstall()
    message_box_hook(None, 'hi content!', 'hi title!', 0)
