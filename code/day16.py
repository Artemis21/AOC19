import itertools


def get_inp():
    with open('code/16.txt') as f:
        return list(map(int, f.read().strip()))


def pattern(n):
    ptn = [*[0]*n, *[1]*n, *[0]*n, *[-1]*n]
    c = itertools.cycle(ptn)
    next(c)
    return c


def phase(signal):
    ret = ''
    for n in range(1, len(signal)+1):
        t = 0
        for a, b in zip(signal, pattern(n)):
            t += a * b
        ret += str(t)[-1]
    return list(map(int, ret))


def halfphase(signal):
    ret = ''
    cum = 0
    for i in reversed(signal):
        cum += i
        ret += str(cum)[-1]
    return list(reversed(list(map(int, ret))))


def part_a():
    sig = get_inp()
    for _ in range(100):
        sig = phase(sig)
    return int(''.join(map(str, sig))[:8])


def part_b():
    sig = get_inp() * 10000
    off = int(''.join(map(str, sig))[:7])
    sig = sig[off:]
    for _ in range(100):
        sig = halfphase(sig)
    return int(''.join(map(str, sig))[:8])


if __name__ == '__main__':
    print('16A:', part_a())
    print('16B:', part_b())
