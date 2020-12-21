from copy import deepcopy

FLOOR = "."
EMPTY = "L"
OCCUPIED = "#"
ADJ = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def num_adj_occupied(i, j, grid):
    count = 0
    m, n = len(grid)-1, len(grid[0])-1
    for dx, dy in ADJ:
        di, dj = i+dx, j+dy
        if 0 <= di <= m and 0 <= dj <= n and grid[di][dj] == OCCUPIED:
            count += 1
    return count


def _solve(grid, occupy_func, seat_tolerance):
    while True:
        new_grid = deepcopy(grid)
        for i, row in enumerate(grid):
            for j, seat in enumerate(row):
                if seat == FLOOR:
                    continue
                num_occupied = occupy_func(i, j, grid)
                if seat == EMPTY and num_occupied == 0:
                    new_grid[i][j] = OCCUPIED
                elif seat == OCCUPIED and num_occupied >= seat_tolerance:
                    new_grid[i][j] = EMPTY
        if new_grid == grid:
            break
        else:
            grid = new_grid
    return sum(sum(seat == OCCUPIED for seat in row) for row in grid)


def solve1(grid):
    return _solve(grid, num_adj_occupied, 4)


def num_visible_occupied(i, j, grid):
    count = 0
    m, n = len(grid) - 1, len(grid[0]) - 1
    for dx, dy in ADJ:
        di, dj = i, j
        while True:
            di, dj = di+dx, dj+dy
            if 0 > di or di > m or 0 > dj or dj > n:
                break
            elif grid[di][dj] == OCCUPIED:
                count += 1
                break
            elif grid[di][dj] == EMPTY:
                break
    return count


def solve2(grid):
    return _solve(grid, num_visible_occupied, 5)


if __name__ == "__main__":
    with open('../data/day11.txt', 'r') as f:
        data = f.read().split('\n')
        data = [list(line) for line in data]
    print(solve1(data))
    print(solve2(data))
