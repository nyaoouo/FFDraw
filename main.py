import logging
import multiprocessing
import os
import pathlib
import sys

exc_path = pathlib.Path(sys.executable if getattr(sys, 'frozen', False) else __file__).absolute().parent
os.environ['ExcPath'] = str(exc_path)

from nylib.logging import install
from nylib.utils.win32.process import enable_privilege, pid_by_executable, is_admin, runas


def main():
    multiprocessing.freeze_support()
    try:
        from ff_draw.main import FFDraw
        install(file_name='AppData/log/ff_draw.log', archive_zip='AppData/log/archive_log.zip')
        logging.debug(f'current Pid:%s')
        if not is_admin():
            runas()
            exit()
        enable_privilege()
        instance = FFDraw(next(pid_by_executable(b'ffxiv_dx11.exe')))
        instance.start_sniffer()
        instance.start_gui_thread()
        instance.start_http_server()
    except StopIteration:
        logging.warning('我们要不先开个游戏？')
        os.system('pause')
    except Exception as e:
        logging.critical('critical error occurred', exc_info=e)
        os.system('pause')


if __name__ == "__main__":
    main()
