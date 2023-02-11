import ctypes
import ipaddress
import socket
from .winapi import iphlpapi


def find_process_tcp_connections(pid: int):
    buffer_length = ctypes.c_ulong(0)
    iphlpapi.GetExtendedTcpTable(None, ctypes.byref(buffer_length), False, iphlpapi.AF.AF_INET, iphlpapi.TCP_TABLE_CLASS.TCP_TABLE_OWNER_PID_ALL, 0)
    size = (buffer_length.value - 4) // ctypes.sizeof(iphlpapi.MIB_TCPROW_OWNER_PID)
    Table = type('Table', (ctypes.Structure,), {'_fields_': [('length', ctypes.c_ulong,), ('table', iphlpapi.MIB_TCPROW_OWNER_PID * size)]})
    table = Table()
    if iphlpapi.GetExtendedTcpTable(
            ctypes.byref(table),
            ctypes.byref(buffer_length),
            False,
            iphlpapi.AF.AF_INET,
            iphlpapi.TCP_TABLE_CLASS.TCP_TABLE_OWNER_PID_ALL,
            0
    ): raise RuntimeError('GetExtendedTcpTable failed')
    for t in table.table:
        if t.owning_pid == pid:
            yield ipaddress.IPv4Address(socket.ntohl(t.local_addr)), \
                  socket.ntohs(t.local_port), \
                  ipaddress.IPv4Address(socket.ntohl(t.remote_addr)), \
                  socket.ntohs(t.remote_port)
