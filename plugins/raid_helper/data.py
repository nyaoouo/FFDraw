import inspect


class DictLock(dict):
    def __init__(self):
        super().__init__()
        self.edit_source = {}

    def assert_locked(self, key):
        s = inspect.stack()[2]
        callee = s.filename, s.lineno
        if self.edit_source.setdefault(key, callee)[0] != callee[0]:
            old_filename, old_line = self.edit_source[key]
            raise RuntimeError(f"key {key!r} is being edited by {old_filename}:{old_line}")

    def __setitem__(self, key, value):
        self.assert_locked(key)
        super().__setitem__(key, value)

    def __delitem__(self, key):
        self.assert_locked(key)
        self.edit_source.pop(key, None)
        super().__delitem__(key)

    def pop(self, key, default=None):
        self.assert_locked(key)
        self.edit_source.pop(key, None)
        return super().pop(key, default)

special_actions = DictLock()
delay_until = DictLock()
omen_color = DictLock()
