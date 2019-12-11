import collections


def trace_wire(wire):
    places = []
    pos = [0, 0]
    steps = 0
    retsteps = collections.OrderedDict()
    for i in wire:
        d, n = i[0], int(i[1:])
        if d in ('U', 'D'):
            old = pos[1]
            if d == 'U':
                new = old - n
                r = range(old-1, new-1, -1)
            else:
                new = old + n
                r = range(old+1, new+1)
            for y in r:
                steps += 1
                coords = (pos[0], y)
                if coords not in retsteps:
                    retsteps[coords] = steps
                places.append(coords)
            pos[1] = new
        else:
            old = pos[0]
            if d == 'L':
                new = old - n
                r = range(old-1, new-1, -1)
            else:
                new = old + n
                r = range(old+1, new+1)
            for x in r:
                steps += 1
                coords = (x, pos[1])
                if coords not in retsteps:
                    retsteps[coords] = steps
                places.append(coords)
            pos[0] = new
    return places, retsteps


def inp():
    with open('3.txt') as f:
        raw = f.read()
    split = raw.split('\n')
    a = split[0].split(',')
    b = split[1].split(',')
    return a, b        
    

def part_a(wires=inp()):
    a = set(trace_wire(wires[0])[0])
    b = set(trace_wire(wires[1])[0])
    xs = a & b
    dists = []
    for i in xs:
        dist = abs(i[0]) + abs(i[1])
        dists.append(dist)
    return min(dists)

def part_b(wires=inp()):
    a, sta = trace_wire(wires[0])
    b, stb = trace_wire(wires[1])
    xs = list(set(a) & set(b))
    steps = []
    for i in xs:
        stsa = sta[i]
        stsb = stb[i]
        steps.append(stsa + stsb)
    return min(steps)


if __name__ == '__main__':
    print('3A:', part_a())
    print('3B: ', part_b())
