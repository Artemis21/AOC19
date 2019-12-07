import itertools


class Command:
    @staticmethod
    def write(master, val):
        address = master.next()
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


class FalseJump(Command):
    params = 2
    @classmethod
    def run(cls, inp, jump, master):
        if not inp:
            master.pointer = jump


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


CMDS = {
    1: Add, 2: Mult, 3: Input, 4: Output, 5: TrueJump, 6: FalseJump, 7: Less,
    8: Equal
}


class Computer:
    def __init__(self, code, inputs, output):
        self.code = code
        self.pointer = 0
        self.inputs = list(inputs)
        self.output = output

    def run(self):
        while not self.loop():
            pass

    def stdin(self):
        return self.inputs.pop(0)

    def stdout(self, out):
        self.output(out)

    def loop(self):
        op = self.next()
        cmd = self.get_cmd(op)
        if not cmd:
            return True    # OP 99
        modes = self.get_modes(op, cmd.params)
        inps = self.get_inps(modes)
        cmd.run(*inps, self)

    def get_cmd(self, raw_op):
        str_op = str(raw_op)
        if len(str_op) < 3:
            num = raw_op
        else:
            num = int(str_op[-2:])
        return CMDS.get(num, False)

    def get_modes(self, raw_op, params):
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
            raw = self.next()
            if mode == '0':
                ret.append(self.code[raw])
            else:
                ret.append(raw)
        return ret

    def next(self):
        ret = self.code[self.pointer]
        self.pointer += 1
        return ret


class PartA:
    def __init__(self):
        self.outputs = []
        code = self.get_inp()
        for i in self.get_phases():
            self.run_amp(code, i)
        self.ans = max(self.outputs)

    def run_amp(self, code, phases, inp=0, n=0):
        if n == 4:
            nxt = lambda out: self.add(out)
        else:
            nxt = lambda out: self.run_amp(code, phases, out, n+1)
        Computer(code, (phases[n], inp), nxt).run()

    def get_phases(self, start=0, end=5):
        return [[*i] for i in itertools.permutations(range(start, end))]

    def get_inp(self):
        with open('7.txt') as f:
            raw = f.read()
        return [*map(int, raw.split(','))]

    def add(self, out):
        self.outputs.append(out)


class AmpComputer(Computer):
    def __init__(self, code, phase):
        super().__init__(code, [phase], None)
        self.out = None

    def stdout(self, out):
        self.out = out

    def run(self, inp):
        self.inputs.append(inp)
        while (self.out == None) and (not self.loop()):
            pass
        ret = self.out
        self.out = None
        return ret


class PartB(PartA):
    def __init__(self):
        self.code = self.get_inp()
        outputs = []
        for i in self.get_phases(5, 10):
            self.make_amps(i)
            outputs.append(self.run_amps())
        self.ans = max(outputs)

    def make_amps(self, phases):
        self.amps = []
        for i in phases:
            self.amps.append(AmpComputer(list(self.code), i))

    def run_amps(self):
        oldfeed = None
        feed = 0
        n = 0
        while feed is not None:
            oldfeed = feed
            feed = self.amps[n].run(feed)
            n += 1
            n %= 5
        return oldfeed


def part_a():
    return PartA().ans


def part_b():
    return PartB().ans


if __name__ == '__main__':
    print('7A:', part_a())
    print('7B:', part_b())
