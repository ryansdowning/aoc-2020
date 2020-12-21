import re
REQUIRED = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}


def isvalid_passport(passport):
    return bool(set(passport.keys()).issuperset(REQUIRED))


def solve1(passports):
    return sum(isvalid_passport(passport) for passport in passports)


def isvalid_hgt(hgt):
    if hgt[-2:] == 'cm':
        return 150 <= int(hgt[:-2]) <= 193
    elif hgt[-2:] == 'in':
        return 59 <= int(hgt[:-2]) <= 76
    return False


VALID_ECL = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def solve2(passports):
    def check_passport(passport):
        return (
                isvalid_passport(passport) and
                (1920 <= int(passport['byr']) <= 2002) and
                (2010 <= int(passport['iyr']) <= 2020) and
                (2020 <= int(passport['eyr']) <= 2030) and
                isvalid_hgt(passport['hgt']) and
                (re.match(r"#[a-z0-9]{6}", passport['hcl']) is not None) and
                (passport['ecl'] in VALID_ECL) and
                (len(passport['pid']) == 9 and passport['pid'].isdigit())
        )
    return sum(check_passport(passport) for passport in passports)


if __name__ == "__main__":
    with open('../data/day4.txt', 'r') as f:
        data = f.read().split('\n\n')
        data = [dict(j.split(':') for j in i.split()) for i in data]
    print(solve1(data))
    print(solve2(data))
