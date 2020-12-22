import re
from itertools import combinations


def solve1(data):
    mem = dict()
    mask_and, mask_or = 2**37-1, 0
    for mask, address, num in data:
        if mask:
            mask_and = int(mask.replace('X', '1'), 2)
            mask_or = int(mask.replace('X', '0'), 2)
        elif address and num:
            mem[address] = (int(num) & mask_and) | mask_or
    return sum(mem.values())


def address_combinations(address, mask_combs, mask_floating):
    a = ["0" if idx in mask_floating else i for idx, i in enumerate(address)]
    for mask in mask_combs:
        perm = a[::]
        for idx in mask:
            perm[idx] = "1"
        yield ''.join(perm)
    yield ''.join(a)


def mask_combinations(floating_idxs):
    return [comb for i in range(1, len(floating_idxs)+1) for comb in combinations(floating_idxs, i)]


def solve2(data):
    mem = dict()
    mask_or, mask_floating, mask_combs = set(), set(), []
    for mask, address, num in data:
        if mask:
            mask_or = int(mask.replace('X', '0'), 2)
            mask_floating = {idx for idx, bit in enumerate(mask) if bit == 'X'}
            mask_combs = mask_combinations(mask_floating)
        elif address and num:
            address = bin(int(address) | mask_or)[2:]
            address = ("0" * (36 - len(address))) + address
            num = int(num)
            for comb in address_combinations(address, mask_combs, mask_floating):
                mem[comb] = num
    return sum(mem.values())


if __name__ == "__main__":
    with open('../data/day14.txt', 'r') as f:
        data = re.findall(r"(?:mask = ([01X]+))|(?:mem\[(\d+)] = (\d+))", f.read())
    print(solve1(data))
    print(solve2(data))
