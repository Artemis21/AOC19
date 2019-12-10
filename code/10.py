import math


def count_pos(y, x, grid):
    angles = set()
    for ty, row in enumerate(grid):
        for tx, cell in enumerate(row):
            if cell:
                angle = math.atan2(tx-x, ty-y)
                angles.add(angle)
    return len(angles)


def get_next(y, x, grid, last):
    angles = {}
    smaller = {}
    start = math.atan2(0, -1)
    for ty, row in enumerate(grid):
        for tx, cell in enumerate(row):
            if ty == y and tx == x:
                continue
            if cell:
                angle = math.atan2(tx-x, ty-y) - start
                d = angles
                if angle < last:
                    d = smaller
                if angle not in d:
                    d[angle] = []
                d[angle].append((ty, tx))
    mina = 4
    for angle in angles:
        if angle < last and angle > mina:
            mina = angle
    if mina == 4:
        if smaller:
            mina = max(smaller)
            angles[mina] = smaller[mina]
        else:
            mina = max(angles)
    closest = None
    dist = 100
    for ty, tx in angles[mina]:
        tdist = abs(ty-y) + abs(tx-x)
        if tdist < dist:
            dist = tdist
            closest = (ty, tx)
    return closest, mina


def twohundreth(grid, y, x):
    last = 0
    for i in range(199):
        nyt, last = get_next(y, x, grid, last)
        ty, tx = nyt
        grid[ty][tx] = 0
    return ty, tx


def max_visibility(grid):
    counts = {}
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if not grid[y][x]:
                continue
            count = count_pos(y, x, grid)
            counts[(y, x)] = count
    best = max(counts, key=lambda y: counts[y])
    return counts[best], best


def get_inp():
    with open('10.txt') as f:
        raw = f.read().strip()
    grid = []
    for row in raw.split('\n'):
        rowlst = []
        for cell in row:
            rowlst.append('.#'.index(cell))
        grid.append(rowlst)
    return grid


def part_a():
    return max_visibility(get_inp())[0]


def part_b():
    grid = get_inp()
    y, x = twohundreth(grid, *max_visibility(grid)[1])
    return 100*x + y


if __name__ == '__main__':
    print('10A:', part_a())
    print('10B:', part_b())
