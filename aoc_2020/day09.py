from functools import reduce


def flatten_unique(data):
    return reduce(lambda x, y: x.union(set(y)), data)


def _solve1(data, window=25):
    sums = [{i + j for i in data[:window]} for j in data[:window]]
    unique_sums = flatten_unique(sums)
    for idx, num in enumerate(data[window:], window):
        if num not in unique_sums:
            return idx, num
        new_sums = {i + num for i in data[idx - window:idx]}
        sums = sums[1:] + [new_sums]
        unique_sums = flatten_unique(sums)
    return None, None


def solve1(data, window=25):
    _, num = _solve1(data, window)
    return num


def solve2(data, window=25):
    idx, target = _solve1(data, window)
    arr = data[:idx]
    n = len(arr)
    curr_sum, left, right = 0, 0, 0
    while right < n:
        curr_sum += arr[right]
        right += 1

        while left < n and curr_sum and curr_sum > target:
            curr_sum -= arr[left]
            left += 1

        if curr_sum == target:
            return min(arr[left:right]) + max(arr[left:right])
    return None


if __name__ == "__main__":
    with open('../data/day09.txt', 'r') as f:
        data = f.read().split('\n')
        data = list(map(int, data))
    print(solve1(data))
    print(solve2(data))
