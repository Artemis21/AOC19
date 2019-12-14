import re


class Moon:
    @classmethod
    def load(cls, raw):
        n = r'([\-0-9]+)'
        m = re.match('<x={}, y={}, z={}>'.format(n, n, n), raw)
        return cls(*map(int, m.groups()))

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.dx = self.dy = self.dz = 0
    
    def gravity(self, other):
        if self.x > other.x:
            self.dx -= 1
        elif self.x < other.x:
            self.dx += 1
        if self.y > other.y: 
            self.dy -= 1
        elif self.y < other.y:
            self.dy += 1
        if self.z > other.z:
            self.dz -= 1
        elif self.z < other.z:
            self.dz += 1
        
    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz
    
    def energy(self):
        a = sum(map(abs, (self.x, self.y, self.z)))
        b = sum(map(abs, (self.dx, self.dy, self.dz)))
        return a * b
    
    
class Coords:
    def __init__(self, vals):
        self.coords = list(vals)
        self.vels = [0, 0, 0, 0]
        self.start = list(self.coords)
        self.n = 0
        self.done = False

    def step(self):
        for idxa, a in enumerate(self.coords):
            for idxb, b in enumerate(self.coords):
                if a == b:
                    continue
                self.vels[idxa] += (a < b)*2 - 1
        for idx, i in enumerate(self.coords):
            self.coords[idx] += self.vels[idx]
        return (self.coords == self.start) and not any(self.vels)

    def find_loop(self):
        while not self.step():
            self.n += 1
        return self.n+1


def get_inp():
    with open('code/12.txt') as f:
        return list(map(Moon.load, f))


def gcd(a, b):
    while b:
        a, b = b, a%b
    return a


def lcm(*nums):
    ret = nums[0]
    for i in nums[1:]:
        ret = ret*i / gcd(ret, i)
    return int(ret)


def part_a():
    moons = get_inp()
    for _ in range(1000):
        for a in moons:
            for b in moons:
                a.gravity(b)
        for i in moons:
            i.move()
    return sum(i.energy() for i in moons)


def part_b():
    moons = get_inp()
    x = Coords(i.x for i in moons).find_loop()
    y = Coords(i.y for i in moons).find_loop()
    z = Coords(i.z for i in moons).find_loop()
    return lcm(x, y, z)
    
    
    
if __name__ == '__main__':
    print('12A:', part_a())
    print('12B:', part_b())
