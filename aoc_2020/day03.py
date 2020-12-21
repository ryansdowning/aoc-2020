from functools import reduce


def solve1(grid, rise=1, run=3):
    n = len(grid[0])
    return sum(row[run*idx % n] == '#' for idx, row in enumerate(grid[::rise]))


def solve2(grid, slopes=((1, 1), (1, 3), (1, 5), (1, 7), (2, 1))):
    return reduce(lambda x, y: x * y, [solve1(grid, rise, run) for rise, run in slopes])


if __name__ == "__main__":
    with open('../data/day03.txt', 'r') as f:
        data = f.read().split('\n')
    print(solve1(data))
    print(solve2(data))
