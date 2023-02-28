import os
import struct
import sys
from ctypes import *

from win32con import PROCESS_ALL_ACCESS

from .winapi import kernel32, psapi, structure, advapi32
from . import exception, memory

CURRENT_PROCESS_HANDLER = -1


def get_memory_basic_information_at_address(
        handle,
        address: int
):
    mbi = structure.MEMORY_BASIC_INFORMATION()
    if kernel32.VirtualQueryEx(
            handle,
            address,
            byref(mbi),
            sizeof(mbi)
    ) == sizeof(structure.MEMORY_BASIC_INFORMATION): return mbi
    raise exception.WinAPIError(kernel32.GetLastError(), "VirtualQueryEx")


def enum_process_module(handle):
    hModules = (c_void_p * 1024)()
    windll.kernel32.SetLastError(0)
    process_module_success = psapi.EnumProcessModulesEx(
        handle,
        byref(hModules),
        sizeof(hModules),
        byref(c_ulong()),
        structure.EnumProcessModuleEX.LIST_MODULES_64BIT
    )
    error_code = windll.kernel32.GetLastError()
    if error_code:
        windll.kernel32.SetLastError(0)
        raise exception.WinAPIError(error_code)
    if process_module_success:
        for hModule in iter(m for m in hModules if m):
            module_info = structure.MODULEINFO(handle)
            psapi.GetModuleInformation(
                handle,
                c_void_p(hModule),
                byref(module_info),
                sizeof(module_info)
            )
            yield module_info


def get_base_module(handle):
    return next(iter(enum_process_module(handle)))


def get_module_by_name(handle, module_name: bytes):
    module_name = module_name.lower()
    for module in enum_process_module(handle):
        if module.name.lower() == module_name:
            return module
    raise KeyError(module_name)


def inject_dll(handle, filepath):
    if not (load_library_a_address := kernel32.GetProcAddress(get_module_by_name(handle, b'kernel32.dll').lpBaseOfDll, b"LoadLibraryA")):
        raise exception.WinAPIError()
    return remote_call(handle, load_library_a_address, filepath)


# def inject_dll(handle, filepath):
#     windll.kernel32.SetLastError(0)
#     if not (filepath_address := kernel32.VirtualAllocEx(
#             handle,
#             0,
#             len(filepath),
#             structure.MEMORY_STATE.MEM_COMMIT.value | structure.MEMORY_STATE.MEM_RESERVE.value,
#             structure.MEMORY_PROTECTION.PAGE_EXECUTE_READWRITE.value
#     )):
#         raise exception.WinAPIError()
#     kernel32.WriteProcessMemory(handle, filepath_address, filepath, len(filepath), None)
#     if not (load_library_a_address := kernel32.GetProcAddress(get_module_by_name(handle, b'kernel32.dll').lpBaseOfDll, b"LoadLibraryA")):
#         raise exception.WinAPIError()
#     thread_h = kernel32.CreateRemoteThread(
#         handle, None, 0, load_library_a_address, filepath_address, 0, None
#     )
#     kernel32.WaitForSingleObject(thread_h, -1)
#     kernel32.VirtualFreeEx(
#         handle, filepath_address, len(filepath), structure.MEMORY_STATE.MEM_RELEASE.value
#     )
#     dll_name = os.path.basename(filepath)
#     dll_name = dll_name.decode('ascii')
#     module_address = kernel32.GetModuleHandleW(dll_name)
#     return module_address
#

def start_thread(handler, call_address, params=None):
    params = params or 0
    windll.kernel32.SetLastError(0)
    if not (thread_h := kernel32.CreateRemoteThread(
            handler,
            None,
            0,
            call_address,
            params,
            0,
            0,
    )):
        raise exception.WinAPIError()
    kernel32.WaitForSingleObject(thread_h, -1)
    return thread_h


def list_processes():
    SNAPPROCESS = 0x00000002
    windll.kernel32.SetLastError(0)
    hSnap = kernel32.CreateToolhelp32Snapshot(SNAPPROCESS, 0)
    process_entry = structure.ProcessEntry32()
    process_entry.dwSize = sizeof(process_entry)
    p32 = kernel32.Process32First(hSnap, byref(process_entry))
    if p32:
        yield process_entry
    while p32:
        yield process_entry
        p32 = kernel32.Process32Next(hSnap, byref(process_entry))
    kernel32.CloseHandle(hSnap)


