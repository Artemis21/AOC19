def orbits(inp):
    tree = []
    index = {'COM': tree}
    for a, b in inp:
        if b not in index:
            index[b] = []
        if a not in index:
            index[a] = []
        index[a].append(index[b])
    return tree, index


def inp():
    with open('code/6.txt') as f:
        raw = f.read()
    return [i.split(')') for i in raw.split('\n')]


def count(tree):
    done = {}

    def recurse(tree, depth):
        if not tree:
            return depth
        name = str((depth, tree))
        if name in done:
            return done[name]
        val = sum(recurse(i, depth+1) for i in tree) + depth
        done[name] = val
        return val
    return recurse(tree, 0)


def distance(tree, index, a='YOU', b='SAN'):
    parents = {}

    def get_parents(tree):
        for i in tree:
            parents[id(i)] = tree
            get_parents(i)

    def find(obj, path=[tree], tree=tree):
        if tree is obj:
            return path
        path = list(path)
        path.append(tree)
        for i in tree:
            found = find(obj, path, i)
            if found:
                return found
        return None
    apath = find(index[a])
    bpath = find(index[b])
    common = []
    for ap in apath:
        for bp in bpath:
            if ap is bp:
                common.append(ap)
                break
    nca = common[-1]

    def depth(find, tree, cur=0):
        if tree is find:
            return cur
        cur += 1
        for i in tree:
            found = depth(find, i, cur)
            if found:
                return found
        return None
    return depth(index[a], nca) + depth(index[b], nca) - 2


def part_a():
    return count(orbits(inp())[0])


def part_b():
    return distance(*orbits(inp()))


if __name__ == '__main__':
    print('6A:', part_a())
    print('6B:', part_b())
