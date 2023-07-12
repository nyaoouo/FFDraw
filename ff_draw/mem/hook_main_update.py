import logging

payload = '''
def on_game_update_hook():
    import ctypes
    import queue
    from nylib.hook import create_hook
    from nylib.utils import Counter, ResEvent
    counter = Counter()
    funcs = {}
    once_func = queue.Queue()

    def on_update(_hook, game_main):
        res = _hook.original(game_main)
        for k, code in list(funcs.items()):
            try:
                exec(code, {'inject_server': inject_server})
            except Exception as e:
                inject_server.push_event('game_update_hook_error', e)
                funcs.pop(k, None)
        while True:
            try:
                _res, code = once_func.get_nowait()
                try:
                    exec(code, name_space := {'inject_server': inject_server})
                    _res.set(name_space.get('res', None))
                except Exception as e:
                    _res.set_exception(e)
            except queue.Empty:
                break
        return res

    def add_func(code):
        k = counter.get()
        funcs[k] = code
        return k

    def remove_func(k):
        funcs.pop(k, None)

    def call_once(code, time_out=5):
        once_func.put((res := ResEvent(), code))
        return res.wait(time_out)

    inject_server.call_map['add_game_update_hook'] = add_func
    inject_server.call_map['remove_game_update_hook'] = remove_func
    inject_server.call_map['call_once_game_update_hook'] = call_once
    hook = create_hook(on_game_update_addr, ctypes.c_void_p, [ctypes.c_int64])(on_update).install_and_enable()
    return hook


def try_hook():
    if not hasattr(inject_server, 'on_game_update_hook'):
        setattr(inject_server, 'on_game_update_hook', on_game_update_hook())
        return 1
    return 0

res = try_hook()
'''


def install(mem):
    on_game_update_addr = mem.scanner.find_address("48 89 5c 24 ? 57 48 ? ? ? 48 ? ? e8 ? ? ? ? 48 ? ? ? ? ? ? 48 ? ? 0f 84")
    logger = logging.getLogger('hook_main_update')

    def on_game_update_hook_error(e):
        logger.error(f'game_update_hook_error:{e}', exc_info=e)

    mem.inject_handle.client.subscribe('game_update_hook_error', on_game_update_hook_error)
    install_cnt = mem.inject_handle.run(f'on_game_update_addr = {on_game_update_addr}' + payload)
    logger.debug(f'install {install_cnt}')

    add_func = mem.inject_handle.client.rpc.add_game_update_hook
    remove_func = mem.inject_handle.client.rpc.remove_game_update_hook
    call_once = mem.inject_handle.client.rpc.call_once_game_update_hook
    return add_func, remove_func, call_once
