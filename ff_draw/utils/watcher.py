import random
import threading

import time
import traceback
import sys

import imgui
from nylib.utils.imgui import window_mgr
from nylib.utils.threading import terminate_thread
from nylib.utils import ResEvent


def work_watcher(work_func):
    work_res = ResEvent()
    watcher_res = ResEvent()

    def _work():
        try:
            work_res.set(work_func())
        except Exception as e:
            work_res.set_exception(e)

    work_thread = threading.Thread(target=_work)

    work_trace = ''
    last_work_trace_update = 0
    res = NULL = type('NULL', (), {})()

    def update_work_trace():
        nonlocal last_work_trace_update, work_trace
        current = time.time()
        if current - last_work_trace_update > 1:
            last_work_trace_update = current
            work_trace = ''.join(traceback.format_stack(sys._current_frames()[work_thread.ident]))
        return work_trace

    def _watcher_ui():
        if work_thread.is_alive():
            imgui.text('working')
            imgui.text(update_work_trace())
            if imgui.button('cancel'):
                terminate_thread(work_thread)
        else:
            nonlocal res
            if res is NULL:
                if not work_res.is_set():
                    watcher_res.set_exception(ValueError('work thread exit without result'))
                res = str(work_res.res)
                if watcher_res.is_exc:
                    res = 'error: ' + res
            imgui.text('done')
            imgui.text(res)
            if imgui.button('ok'):
                watcher_res.set()

    def watcher_ui(window: window_mgr.Window):
        try:
            _watcher_ui()
        except Exception as e:
            watcher_res.set_exception(e)
            window.close()
        else:
            if watcher_res.is_set():
                window.close()

    from ff_draw.main import FFDraw
    FFDraw.instance.gui.window_manager.new_window(f'func_watcher {work_func}##func_watcher{work_func}_{time.time_ns()}_{random.random()}', watcher_ui, closable=False, float_state=2)
    work_thread.start()
    watcher_res.wait()
    return work_res.wait(0)
