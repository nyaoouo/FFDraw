import dataclasses
import inspect

lazy_chunks_key = '__lazy_chunks__'


@dataclasses.dataclass
class LazyChunk:
    _code: str
    _global: dict
    _local: dict

    def _load(self):
        if self._code:
            exec(self._code, self._global, self._local)
            self._code = ''

    def __getattr__(self, item):
        self._load()
        if item in self._local:
            return self._local[item]
        if item in self._global:
            return self._global[item]
        raise NameError(item)

    def __bool__(self):
        return False


def lazy_chunk():
    import re
    stack = inspect.stack()[1]
    with open(stack.filename, encoding='utf-8') as _src:
        src = iter(_src)
        for _ in range(stack.lineno): next(src)
        spacing, code = re.match(r"( *)([^ ].*)?", next(src)).groups()
        chunk_ind = len(spacing)
        code += '\n'
        while (line := next(src, None)) is not None:
            spacing, line_code = re.match(r"( *)([^ ].*)?", line).groups()
            if not line_code: continue
            if (_ind := len(spacing)) < chunk_ind: break
            code += ' ' * (_ind - chunk_ind) + line_code + '\n'
    frame = stack.frame
    frame.f_locals.setdefault(lazy_chunks_key, []).append(res := LazyChunk(code.strip(), frame.f_globals, frame.f_locals))
    return res
