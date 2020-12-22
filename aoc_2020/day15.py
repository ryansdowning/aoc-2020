def update_memory(num, idx, memory):
    if num in memory:
        old_idx, _ = memory[num]
        memory[num] = (idx, idx - old_idx)
    else:
        memory[num] = (idx, 0)


def solve1(data, rounds=2020):
    memory = dict()
    for idx, num in enumerate(data):
        update_memory(num, idx, memory)

    prev = data[-1]
    for idx in range(len(data), rounds):
        _, diff = memory[prev]
        prev = diff
        update_memory(prev, idx, memory)
    return prev


def solve2(data):
    return solve1(data, 30000000)


if __name__ == "__main__":
    with open('../data/day15.txt', 'r') as f:
        data = list(map(int, f.read().split(',')))
    print(solve1(data))
    print(solve2(data))
