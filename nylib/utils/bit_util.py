def bit_list_flag_set(_list, idx, val, item_size=8):
    if val:
        _list[idx // item_size] |= 1 << (idx % item_size)
    else:
        _list[idx // item_size] &= ~(1 << (idx % item_size))


def bit_list_flag_get(_list, idx, item_size=8):
    return (_list[idx // item_size] & 1 << (idx % item_size)) > 0


def bit_iter_idx(v):
    i = 0
    while v:
        if v & 1: yield i
        v >>= 1
        i += 1


def bit_to_list(v, size=0):
    res = []
    while v:
        res.append(v & 1)
        v >>= 1
    if (add := size - len(res)) > 0:
        res.extend(0 for _ in range(add))
    return res


def bit_from_list(l):
    v = 0
    for _v in reversed(l):
        v = (v << 1) | _v
    return v


def bit_count(v):
    i = 0
    while v:
        if v & 1: i += 1
        v >>= 1
    return i
