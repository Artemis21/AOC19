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
    @classmethod
    def run(cls):
        return (int(input('< ')),)


class OutOp:
    params = 1
    code = 4
    @classmethod
    def run(cls, inp):
        print('>', inp)
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


def run(code):
    pos = 0
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
        out = op.run(*inps)
        if type(out) == int:
            pos = out
        else:
            for i in out:
                place = code[pos]
                pos += 1
                code[place] = i


def get_inp():
    with open('5.txt') as f:
        raw = f.read()
    return [*map(int, raw.split(','))]


def main():
    run(get_inp())


if __name__ == '__main__':
    print('5A (Send input: 1, output: last output)')
    main()
    print('5B (Send input: 5, output: last (only) output)')
    main()
