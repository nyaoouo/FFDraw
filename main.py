import logging
import os
import pathlib
import sys

exc_path = pathlib.Path(sys.executable if getattr(sys, 'frozen', False) else __file__).absolute().parent
os.environ['ExcPath'] = str(exc_path)
os.environ['PathEncoding'] = encoding_path.read_text().strip() if (encoding_path := exc_path / 'path_encoding.txt').exists() else sys.getfilesystemencoding()

from nylib.logging import install
from nylib.utils.win32.process import enable_privilege, pid_by_executable
from ff_draw.main import FFDraw

if __name__ == "__main__":
    install()
    logging.debug('set path encoding:%s' % os.environ['PathEncoding'])
    try:
        enable_privilege()
        instance = FFDraw(next(pid_by_executable(b'ffxiv_dx11.exe')))
        instance.start_gui_thread()
        instance.start_http_server()
    except Exception as e:
        logging.critical('critical error occurred', exc_info=e)
        os.system('pause')
