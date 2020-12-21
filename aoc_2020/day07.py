from collections import defaultdict
import re
OUTER_RE = r"(?P<outer>[a-z\s]+) bags contain (?:(?:no other bags)|(?P<inner>.*))\."
INNER_RE = r"(?P<num>\d+) (?P<name>[a-z]\s+)(?: ,)?"


def parse_bags(data):
    bags = defaultdict(list)
    for line in data:
        line = re.sub(r" bags?", '', line)
        line = re.match(re.compile(r"(?P<outer>[a-z\s]+) contain (?:(?:no other)|(?P<inner>.*))\."), line)
        if inner := line.group('inner'):
            inner = re.findall(r"(?P<num>\d+) (?P<name>[a-z\s+]+)(?: ,)?", inner)
            inner = list(map(lambda x: (int(x[0]), x[1]), inner))
        else:
            inner = []
        bags[line.group('outer')] = inner
    return bags


def contains_gold(inner, has_gold, bags):
    for num, name in inner:
        if name in has_gold or name == 'shiny gold' or contains_gold(bags[name], has_gold, bags):
            return True
    return False


def solve1(bags):
    has_gold = set()
    for outer, inner in bags.items():
        if contains_gold(inner, has_gold, bags):
            has_gold.add(outer)
    return len(has_gold)


def bags_inside(bag, bags):
    inner = bags[bag]
    if not inner:
        return 1
    return sum(num * bags_inside(name, bags) for num, name in inner) + 1


def solve2(bags):
    return bags_inside('shiny gold', bags) - 1  # bags_inside includes the original bag


if __name__ == "__main__":
    with open('../data/day07.txt', 'r') as f:
        data = f.read().split('\n')
    bags = parse_bags(data)
    print(solve1(bags))
    print(solve2(bags))
