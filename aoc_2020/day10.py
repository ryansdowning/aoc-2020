from collections import Counter


def solve1(adapters):
    sorted_adapters = sorted(adapters)
    consecutive_pairs = zip(sorted_adapters[1:], sorted_adapters)
    diffs = [i - j for i, j in consecutive_pairs]
    count = Counter(diffs)
    count[sorted_adapters[0]] += 1   # First 0 -> n adapter
    count[3] += 1  # Last n -> n + 3 adapter
    return count[1] * count[3]


def solve2(adapters):
    sorted_adapters = sorted(adapters)
    max_adapter = sorted_adapters[-1] + 3
    sorted_adapters.append(max_adapter)
    partial_sums = [0 for _ in range(max_adapter + 1)]
    partial_sums[0] = 1
    for adapter in sorted_adapters:
        partial_sums[adapter] = sum(partial_sums[max(0, adapter - 3): adapter])
    return partial_sums[max_adapter]


if __name__ == "__main__":
    with open('../data/day10.txt', 'r') as f:
        data = f.read().split('\n')
        data = list(map(int, data))
    print(solve1(data))
    print(solve2(data))
