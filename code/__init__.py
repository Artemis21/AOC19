import importlib
import time


LAST = 14


def load(num):
    return importlib.import_module(f'.day{num}', __package__)


def wait(fun):
    s = time.time()
    v = fun()
    e = time.time()
    return v, e-s


def run_part(num, part, module=None):
    if not module:
        module = load(num)
    if part == 'A':
        fun = module.part_a
    else:
        fun = module.part_b
    val, t = wait(fun)
    print(f'{num:>3}{part}: {val:<10} ({t:.3}s)')
    return t


def run_challenge(num):
    module = load(num)
    atime = run_part(num, 'A', module)
    btime = run_part(num, 'B', module)
    return atime + btime


def run_parts(*parts):
    for i in parts:
        if i[-1].upper() not in ('A', 'B'):
            run_challenge(int(i))
        else:
            num = int(i[:-1])
            part = i[-1].upper()
            run_part(num, part)


def run_all():
    print('Running Advent of Code 2019 solutions:')
    total = 0
    for i in range(1, LAST+1):
        total += run_challenge(i)
    avg = total / (LAST * 2)
    print(
        f'Total time: {total:.3}s | Average time per challange part: {avg:.3}s'
    )
