from ctypes import *
from ctypes.util import find_library
from pathlib import Path

c_void_pp = POINTER(c_void_p)

clib = cdll.LoadLibrary(find_library(
    str(Path(__file__).parent / 'res' / ('EasyHook64.dll' if sizeof(c_void_p) == 8 else 'EasyHook32.dll'))
))


class HOOK_TRACE_INFO(Structure):
    _fields_ = [("Link", c_void_p)]


TRACED_HOOK_HANDLE = POINTER(HOOK_TRACE_INFO)

lh_install_hook = clib.LhInstallHook
lh_install_hook.restype = c_ulong
lh_install_hook.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]

lh_uninstall_hook = clib.LhUninstallHook
lh_uninstall_hook.restype = c_ulong
lh_uninstall_hook.argtypes = [c_void_p]

lh_uninstall_all_hooks = clib.LhUninstallAllHooks
lh_uninstall_all_hooks.restype = c_ulong

rtl_get_last_error = clib.RtlGetLastError
rtl_get_last_error.restype = c_ulong

rtl_get_last_error_string = clib.RtlGetLastErrorString
rtl_get_last_error_string.restype = c_wchar_p

lh_set_inclusive_acl = clib.LhSetInclusiveACL
lh_set_inclusive_acl.restype = c_ulong
lh_set_inclusive_acl.argtypes = [c_void_p, c_ulong, c_void_p]

lh_set_exclusive_acl = clib.LhSetExclusiveACL
lh_set_exclusive_acl.restype = c_ulong
lh_set_exclusive_acl.argtypes = [c_void_p, c_ulong, c_void_p]

lh_get_bypass_address = clib.LhGetHookBypassAddress
lh_get_bypass_address.restype = c_ulong
lh_get_bypass_address.argtypes = [c_void_p, c_void_pp]

lh_wait_for_pending_removals = clib.LhWaitForPendingRemovals


def test():
    from ctypes.wintypes import HWND, LPCWSTR, UINT
    t_dll = CDLL('User32.dll')
    t_dll.MessageBoxW.argtypes = [HWND, LPCWSTR, LPCWSTR, UINT]
    play_test = lambda: t_dll.MessageBoxW(None, 'hi content!', 'hi title!', 0)
    play_test()

    interface = CFUNCTYPE(c_int, HWND, LPCWSTR, LPCWSTR, UINT)

    def fake_function(handle, title, message, flag):
        print(title, message)
        return t_original(handle, "hooked " + title, "hooked " + message, flag)

    hook_f = interface(fake_function)

    t_hook_info = HOOK_TRACE_INFO()
    if lh_install_hook(t_dll.MessageBoxW, hook_f, None, byref(t_hook_info)):
        raise Exception(f"EasyHookException {rtl_get_last_error():#X}:{rtl_get_last_error_string()}")

    original_func_p = c_void_p()

    if lh_get_bypass_address(byref(t_hook_info), byref(original_func_p)):
        raise Exception(f"EasyHookException {rtl_get_last_error():#X}:{rtl_get_last_error_string()}")

    t_original = interface(original_func_p.value)
    t_original(None, 'o content!', 'o title!', 0)

    ACLEntries = (c_ulong * 1)(0)
    if lh_set_inclusive_acl(addressof(ACLEntries), 1, byref(t_hook_info)):
        raise Exception(f"EasyHookException {rtl_get_last_error():#X}:{rtl_get_last_error_string()}")

    print('inclusive')
    play_test()

    if lh_set_exclusive_acl(addressof(ACLEntries), 1, byref(t_hook_info)):
        raise Exception(f"EasyHookException {rtl_get_last_error():#X}:{rtl_get_last_error_string()}")

    print('exclusive')
    play_test()

    if lh_set_inclusive_acl(addressof(ACLEntries), 1, byref(t_hook_info)):
        raise Exception(f"EasyHookException {rtl_get_last_error():#X}:{rtl_get_last_error_string()}")

    print('inclusive')
    play_test()

    if lh_uninstall_hook(byref(t_hook_info)):
        raise Exception(f"EasyHookException {rtl_get_last_error():#X}:{rtl_get_last_error_string()}")

    print('uninstalled')
    play_test()

    if lh_wait_for_pending_removals():
        raise Exception(f"EasyHookException {rtl_get_last_error():#X}:{rtl_get_last_error_string()}")

    print('end')
