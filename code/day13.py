import sys


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
    def __init__(self, code):
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


def get_inp():
    with open('code/13.txt') as f:
        return list(map(int, f.read().split(',')))


class Screen:
    def __init__(self, w=60, h=30):
        self.w = w
        self.h = h
        self.data = {}
        self.scoreval = 0

    def add(self, x, y, tile):
        tile = ' X#=o'[tile]
        self.data[(x, y)] = tile

    def score(self, new):
        self.scoreval = new

    def draw(self):
        p = ''
        for y in range(self.h):
            l = '\n'
            for x in range(self.w):
                l += self.data.get((x, y), ' ')
            p += l
        print(p + '\n\n' + str(self.scoreval))


class Game(Computer):
    def __init__(self, code):
        super().__init__(code)
        self.screen = Screen()
        self.out = 'x'
        self.x = None
        self.y = None

    def stdout(self, out):
        if self.out == 'x':
            self.x = out
            self.out = 'y'
        elif self.out == 'y':
            self.y = out
            self.out = 'tile'
        else:
            if (self.x, self.y) == (-1, 0):
                self.screen.score(out)
            else:
                self.screen.add(self.x, self.y, out)
            self.out = 'x'

    def stdin(self):
        screen = self.screen.data
        for i in screen:
            if screen[i] == '=':
                paddle = i[0]
            elif screen[i] == 'o':
                ball = i[0]
        if paddle > ball:
            return -1
        elif paddle < ball:
            return 1
        return 0


def part_a():
    g = Game(get_inp())
    g.run()
    return sum(g.screen.data[i] == '#' for i in g.screen.data)


def part_b():
    i = get_inp()
    i[0] = 2
    g = Game(i)
    g.run()
    return g.screen.scoreval


if __name__ == '__main__':
    print('13A:', part_a())
    print('13B:', part_b())
