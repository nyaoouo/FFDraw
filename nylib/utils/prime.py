from random import randint


def miller_rabin(p):
    if p == 1: return False
    if p == 2: return True
    if p % 2 == 0: return False
    m, k, = p - 1, 0
    while m % 2 == 0:
        m, k = m // 2, k + 1
    a = randint(2, p - 1)
    x = pow(a, m, p)
    if x == 1 or x == p - 1: return True
    while k > 1:
        x = pow(x, 2, p)
        if x == 1: return False
        if x == p - 1: return True
        k = k - 1
    return False


def is_prime(p, r=40):
    for i in range(r):
        if not miller_rabin(p):
            return False
    return True


def get_prime_by_max(_max):
    s_num = num = randint(_max // 2, _max)
    while True:
        if is_prime(num):
            return num
        elif num + 1 >= _max:
            break
        else:
            num += 1
    while True:
        if is_prime(s_num): return s_num
        s_num -= 1


def get_prime(bit_size):
    return get_prime_by_max(1 << bit_size)


def _rsa_test():
    p1, p2 = get_prime(1024), get_prime(1024)
    n = p1 * p2
    o = (p1 - 1) * (p2 - 1)
    e = get_prime_by_max(o)
    d = pow(e, -1, o)
    enc = lambda m: pow(m, e, n)
    dec = lambda m: pow(m, d, n)
    print(f'n={n:#x}')
    print(f'e={e:#x}')
    print(f'd={d:#x}')
    print(hex(encr := enc(9)))
    print(hex(dec(encr)))


_rsa_test()
