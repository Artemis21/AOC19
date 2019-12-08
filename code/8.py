WIDTH = 25
HEIGHT = 6


def get_layers(raw):
    depth = len(raw) / (WIDTH*HEIGHT)
    image = []
    for idx, pixel in enumerate(raw):
        if not idx % (WIDTH*HEIGHT):
            image.append([])
        if not idx % WIDTH:
            image[-1].append([])
        image[-1][-1].append(pixel)
    return image


def get_inp():
    with open('8.txt') as f:
        return f.read().strip()


def draw_image(layers):
    image = [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for layer in reversed(layers):
        for y, row in enumerate(layer):
            for x, pixel in enumerate(row):
                if pixel == '1':
                    image[y][x] = '█'
                elif pixel == '0':
                    image[y][x] = ' '
    print('\n'.join(''.join(i) for i in image))


def part_a():
    raw = get_inp()
    size = WIDTH * HEIGHT
    layers = [raw[i:i + size] for i in range(0, len(raw), size)]
    counts = {}
    for i in layers:
        zeroes = i.count('0')
        ones = i.count('1')
        twos = i.count('2')
        counts[zeroes] = ones * twos
    return counts[min(counts)]


def part_b():
    draw_image(get_layers(get_inp()))
    return 'See above ^^^'


if __name__ == '__main__':
    print('8A:', part_a())
    print('8B:', part_b())
