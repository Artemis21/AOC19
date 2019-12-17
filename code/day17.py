class Command:
    @staticmethod
    def write(master, val):
        address = master.next(literal=True)
        if address >= len(master.code):
            master.extra[address] = val
        else:
            master.code[address] = val


class Add(Command):
    params = 2
    @classmethod
    def run(cls, a, b, master):
        cls.write(master, a+b)


class Mult(Command):
    params = 2
    @classmethod
    def run(cls, a, b, master):
        cls.write(master, a*b)


class Input(Command):
    params = 0
    @classmethod
    def run(cls, master):
        val = master.stdin()
        cls.write(master, val)


class Output(Command):
    params = 1
    @classmethod
    def run(cls, inp, master):
        master.stdout(inp)


class TrueJump(Command):
    params = 2
    @classmethod
    def run(cls, inp, jump, master):
        if inp:
            master.pointer = jump
            master.increase = 0


class FalseJump(Command):
    params = 2
    @classmethod
    def run(cls, inp, jump, master):
        if not inp:
            master.pointer = jump
            master.increase = 0


class Less(Command):
    params = 2
    @classmethod
    def run(cls, a, b, master):
        if a < b:
            cls.write(master, 1)
        else:
            cls.write(master, 0)


class Equal(Command):
    params = 2
    @classmethod
    def run(cls, a, b, master):
        if a == b:
            cls.write(master, 1)
        else:
            cls.write(master, 0)


class ChangeBase(Command):
    params = 1
    @classmethod
    def run(cls, am, master):
        master.relbase += am


CMDS = {
    1: Add, 2: Mult, 3: Input, 4: Output, 5: TrueJump, 6: FalseJump, 7: Less,
    8: Equal, 9: ChangeBase
}


class Computer:
    def __init__(self, code, inputs=[]):
        self.code = code
        self.pointer = 0
        self.relbase = 0
        self.extra = {}
        self.relmode = False
        self.increase = 0

    def run(self):
        while not self.loop():
            pass

    def loop(self):
        op = self.next(command=True)
        cmd = self.get_cmd(op)
        if not cmd:
            return True    # OP 99
        modes = self.get_modes(op, cmd.params+1)
        inps = self.get_inps(modes[:-1])
        if modes and modes[-1] == '2':
            self.relmode = True
        cmd.run(*inps, self)
        self.pointer += self.increase
        self.increase = 0
        self.relmode = False

    def get_cmd(self, raw_op):
        str_op = str(raw_op)
        if len(str_op) < 3:
            num = raw_op
        else:
            num = int(str_op[-2:])
        if num == 99:
            return False
        return CMDS[num]

    def get_modes(self, raw_op, params):    # tested
        str_op = str(raw_op)
        given_modes = ''
        if len(str_op) > 2:
            given_modes = str_op[:-2]
        full_modes = ''
        for i in range(-1, -params-1, -1):
            try:
                full_modes += given_modes[i]
            except IndexError:
                full_modes += '0'
        return full_modes

    def get_inps(self, modes):
        ret = []
        for mode in modes:
            ret.append(self.next(mode=mode))
        return ret

    def get_param(self, mode, raw, literal=False):
        if mode == '2':
            if literal:
                return raw + self.relbase
            raw += self.relbase
            mode = '0'
        if literal:
            return raw
        if mode == '0':
            if raw < len(self.code):
                return self.code[raw]
            else:
                return self.extra.get(raw, 0)
        elif mode == '1':
            return raw

    def next(self, literal=False, command=False, mode='0'):
        raw = self.code[self.pointer + self.increase]
        self.increase += 1
        if command:
            return raw
        if mode == '0' and self.relmode:
            mode = '2'
        return self.get_param(mode, raw, literal)


class Camera(Computer):
    def __init__(self, code, inp=[]):
        super().__init__(code)
        self.grid = [[]]
        self.inp = inp
        self.last = None

    def stdin(self):
        return self.inp.pop(0)

    def stdout(self, out):
        self.last = out
        c = chr(out)
        if c == '\n':
            self.grid.append([])
        else:
            self.grid[-1].append(c)


class Vacuum(Computer):
    def __init__(self, code, grid):
        super().__init__(code)
        self.grid = grid


def find_xs(grid):
    xs = []
    for x in range(1, len(grid[0])-1):
        for y in range(1, len(grid)-1):
            if grid[y][x] != '#':
                continue
            if grid[y-1][x] == grid[y+1][x] == grid[y][x-1] == grid[y][x+1] == '#':
                xs.append(x * y)
    return sum(xs)


def find_path(grid):
    r = '<v>^'
    for y, col in enumerate(grid):
        for x, cell in enumerate(col):
            if cell in r:
                pos = [x, y, r.index(cell)]
                break
    ret = []
    blocked = False
    while '#' in str(grid):
        n, nx, ny = nxt(pos, grid)
        if n == '#' or blocked:
            blocked = False
            if ret and type(ret[-1]) == int:
                ret[-1] += 1
            else:
                ret.append(1)
            pos[0] = nx
            pos[1] = ny
            grid[pos[1]][pos[0]] = '+'
            continue
        if '#' not in str(grid): break
        for _ in range(4):
            pos[2] += 1
            pos[2] %= 4
            ret.append('L')
            n, nx, ny = nxt(pos, grid)
            if n == '#':
                if len(ret) > 2 and ret[-3:] == ['L', 'L', 'L']:
                    ret.pop(-1)
                    ret.pop(-1)
                    ret.pop(-1)
                    ret.append('R')
                break
        blocked = True
    return ret


def nxt(pos, grid):
    x, y, rawd = pos
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dx, dy = dirs[rawd]
    x += dx
    y += dy
    if y < 0 or x < 0:
        return '', x, y
    try:
        return grid[y][x], x, y
    except IndexError:
        return '', x, y


def compress(path):
    path = (
        ''.join(map(str, path)).replace('LLL', 'R').replace('LR', '+')
                               .replace('RL', '+').replace('L', '\nL')
                               .replace('R', '\nR').strip().split('\n')
    )
    new = []
    for i in path:
        if '+' in i:
            new.append(i[0] + str(eval(i[1:])))
        else:
            new.append(i)
    return '''B,B,C,C,A,C,A,C,A,B
L,6,L,10,R,12,R,12
L,10,L,10,R,6
R,12,L,12,L,12'''      # manually computed


def get_inp():
    with open('code/17.txt') as f:
        return list(map(int, f.read().split(',')))


def part_a():
    c = Camera(get_inp())
    c.run()
    c.grid.pop(-1)
    c.grid.pop(-1)
    return find_xs(c.grid)


def part_b():
    c = Camera(get_inp())
    c.run()
    grid = c.grid
    grid.pop(-1)
    grid.pop(-1)
    path = find_path(grid)
    rawinp = compress(path) + '\nn\n'
    inp = [ord(i) for i in rawinp]
    code = get_inp()
    code[0] = 2
    c = Camera(code, inp)
    c.run()
    return c.last


if __name__ == '__main__':
    print('17A:', part_a())
    print('17B:', part_b())
