def parse_subrule(rules, subrule, string):
    if not subrule:
        yield string
    else:
        r, *remaining_rules = subrule
        for s in parse_rule(rules, r, string):
            yield from parse_subrule(rules, remaining_rules, s)


def expand_rule(rules, rule, string):
    for subrule in rule:
        yield from parse_subrule(rules, subrule, string)


def parse_rule(rules, rule_id, string):
    if isinstance(rules[rule_id], list):
        yield from expand_rule(rules, rules[rule_id], string)
    else:
        if string and string[0] == rules[rule_id]:
            yield string[1:]


def accept_string(rules, string, rule_id='0'):
    return any(m == '' for m in parse_rule(rules, rule_id, string))


def solve1(rules, messages):
    return sum(accept_string(rules, message) for message in messages)


def solve2(rules, messages):
    rules['8'] = [['42'], ['42', '8']]
    rules['11'] = [['42', '31'], ['42', '11', '31']]
    return sum(accept_string(rules, message) for message in messages)


if __name__ == "__main__":
    with open('../data/day19.txt', 'r') as f:
        rules_text, messages = f.read().split('\n\n')
    rules_dict = dict()
    for rule_text in rules_text.split('\n'):
        num, rule = rule_text.split(': ')
        if rule[0] == '"':
            rule = rule[1]
        else:
            rule = [subrule.split() for subrule in rule.split(' | ')]
        rules_dict[num] = rule
    messages = messages.split('\n')
    print(solve1(rules_dict, messages))
    print(solve2(rules_dict, messages))
