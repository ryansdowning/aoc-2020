from functools import reduce


def solve1(start, buses):
    buses = [bus for bus in buses if bus != 'x']
    delays = {bus: bus - (start % bus) for bus in buses}
    closest_bus = min(delays, key=lambda x: delays[x])
    return closest_bus * delays[closest_bus]


def solve2(buses):
    mods = {}
    for idx, bus in enumerate(buses):
        if bus != 'x':
            mods[bus] = -idx % bus

    total = 0
    count = 1
    for bus in mods:
        while total % bus != mods[bus]:
            total += count
        count *= bus

    return total


if __name__ == "__main__":
    with open('../data/day13.txt', 'r') as f:
        data = f.read().split('\n')
        start = int(data[0])
        buses = [int(i) if i != 'x' else i for i in data[1].split(',')]
    print(solve1(start, buses))
    print(solve2(buses))
