def process(operations):
    acc = 0
    count = 0
    executed = set()
    n = len(operations)
    while count < n and count not in executed:
        executed.add(count)
        operation, value = operations[count]
        value = int(value)
        if operation == 'acc':
            acc += value
        elif operation == 'jmp':
            count += value - 1  # decrement to account for auto-increment
        count += 1
    return count == n and count not in executed, acc


def solve1(operations):
    _, acc = process(operations)
    return acc


OPERATION_MAP = {"nop": "jmp", "jmp": "nop", "acc": "acc"}


def solve2(operations):
    for idx, (operation, value) in enumerate(operations):
        operations[idx][0] = OPERATION_MAP[operation]
        completed, acc = process(operations)
        if completed:
            return acc
        operations[idx][0] = operation
    return None


if __name__ == "__main__":
    with open('../data/day8.txt', 'r') as f:
        data = f.read().split('\n')
        data = [i.split() for i in data]
    print(solve1(data))
    print(solve2(data))
