import logging
import pathlib
import threading
import typing

if typing.TYPE_CHECKING:
    from . import Command


class Script:
    logger = logging.getLogger('CommandScript')
    def __init__(self, main: 'Command', script_name):
        self.main = main.main
        self.script_name = script_name
        for p_ in self.main.plugin_path:
            if (s := pathlib.Path(p_) / 'scripts' / f'{script_name}.py').exists():
                self.script_path = s
                break
        else:
            raise FileNotFoundError(f'no script {script_name} found')

    def run(self, args):
        code = compile(self.script_path.read_text('utf-8'), self.script_path, 'exec')
        try:
            exec(code, {'__file__': str(self.script_path), 'args': args})
        except Exception as e:
            self.logger.error(f'error in {self.script_name}: {e}',exc_info=True)

    def run_thread(self, args):
        (t := threading.Thread(target=self.run, args=(args,),daemon=True)).start()
        return t
