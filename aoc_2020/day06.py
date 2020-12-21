from functools import reduce


def solve1(groups):
    def group_yes(group_responses):
        unique = (set(response) for response in group_responses)
        return reduce(lambda x, y: x.union(y), unique)
    return sum(len(group_yes(group)) for group in groups)


def solve2(groups):
    def group_yes(group_responses):
        unique = (set(response) for response in group_responses)
        return reduce(lambda x, y: x.intersection(y), unique)
    return sum(len(group_yes(group)) for group in groups)


if __name__ == "__main__":
    with open('../data/day6.txt', 'r') as f:
        data = f.read().split('\n\n')
        data = [i.split() for i in data]
    print(solve1(data))
    print(solve2(data))
