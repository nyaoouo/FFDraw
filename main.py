import logging
import os
import pathlib
import sys
import threading
import time

os.environ['ExcPath'] = str(pathlib.Path(sys.executable if getattr(sys, 'frozen', False) else __file__).absolute().parent)

from nylib.logging import install
from nylib.utils.win32.process import enable_privilege, pid_by_executable
from ff_draw.main import FFDraw

if __name__ == "__main__":
    install()
    try:
        enable_privilege()
        instance = FFDraw(next(pid_by_executable(b'ffxiv_dx11.exe')))
        instance.start_gui_thread()
        instance.start_http_server()
    except Exception as e:
        logging.critical('critical error occurred', exc_info=e)
        os.system('pause')
