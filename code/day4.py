import re


def check_same(pwd):
    old = ''
    for i in pwd:
        if i == old:
            return True
        old = i
    return False


def get_p():
    each = []
    for i in range(10):
        p = '(^|[^{}]){}{}([^{}]|$)'.format(i, i, i, i)
        each.append(p)
    return '(' + ')|('.join(each) + ')'


def check_b_same(pwd, p):
    return re.search(p, pwd)


def check_diff(pwd):
    old = 0
    for i in pwd:
        i = int(i)
        if i < old:
            return False
        old = i
    return True


def part_a(inp='108457-562041'):
    start, end = inp.split('-')
    poss = 0
    for pwd in range(int(start), int(end)+1):
        s = str(pwd)
        if check_same(s) and check_diff(s):
            poss += 1
    return poss


def part_b(inp='108457-562041'):
    start, end = inp.split('-')
    poss = 0
    pttn = get_p()
    for pwd in range(int(start), int(end)+1):
        s = str(pwd)
        if check_b_same(s, pttn) and check_diff(s):
            poss += 1
    return poss


if __name__ == '__main__':
    print('4A:', part_a())
    print('4B:', part_b())
