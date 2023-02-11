import ctypes
import dataclasses
import typing

_T = typing.TypeVar('_T')


@dataclasses.dataclass
class ModuleBase:
    file_path: str
    image_base: int
    image_size: int


class DriverBase:

    def read(self, _type: typing.Type[_T], address: int, ) -> _T:
        """
        从目标读取内存

        :param _type: 数据类型
        :param address: 内存地址
        :return: 数据
        """
        raise NotImplementedError

    def read_string_fast(self, address: int, max_size: int = 64, encoding: str = 'utf-8', errors='ignore') -> str:
        return self.read(ctypes.c_char * max_size, address).value.decode(encoding=encoding, errors=errors)

    def read_string_safe(self, address: int, max_size: int = 64, encoding: str = 'utf-8', errors='ignore') -> str:
        buffer = bytearray()
        i = 0
        while i < max_size and (n := self.read_uint8(address + i)):
            buffer.append(n)
            i += 1
        return buffer.decode(encoding=encoding, errors=errors)

    read_string = read_string_fast

    def read_bytes(self, address: int, size: int) -> bytes:
        return self.read(ctypes.c_char * size, address)[:]

    def read_uint8(self, address: int) -> int:
        return self.read(ctypes.c_uint8, address).value

    def read_int8(self, address: int) -> int:
        return self.read(ctypes.c_int8, address).value

    def read_uint16(self, address: int) -> int:
        return self.read(ctypes.c_uint16, address).value

    def read_int16(self, address: int) -> int:
        return self.read(ctypes.c_int16, address).value

    def read_uint32(self, address: int) -> int:
        return self.read(ctypes.c_uint32, address).value

    def read_int32(self, address: int) -> int:
        return self.read(ctypes.c_int32, address).value

    def read_uint64(self, address: int) -> int:
        return self.read(ctypes.c_uint64, address).value

    def read_int64(self, address: int) -> int:
        return self.read(ctypes.c_int64, address).value

    def read_float(self, address: int) -> float:
        return self.read(ctypes.c_float, address).value

    def read_double(self, address: int) -> float:
        return self.read(ctypes.c_double, address).value

    def write(self, address: int, data) -> None:
        """
        往目标内存写入数据

        :param address: 内存地址
        :param data: 数据
        """
        raise NotImplementedError

    def write_string(self, address, string: str, encoding='utf-8'):
        self.write_bytes(address, string.encode(encoding))

    def write_bytes(self, address: int, data: bytes):
        if isinstance(data, bytearray):
            self.write(address, (ctypes.c_char * len(data)).from_buffer(data))
        else:
            self.write(address, (ctypes.c_char * len(data)).from_buffer_copy(data))

    def malloc(self, size: int) -> int:
        """
        获取新的内存空间

        :param size: 大小
        :return: 内存地址
        """
        raise NotImplementedError

    def free(self, address: int):
        """
        释放内存空间

        :param address: 内存地址
        """
        raise NotImplementedError

    def iter_modules(self) -> typing.Iterable[ModuleBase]:
        """
        遍历进程调用的 dll, so 之类
        """
        raise NotImplementedError

    def base_module(self) -> ModuleBase:
        """
        进程的执行档
        """
        return next(iter(self.iter_modules()))
