with open('2.txt') as f:
	raw = f.read()
IN = eval('[' + raw + ']')


def cmd(op, a, b):
	if op == 1:
		return a + b
	if op == 2:
		return a * b


def run(code):
	for idx in range(0, len(code), 4):
		op = code[idx]
		if op == 99:
			break
		i1 = code[code[idx+1]]
		i2 = code[code[idx+2]]
		i3 = code[idx+3]
		code[i3] = cmd(op, i1, i2)
	return code
	
	
def part_a(a=12, b=2):
	code = list(IN)
	code[1] = a
	code[2] = b
	code = run(code)
	return code[0]
	

def part_b():
	for a in range(100):
		for b in range(100):
			res = part_b(a, b)
			if res == 19690720:
				return 100*a + b
	
	
if __name__ == '__main__':
	print('2A:', part_a())
	print('2B:', part_b())
