import sys
from . import process, memory
from .winapi import kernel32, structure
from .process import CURRENT_PROCESS_HANDLER

python_dll_name = f"python{sys.version_info.major}{sys.version_info.minor}.dll"
local_python_dll_handle = kernel32.GetModuleHandleW(python_dll_name)
python_dll_name = python_dll_name.encode(structure.DEFAULT_CODING)
python_dll_info = process.get_module_by_name(CURRENT_PROCESS_HANDLER, python_dll_name)
func_offsets = {
    'Py_InitializeEx': kernel32.GetProcAddress(local_python_dll_handle, b'Py_InitializeEx') - python_dll_info.lpBaseOfDll,
    'PyRun_SimpleString': kernel32.GetProcAddress(local_python_dll_handle, b'PyRun_SimpleString') - python_dll_info.lpBaseOfDll,
    'Py_FinalizeEx': kernel32.GetProcAddress(local_python_dll_handle, b'Py_FinalizeEx') - python_dll_info.lpBaseOfDll,
}

def get_python_base_address(handle, auto_inject=False):
    py_dll_module = process.get_module_by_name(handle, python_dll_name)
    if py_dll_module is None:
        if auto_inject:
            base = process.inject_dll(handle, python_dll_info.filename)
            param_address = memory.alloc(handle, 4)
            memory.write_int(handle, param_address, 1)
            process.start_thread(handle, base + func_offsets['Py_InitializeEx'], param_address)
            return base
        else:
            raise Exception("Python DLL not found")
    return py_dll_module.lpBaseOfDll


def exec_shell_code(handle, shell_code: bytes, auto_inject=False):
    py_base_address = get_python_base_address(handle, auto_inject)
    shell_code_address = memory.alloc(handle, len(shell_code))
    memory.write_string(handle, shell_code_address, shell_code)
    process.start_thread(handle, py_base_address + func_offsets['PyRun_SimpleString'], shell_code_address)
    kernel32.VirtualFreeEx(handle, shell_code_address, 0, 0x8000)
