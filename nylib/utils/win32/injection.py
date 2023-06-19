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


def dict_new(handle, auto_inject=False):
    return process.remote_call(handle, get_python_base_address(handle, auto_inject) + pyfunc_offset(b'PyDict_New'))


def decref(handle, pyobj):  # TODO: need impl
    pass


def exec_shell_code(handle, shell_code: bytes, p_dict=None, auto_inject=False):
    # return process.remote_call(handle, get_python_base_address(handle, auto_inject) + pyfunc_offset(b'PyRun_SimpleString'), shell_code)
    py_base = get_python_base_address(handle, auto_inject)
    need_decref = False
    if p_dict is None:
        p_dict = dict_new(handle, auto_inject)
        need_decref = True
    res = process.remote_call(handle, py_base + pyfunc_offset(b'PyRun_String'), shell_code, 0x101, p_dict, p_dict)
    if not res:
        error_occurred = process.remote_call(handle, py_base + pyfunc_offset(b'PyErr_Occurred'))
        if error_occurred:
            type_name = memory.read_string(handle, memory.read_address(handle, error_occurred + 0x18))
            with memory.Namespace(handle=handle) as ns:
                p_data = ns.store(b'\0' * 0x18)
                process.remote_call(handle, py_base + pyfunc_offset(b'PyErr_Fetch'), p_data, p_data + 0x8, p_data + 0x10)
                exc_val = memory.read_uint64(handle, p_data + 0x8)
                desc = None
                if exc_val:
                    py_str = process.remote_call(handle, py_base + pyfunc_offset(b'PyObject_Str'), exc_val)
                    str_size = ns.take(8)
                    p_str = process.remote_call(handle, py_base + pyfunc_offset(b'PyUnicode_AsUTF8AndSize'), py_str, str_size)
                    if py_str:
                        desc = memory.read_string(handle, p_str, memory.read_uint64(handle, str_size))
                        decref(handle, py_str)
                    decref(handle, exc_val)
                decref(handle, error_occurred)
            if desc:
                raise RuntimeError(f"Exception in shell: {type_name}: {desc}")
            else:
                raise RuntimeError(f"Exception in shell: {type_name}")
        else:
            raise RuntimeError(f"Exception in shell but no error occurred")
    else:
        decref(handle, res)
    if need_decref:
        decref(handle, p_dict)
