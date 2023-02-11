import ctypes
import ctypes.wintypes

dll = ctypes.WinDLL('psapi.dll')
#: Retrieves a handle for each module in the specified process that meets the specified filter criteria.
#:
#: https://msdn.microsoft.com/en-us/library/windows/desktop/ms682633(v=vs.85).aspx
EnumProcessModulesEx = dll.EnumProcessModulesEx
EnumProcessModulesEx.argtypes = [ctypes.wintypes.HANDLE,ctypes.wintypes.HMODULE,ctypes.wintypes.DWORD,ctypes.wintypes.LPDWORD,ctypes.wintypes.DWORD]
EnumProcessModulesEx.restype = ctypes.c_bool


#: Retrieves a handle for each module in the specified process that meets the specified filter criteria.
#:
#: https://msdn.microsoft.com/en-us/library/windows/desktop/ms683196(v=vs.85).aspx
GetModuleBaseNameA = dll.GetModuleBaseNameA
GetModuleBaseNameA.argtypes = [ctypes.wintypes.HANDLE,ctypes.wintypes.HMODULE,ctypes.c_void_p,ctypes.wintypes.DWORD]
GetModuleBaseNameA.restype = ctypes.c_ulonglong


#: Retrieves information about the specified module in the MODULEINFO structure.
#:
#: https://msdn.microsoft.com/en-us/library/windows/desktop/ms683201(v=vs.85).aspx
GetModuleInformation = dll.GetModuleInformation
GetModuleInformation.argtypes = [ctypes.wintypes.HANDLE,ctypes.wintypes.HMODULE,ctypes.c_void_p,ctypes.wintypes.DWORD]
GetModuleInformation.restype = ctypes.c_bool

#: Retrieves information about the specified module in the MODULEINFO structure.
#:
#: https://msdn.microsoft.com/en-us/library/windows/desktop/ms683198(v=vs.85).aspx
GetModuleFileNameExA = dll.GetModuleFileNameExA
GetModuleFileNameExA.argtypes = [ctypes.wintypes.HANDLE,ctypes.wintypes.HMODULE,ctypes.c_void_p,ctypes.wintypes.DWORD]
GetModuleFileNameExA.restype = ctypes.c_ulong
