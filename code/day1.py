import math


def fuel(mass):
    return math.floor(mass / 3) - 2

def complete_fuel(mass):
    ret = 0
    while True:
        mass = math.floor(mass / 3) - 2
        if mass < 0:
            break
        ret += mass
    return ret


def get_inp():
    with open('code/1.txt') as f:
        return tuple(map(int, f))


def part_a():
    return sum(map(fuel, get_inp()))

def part_b():
    return sum(map(complete_fuel, get_inp()))


if __name__ == '__main__':
    print('1A:', part_a())
    print('1B:', part_b())
