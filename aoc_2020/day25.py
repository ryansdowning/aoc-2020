SUBJECT = 7
R = 20201227


def get_loop_size(key):
    val = 1
    c = 0
    while val != key:
        val = val * SUBJECT % R
        c += 1
    return c


def solve1(card, door):
    card_loop = get_loop_size(card)
    val = 1
    for _ in range(card_loop):
        val = val * door % R
    return val


if __name__ == "__main__":
    with open('../data/day25.txt', 'r') as f:
        data = f.read().split('\n')
    data = list(map(int, data))
    print(solve1(*data))
