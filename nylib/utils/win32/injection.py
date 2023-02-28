import functools
import sys
from . import process, memory
from .winapi import kernel32, structure
from .process import CURRENT_PROCESS_HANDLER

python_dll_name = f"python{sys.version_info.major}{sys.version_info.minor}.dll"
local_python_dll_handle = kernel32.GetModuleHandleW(python_dll_name)
python_dll_name = python_dll_name.encode(structure.DEFAULT_CODING)
python_dll_info = process.get_module_by_name(CURRENT_PROCESS_HANDLER, python_dll_name)


@functools.cache
def pyfunc_offset(name):
    return kernel32.GetProcAddress(local_python_dll_handle, name) - python_dll_info.lpBaseOfDll


def get_python_base_address(handle, auto_inject=False):
    try:
        return process.get_module_by_name(handle, python_dll_name).lpBaseOfDll
    except KeyError:
        if not auto_inject: raise
        base = process.inject_dll(handle, python_dll_info.filename)
        process.remote_call(handle, base + pyfunc_offset(b'Py_InitializeEx'), 1, push_stack_depth=0x58)
        return base


def exec_shell_code(handle, shell_code: bytes, auto_inject=False):
    return process.remote_call(handle, get_python_base_address(handle, auto_inject) + pyfunc_offset(b'PyRun_SimpleString'), shell_code)
