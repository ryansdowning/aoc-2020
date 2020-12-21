def solve1(nums, target=2020):
    diff = set()
    for num in nums:
        if num in diff:
            return num * (target - num)
        else:
            diff.add(target - num)
    return None


def solve2(nums, target=2020):
    for idx, num in enumerate(nums):
        sub_target = target - num
        if found := solve1(nums[idx:], sub_target):
            return num * found
    return None


if __name__ == "__main__":
    with open('../data/day1.txt', 'r') as f:
        data = f.read().split('\n')
        data = list(map(int, data))
    print(solve1(data))
    print(solve2(data))
