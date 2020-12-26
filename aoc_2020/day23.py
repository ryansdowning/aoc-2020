from itertools import count


def play(cups, rounds):
    cup_hash = {i: j for i, j in zip(cups, cups[1:] + [cups[0]])}
    curr = cups[0]
    n = len(cups)
    for _ in range(rounds):
        i = curr
        pickup = [i := cup_hash[i] for _ in range(3)]
        dest = next(
            cup for i in count(1)
            if (cup if (cup := curr - i) > 0 else (cup := n + cup)) not in pickup
        )

        cup_hash[curr], cup_hash[pickup[-1]], cup_hash[dest] = cup_hash[pickup[-1]], cup_hash[dest], cup_hash[curr]
        curr = cup_hash[curr]

    idx = 1
    return [idx := cup_hash[idx] for _ in cups[:-1]]


def solve1(cups):
    return ''.join(map(str, play(cups, 100)))


def solve2(cups):
    cups = cups + list(range(len(cups) + 1, 1_000_001))
    result = play(cups, 10_000_000)
    return result[0] * result[1]


if __name__ == "__main__":
    with open('../data/day23.txt', 'r') as f:
        data = list(map(int, f.read().strip()))
    print(solve1(data))
    print(solve2(data))
