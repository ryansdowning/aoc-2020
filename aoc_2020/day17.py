import numpy as np
from scipy.ndimage import generic_filter

CYCLES = 6


def _solve(data, dim):
    """
    Very interesting solution I found on reddit that utilizes scipy ndimage to construct the n-dimensional space
    dynamically using the given function.
    """
    def func(x):
        if x[len(x) // 2] == 0:
            return int(np.sum(x) == 3)
        else:
            return int(np.sum(x) in (3, 4))

    d = 20
    a = (np.array(data) == "#").astype(np.uint8)
    for _ in range(dim-2):
        a = np.reshape(a, (1,)+a.shape)
    arr = np.pad(a, (d-a.shape[0]) // 2)
    kernel = np.ones([3]*dim, dtype=np.uint8)
    for i in range(CYCLES):
        arr = generic_filter(arr, func, footprint=kernel, mode="constant", cval=0)
    return np.sum(arr)


def solve1(data):
    return _solve(data, 3)


def solve2(data):
    return _solve(data, 4)


if __name__ == "__main__":
    with open('../data/day17.txt', 'r') as f:
        data = [list(line.strip()) for line in f.readlines()]
    print(solve1(data))
    print(solve2(data))
