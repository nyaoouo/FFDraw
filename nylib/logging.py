import io
import logging
import os.path
import pathlib
import sys
import threading
import time
import typing
import zipfile

Verbose1 = 9
Verbose2 = 8
Verbose3 = 7


class AsciiFormat:
    end = 0
    bold = 1
    italic = 2
    underline = 4
    strikethrough = 9

    grey = 90
    red = 91
    green = 92
    yellow = 93
    blue = 94
    purple = 95
    cyan = 96
    light_grey = 97

    grey_f = 100
    red_f = 101
    green_f = 102
    yellow_f = 103
    blue_f = 104
    purple_f = 105
    cyan_f = 106
    light_grey_f = 107


_control_map = [
    f'\x1b[{AsciiFormat.light_grey}m',  # logging.NOTSET
    f'\x1b[{AsciiFormat.grey}m',  # logging.DEBUG
    f'\x1b[{AsciiFormat.green}m',  # logging.INFO
    f'\x1b[{AsciiFormat.yellow}m',  # logging.WARNING
    f'\x1b[{AsciiFormat.red}m',  # logging.ERROR
    f'\x1b[{AsciiFormat.red}m\x1b[{AsciiFormat.bold}m',  # logging.CRITICAL
]
_end_line = f'\x1b[{AsciiFormat.end}m'


def install(
        level=logging.DEBUG,
        format='[%(asctime)s]\t[%(levelname)s]\t[%(name)s]\t%(message)s',
        use_color=True,
        multiline_process=True,
        std_out=True,
        file_name=None,
        file_size=1024 * 1024 * 10,
        archive_zip=None,
):
    logging.addLevelName(Verbose1, 'Verbose1')
    logging.addLevelName(Verbose2, 'Verbose2')
    logging.addLevelName(Verbose3, 'Verbose3')
    if use_color:
        import platform

        if platform.system() == 'Windows':
            # enable windows console color
            import ctypes
            kernel32 = ctypes.WinDLL('kernel32')
            hStdOut = kernel32.GetStdHandle(-11)
            mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
            mode.value |= 4
            kernel32.SetConsoleMode(hStdOut, mode)

        old_stream_handler_format = logging.StreamHandler.format
        logging.StreamHandler.format = lambda obj, record: _control_map[min(record.levelno // 10, 5)] + old_stream_handler_format(obj, record) + _end_line
    if multiline_process:
        old_formatter_format = logging.Formatter.format

        def new_formatter_format(self, record: logging.LogRecord):
            exc_text = None
            if o_exc_info := record.exc_info:
                exc_text = self.formatException(o_exc_info)
                record.exc_info = None
            s_text = None
            if o_stack_info := record.stack_info:
                s_text = self.formatStack(o_stack_info)
                record.stack_info = None

            o_msg = record.msg
            res = ''
            i = 0
            to_loop = str(o_msg).split('\n')
            if exc_text: to_loop += exc_text.split('\n')
            if s_text: to_loop += s_text.split('\n')

            for i, line in enumerate(to_loop):
                record.msg = line
                if i:
                    res += '\n' + old_formatter_format(self, record)
                else:
                    res += old_formatter_format(self, record)
            if i:
                record.msg = '----------------------------------------'
                s = old_formatter_format(self, record)
                res = s + '\n' + res + '\n' + s

            record.msg = o_msg
            record.exc_info = o_exc_info
            record.stack_info = o_stack_info
            return res

        logging.Formatter.format = new_formatter_format

    handlers = []
    if std_out:
        std_handler = logging.StreamHandler(sys.stdout)
        std_handler.setLevel(level)
        handlers.append(std_handler)
    if file_name:
        file_handler = logging.StreamHandler(_Std2FileWriter(file_name, max_size=file_size, archive_zip=archive_zip))
        file_handler.setLevel(level)
        handlers.append(file_handler)

    logging.basicConfig(level=level, format=format, handlers=handlers)


STDERR = 1
STDOUT = 2
STDALL = 3


class _Std2FileWriter(io.IOBase):
    logger = logging.getLogger('Std2FileWriter')

    def __init__(self, file_name, max_size=1024 * 1024 * 10, archive_zip=None, another_output: typing.Iterable[io.IOBase] = None):
        self.file_name = pathlib.Path(file_name) if isinstance(file_name, str) else file_name
        self.file_name = self.file_name.absolute()
        self.max_size = max_size
        self.archive_zip = pathlib.Path(archive_zip) if isinstance(archive_zip, str) else archive_zip
        self.another_output = another_output
        self.archive_fmt = f'{self.file_name.stem}_%Y_%m_%d_%H_%M_%S{self.file_name.suffix}'
        self.file = None
        self._open()
        self.lock = threading.Lock()

    def __del__(self):
        self._close()

    def _open(self):
        self._close()
        self.file_name.parent.mkdir(parents=True, exist_ok=True)
        self.file = open(self.file_name, 'a', encoding='utf-8', buffering=1)

    def _close(self):
        if self.file:
            self.file.close()
            self.file = None
            return True
        return False

    def archive(self):
        if not self.archive_zip: return
        self._close()
        if os.path.exists(self.file_name):
            self.archive_zip.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(self.archive_zip, 'a') as zip_file:
                zip_file.write(self.file_name, time.strftime(self.archive_fmt), compress_type=zipfile.ZIP_DEFLATED)
            os.remove(self.file_name)

    def write(self, s):
        # with self.lock:
        if not self.file: self._open()
        if self.file.tell() > self.max_size:
            self.archive()
            self._open()
        if self.another_output:
            for another in self.another_output:
                another.write(s)
        self.file.write(s)


def std2file(file_name, max_size=1024 * 1024 * 10, archive_zip=None, select_type=0):
    writer = _Std2FileWriter(file_name, max_size, archive_zip)
    if select_type & STDERR:
        sys.stderr = writer
    if select_type & STDOUT:
        sys.stdout = writer
