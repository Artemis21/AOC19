class AddOp:
    params = 2
    code = 1
    @classmethod
    def run(cls, a, b):
        return (a + b,)


class MultOp:
    params = 2
    code = 2
    @classmethod
    def run(cls, a, b):
        return (a * b,)


class InpOp:
    params = 0
    code = 3
    send_input = True
    @classmethod
    def run(cls, inp):
        return (inp,)


class OutOp:
    params = 1
    code = 4
    send_output = True
    @classmethod
    def run(cls, inp, out):
        out.append(inp)
        return ()


class TrueOp:
    params = 2
    code = 5
    @classmethod
    def run(cls, inp, jump):
        if inp:
            return jump
        else:
            return ()


class FalseOp:
    params = 2
    code = 6
    @classmethod
    def run(cls, inp, jump):
        if inp:
            return ()
        else:
            return jump


class LessOp:
    params = 2
    code = 7
    @classmethod
    def run(cls, a, b):
        if a < b:
            return (1,)
        else:
            return (0,)


class EqualOp:
    params = 2
    code = 8
    @classmethod
    def run(cls, a, b):
        if a == b:
            return (1,)
        else:
            return (0,)


OPS = {
    1: AddOp, 2: MultOp, 3: InpOp, 4: OutOp, 5: TrueOp, 6: FalseOp, 7: LessOp,
    8: EqualOp
}


def run(code, p_input):
    pos = 0
    outputs = []
    while True:
        op = code[pos]
        pos += 1
        str_op = str(op)
        if len(str_op) < 3:
            main = op
            modes = ''
        else:
            main = int(str_op[-2:])
            modes = str_op[:-2]
        if main == 99:
            break
        op = OPS[main]
        fullmodes = ''
        for i in range(-1, -op.params-1, -1):
            try:
                fullmodes += modes[i]
            except IndexError:
                fullmodes += '0'
        inps = []
        for mode in fullmodes:
            raw = code[pos]
            pos += 1
            if mode == '0':
                inps.append(code[raw])
            else:
                inps.append(raw)
        if getattr(op, 'send_input', False):
            inps.append(p_input)
        if getattr(op, 'send_output', False):
            inps.append(outputs)
        out = op.run(*inps)
        if type(out) == int:
            pos = out
        else:
            for i in out:
                place = code[pos]
                pos += 1
                code[place] = i
    return outputs


def get_inp():
    with open('code/5.txt') as f:
        raw = f.read()
    return [*map(int, raw.split(','))]


def main():
    run(get_inp())


def part_a():
    return run(get_inp(), 1)[-1]


def part_b():
    return run(get_inp(), 5)[0]


if __name__ == '__main__':
    print('5A:', part_a())
    print('5B:', part_b())
