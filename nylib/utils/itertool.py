def repeat_add(start, times, step=1):
    for _ in range(times):
        yield start
        start = start + step


def iter_repeat_add(d, add=0):
    start, times, step = d
    if isinstance(start, int):
        for i in range(times):
            yield start + add
            add += step
    else:
        for i in range(times):
            yield iter_repeat_add(start, add)
            add += step


def seq_dif(seq):
    if len(seq) < 2:
        raise ValueError()
    _n = next(it := iter(seq))
    dif = (n := next(it)) - _n
    while 1:
        try:
            if (_n := next(it)) - n != dif:
                raise ValueError()
        except StopIteration:
            return dif
        n = _n


def seq_to_repeat_add(seq):
    return seq[0], len(seq), seq_dif(seq)


def seq_to_range(seq):
    if (dif := seq_dif(seq)) == 0:
        raise ValueError()
    return seq[0], seq[-1] + (1 if dif > 0 else -1), dif
