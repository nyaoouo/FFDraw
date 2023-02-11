import ctypes.wintypes

Iphlpapi = ctypes.WinDLL('Iphlpapi.dll')


class MIB_TCPROW_OWNER_PID(ctypes.Structure):
    _fields_ = [
        ('state', ctypes.c_ulong),
        ('local_addr', ctypes.c_ulong),
        ('local_port', ctypes.c_ushort),
        ('remote_addr', ctypes.c_ulong),
        ('remote_port', ctypes.c_ushort),
        ('owning_pid', ctypes.c_ulong),
    ]


class TCP_TABLE_CLASS:
    TCP_TABLE_BASIC_LISTENER = 0
    TCP_TABLE_BASIC_CONNECTIONS = 1
    TCP_TABLE_BASIC_ALL = 2
    TCP_TABLE_OWNER_PID_LISTENER = 3
    TCP_TABLE_OWNER_PID_CONNECTIONS = 4
    TCP_TABLE_OWNER_PID_ALL = 5
    TCP_TABLE_OWNER_MODULE_LISTENER = 6
    TCP_TABLE_OWNER_MODULE_CONNECTIONS = 7
    TCP_TABLE_OWNER_MODULE_ALL = 8


class AF:
    AF_INET = 2
    AF_INET6 = 23

GetExtendedTcpTable = Iphlpapi.GetExtendedTcpTable
GetExtendedTcpTable.restype = ctypes.c_int
GetExtendedTcpTable.argtypes = [
    ctypes.c_void_p,  # pTcpTable
    ctypes.c_void_p,  # pdwSize
    ctypes.c_bool,  # bOrder
    ctypes.c_ulong,  # ulAf
    ctypes.c_uint,  # tcpTableClass
    ctypes.c_ulong  # reserved
]
