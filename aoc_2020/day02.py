import re


def _parse_password(password):
    if g := re.match(r"(?P<low>\d+)\-(?P<high>\d+) (?P<target>[a-z]): (?P<password>.*)", password):
        return g.groupdict()
    return None


def solve1(passwords):
    def check_pass(password, target, low, high):
        total = sum(1 for i in password if i == target)
        return int(low) <= total <= int(high)

    return sum(check_pass(**_parse_password(password)) for password in passwords)


def solve2(passwords):
    def check_pass(password, target, low, high):
        return (password[int(low) - 1] == target) ^ (password[int(high) - 1] == target)

    return sum(check_pass(**_parse_password(password)) for password in passwords)


if __name__ == "__main__":
    with open('../data/day2.txt', 'r') as f:
        data = f.read().split('\n')
    print(solve1(data))
    print(solve2(data))
