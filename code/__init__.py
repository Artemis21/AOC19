import importlib
import time


def wait(fun):
    s = time.time()
    v = fun()
    e = time.time()
    return v, e-s


print('Running Advent of Code 2019 solutions:')
start = time.time()


for i in range(1, 12):
    name = f'{i}'
    module = importlib.import_module(name, '.')
    av, at = wait(module.part_a)
    print(f'{i:>3}A: {av:<10} ({at:.3}s)')
    bv, bt = wait(module.part_b)
    print(f'{i:>3}B: {bv:<10} ({bt:.3}s)')


end = time.time()
total = end - start
print(f'Total time: {total:.3}s.')
print(f'Average per challenge part: {total/11:.3}s')