def enable_privilege():
    hProcess = c_void_p(CURRENT_PROCESS_HANDLER)
    if advapi32.OpenProcessToken(hProcess, 32, byref(hProcess)):
        tkp = structure.TOKEN_PRIVILEGES()
        advapi32.LookupPrivilegeValue(None, "SeDebugPrivilege", byref(tkp.Privileges[0].Luid))
        tkp.count = 1
        tkp.Privileges[0].Attributes = 2
        advapi32.AdjustTokenPrivileges(hProcess, 0, byref(tkp), 0, None, None)
        return kernel32.GetLastError()
    return 0


def get_module_info(process_id: int, module_name: str):
    h_snap = windll.kernel32.CreateToolhelp32Snapshot(8, process_id)
    if h_snap == -1: raise Exception("CreateToolhelp32Snapshot")
    module_entry = structure.MODULEENTRY32()
    module_entry.dwSize = sizeof(module_entry)
    while windll.kernel32.Module32Next(h_snap, byref(module_entry)):
        if module_name == module_entry.szModule.decode(structure.DEFAULT_CODING):
            windll.kernel32.CloseHandle(h_snap)
            return module_entry
    windll.kernel32.CloseHandle(h_snap)
    raise Exception(f"Module {module_name} not found")


def process_is_wow64(handle):
    buf = c_ulong(0)
    if windll.kernel32.IsWow64Process(handle, byref(buf)):
        return bool(buf.value)
    raise exception.WinAPIError(windll.kernel32.GetLastError(), "IsWow64Process")


def pid_by_executable(executable_name: bytes):
    for process in list_processes():
        if process.szExeFile == executable_name:
            yield process.th32ProcessID


def open_process(process_id: int, desired_access=PROCESS_ALL_ACCESS, inherit_handle=False):
    if handle := kernel32.OpenProcess(desired_access, inherit_handle, process_id):
        return handle
    raise exception.WinAPIError(windll.kernel32.GetLastError(), "OpenProcess")


def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except:
        return False


def runas():
    windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


_MOV_RBX = b'\x48\xBB'  # MOV rbx, n
_INT_ARG = [
    b'\x48\xB9',  # MOV rcx, n
    b'\x48\xBA',  # MOV rdx, n
    b'\x49\xB8',  # MOV r8, n
    b'\x49\xB9',  # MOV r9, n
]
_FLOAT_ARG = [
    b'\xF3\x0F\x10\x03',  # MOVSS xmm0, [rbx]
    b'\xF3\x0F\x10\x0B',  # MOVSS xmm1, [rbx]
    b'\xF3\x0F\x10\x13',  # MOVSS xmm2, [rbx]
    b'\xF3\x0F\x10\x1B',  # MOVSS xmm3, [rbx]
]
def remote_call(handle, func_ptr, *args: int | float | bytes | bool, push_stack_depth=0x28):
    if len(args) > 4:
        raise ValueError('not yet handle args more then 4')
    with memory.Namespace(handle) as name_space:
        return_address = name_space.take(8)
        shell = (
                b"\x55"  # PUSH rbp
                b"\x48\x89\xE5"  # MOV rbp, rsp
                b"\x48\x83\xec" + struct.pack('B', push_stack_depth) +  # SUB rsp, push_stack_depth
                b"\x53"  # PUSH rbx
                b"\x48\x31\xDB"  # XOR rbx, rbx
        )
        for i, a in enumerate(args):
            if isinstance(a, bytes):
                a = name_space.store(a)
            elif isinstance(a, bool):
                a = int(a)
            if isinstance(a, int):
                shell += _INT_ARG[i] + struct.pack('q', a)
            elif isinstance(a, float):
                shell += _MOV_RBX + struct.pack('f', a) + bytes(4) + _FLOAT_ARG[i]
            else:
                raise TypeError(f'not support arg type {type(a)} at pos {i}')
        shell += (
                b"\x48\xBB" + struct.pack('q', func_ptr) +  # MOV rbx, func_ptr
                b"\xFF\xD3"  # CALL rbx
                b"\x48\xBB" + struct.pack('q', return_address) +  # MOV rbx, return_address
                b"\x48\x89\x03"  # MOV [rbx], rax
                b"\x5B"  # POP rbx
                b"\x48\x83\xc4" + struct.pack('B', push_stack_depth) +  # ADD rsp, 0x28
                b"\x48\x89\xEC"  # MOV rsp, rbp
                b"\x5D"  # POP rbp
                b"\xC3"  # RET
        )
        code_address = name_space.store(shell)
        start_thread(handle, code_address)
        return memory.read_uint64(handle, return_address)
