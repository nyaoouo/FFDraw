import logging
import multiprocessing
import os
import pathlib
import sys
import time
exc_path = pathlib.Path(sys.executable if getattr(sys, 'frozen', False) else __file__).absolute().parent
os.environ['ExcPath'] = str(exc_path)

try:
    from nylib.logging import install
    from nylib.utils.win32.process import enable_privilege, pid_by_executable, is_admin, runas
except ImportError:
    sys.path.append(str(exc_path/'NyLib'))
    from nylib.logging import install
    from nylib.utils.win32.process import enable_privilege, pid_by_executable, is_admin, runas


def find_game_pid():
    is_log = False
    while True:
        pids = list(pid_by_executable(b'ffxiv_dx11.exe'))
        if not pids:
            if not is_log:
                logging.debug('cant find ffxiv_dx11.exe, waiting...')
                is_log = True
            time.sleep(1)
            continue
        if len(pids) > 1:
            logging.warning('发现多个游戏进程，请输入序号进行选择:\n' + '\n'.join(f'{i}:{pid}' for i, pid in enumerate(pids)))
            return pids[int(input('输入序号:'))]
        else:
            return pids[0]


def main():
    multiprocessing.freeze_support()

    try:
        from ff_draw.main import FFDraw
        install(file_name='AppData/log/ff_draw.log', archive_zip='AppData/log/archive_log.zip')
        if not is_admin():
            runas()
            exit()

        enable_privilege()
        game_pid= find_game_pid()
        logging.debug(f'current Pid:{os.getpid()} game Pid:{game_pid}')
        instance = FFDraw(game_pid)
        instance.start_sniffer()
        instance.start_http_server()
        instance.start_gui_thread()
    except Exception as e:
        logging.critical('critical error occurred', exc_info=e)
        os.system('pause')


if __name__ == "__main__":
    main()
