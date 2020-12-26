import re
from collections import defaultdict

DIR_MAP = {'e': (1, 0), 'w': (-1, 0), 'se': (1, -1), 'sw': (0, -1), 'ne': (0, 1), 'nw': (-1, 1)}
DAYS = 100


def _solve(directions):
    final = defaultdict(int)
    for tile in directions:
        x, y = zip(*tile)
        pos = sum(x), sum(y)
        final[pos] = 1 - final[pos]  # Flip position flag back and forth
    return final


def solve1(directions):
    final = _solve(directions)
    return sum(final.values())


def update_tile(tile, n_black_adj):
    if tile:
        return -int(n_black_adj == 0 or n_black_adj > 2) + 1
    else:
        return int(n_black_adj == 2)


def solve2(directions):
    curr = _solve(directions)
    for _ in range(DAYS):
        today = curr.copy()
        perimeter = set()
        for cx, cy in list(today):
            n_black_adj = 0
            for x, y in DIR_MAP.values():
                adj = (cx + x, cy + y)
                perimeter.add(adj)
                n_black_adj += curr[adj]
            today[(cx, cy)] = update_tile(curr[(cx, cy)], n_black_adj)
        for cx, cy in perimeter:
            today[(cx, cy)] = update_tile(curr[(cx, cy)], sum(curr[(cx + x, cy + y)] for x, y in DIR_MAP.values()))
        curr = today
    return sum(curr.values())


if __name__ == "__main__":
    with open('../data/day24.txt', 'r') as f:
        data = f.read().split('\n')

    def not_empty(vals):
        for val in vals:
            if val:
                return val
        return None
    data = [[DIR_MAP[not_empty(i)] for i in re.findall(r"(se)|(ne)|(sw)|(nw)|(e)|(w)", line)] for line in data]
    print(solve1(data))
    print(solve2(data))
