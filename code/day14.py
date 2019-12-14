import re
import math


def parse_line(raw):
	term = '[0-9]+ [A-Z]+'
	gs = re.findall(term, raw)
	new = []
	for i in gs:
		parts = i.split(' ')
		num = int(parts[0])
		name = parts[1].replace(',', '').replace(' ', '')
		new.append((num, name))
	return new[:-1], new[-1]


def get_inp():
	ret = {}
	with open('14.txt') as f:
		for line in f:
			react, prod = parse_line(line)
			ret[prod] = react
	return ret
	
	
def find_needed(prod, data):
	for i in data:
		if i[1] == prod:
			break
	return data[i], i[0]


def find_ore(data, fuel=1):
	leftover = {}
	
	def follow(prod, amnt):
		if prod == 'ORE':
			return amnt, amnt
		needed, makes = find_needed(prod, data)
		make = math.ceil(amnt/makes)
		ore = 0
		for namt, nprod in needed:
			namt *= make
			if nprod in leftover:
				lft = leftover[nprod]
				if lft >= namt:
					leftover[nprod] = lft - namt
					continue
				leftover[nprod] = 0
				namt -= lft	
			nore, made = follow(nprod, namt)
			ore += nore
			if nprod not in leftover:
				leftover[nprod] = 0
			leftover[nprod] += made - namt
		return ore, make*makes
	return follow('FUEL', fuel)[0]


def check_fuel(data, fuel):
	leftover = {}
	ore = 1_000_000_000_000
	
	def follow(prod, amnt):
		nonlocal ore
		if prod == 'ORE':
			ore -= amnt
			return amnt
		needed, makes = find_needed(prod, data)
		make = math.ceil(amnt/makes)
		for namt, nprod in needed:
			namt *= make
			if nprod in leftover:
				lft = leftover[nprod]
				if lft >= namt:
					leftover[nprod] = lft - namt
					continue
				leftover[nprod] = 0
				namt -= lft	
			made = follow(nprod, namt)
			if made - namt:
				if nprod not in leftover:
					leftover[nprod] = 0
				leftover[nprod] += made - namt
		return make*makes

	follow('FUEL', fuel)
	if ore < 0:
		return False
	return True
	
	
def find_fuel(data):
	low = 0
	high = 10_000_000
	while high - low != 1:
		avg = (low + high) // 2
		v = check_fuel(data, avg)
		if v:
			low = avg
		else:
			high = avg
	return low

	
def part_a():
	return find_ore(get_inp())
	
	
def part_b():
	return find_fuel(get_inp())


if __name__ == '__main__':
	print('14A:', part_a())
	print('14B:', part_b())
