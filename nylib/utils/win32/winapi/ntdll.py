import ctypes

dll = ctypes.WinDLL('ntdll.dll')

NTSTATUS = ctypes.c_ulong
THREADINFOCLASS = ctypes.c_ulong

#: Retrieves information about the specified thread.
#:
#: https://msdn.microsoft.com/en-us/library/windows/desktop/ms684283.aspx
NtQueryInformationThread = dll.NtQueryInformationThread
NtQueryInformationThread.restype = NTSTATUS
NtQueryInformationThread.argtypes = [
    ctypes.c_void_p,
    THREADINFOCLASS,
    ctypes.c_void_p,
    ctypes.c_ulong,
    ctypes.POINTER(ctypes.c_ulong)
]

PROCESSINFOCLASS = ctypes.c_ulong
NtQueryInformationProcess = dll.NtQueryInformationProcess
NtQueryInformationProcess.restype = NTSTATUS
NtQueryInformationProcess.argtypes = [
    ctypes.c_void_p,
    THREADINFOCLASS,
    ctypes.c_void_p,
    ctypes.c_ulong,
    ctypes.POINTER(ctypes.c_ulong)
]

NtQuerySystemInformation = dll.NtQuerySystemInformation
NtQuerySystemInformation.restype = NTSTATUS
NtQuerySystemInformation.argtypes = [
    ctypes.c_ulong,
    ctypes.c_void_p,
    ctypes.c_ulong,
    ctypes.POINTER(ctypes.c_ulong)
]

NtQueryObject = dll.NtQueryObject
NtQueryObject.restype = NTSTATUS
NtQueryObject.argtypes = [
    ctypes.c_void_p,
    ctypes.c_ulong,
    ctypes.c_void_p,
    ctypes.c_ulong,
    ctypes.POINTER(ctypes.c_ulong)
]

# http://undocumented.ntinternals.net/index.html?page=UserMode%2FUndocumented%20Functions%2FTime%2FNtSetTimerResolution.html
NtSetTimerResolution = dll.NtSetTimerResolution
NtSetTimerResolution.restype = NTSTATUS
NtSetTimerResolution.argtypes = [
    ctypes.c_ulong,  # DesiredResolution
    ctypes.c_bool,  # SetResolution
    ctypes.POINTER(ctypes.c_ulong)  # CurrentResolution
]
