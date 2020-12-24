import re


class Token:
    def __str__(self):
        return type(self).__name__

    def __eq__(self, other):
        return isinstance(other, type(self))


class TOK_EOF(Token):
    pass


class TOK_ADD(Token):
    pass


class TOK_MULT(Token):
    pass


class TOK_LPAREN(Token):
    pass


class TOK_RPAREN(Token):
    pass


class TOK_INT(Token):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return f"{super(TOK_INT, self).__str__()} {self.val}"

    def __eq__(self, other):
        return super(TOK_INT, self).__eq__(other) and other.val == self.val


class Expr:
    def __str__(self):
        return type(self).__name__


class Int(Expr):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return f"Int({self.val})"


class Add(Expr):
    def __init__(self, a: Expr, b: Expr):
        self.a = a
        self.b = b

    def __str__(self):
        return f"Add({self.a}, {self.b})"


class Mult(Expr):
    def __init__(self, a: Expr, b: Expr):
        self.a = a
        self.b = b

    def __str__(self):
        return f"Mult({self.a}, {self.b})"


def lookahead(toks):
    if not toks:
        raise AttributeError("No more tokens")
    return toks[0]


def tokenize(line):
    n = len(line)
    if n == 0:
        return [TOK_EOF()]

    def helper(pos):
        if pos >= n:
            return [TOK_EOF()]
        elif re.match(r"\s", line[pos]):
            return helper(pos+1)
        elif re.match(r"\(", line[pos]):
            return [TOK_LPAREN()] + helper(pos+1)
        elif re.match(r"\)", line[pos]):
            return [TOK_RPAREN()] + helper(pos+1)
        elif re.match(r"\+", line[pos]):
            return [TOK_ADD()] + helper(pos+1)
        elif re.match(r"\*", line[pos]):
            return [TOK_MULT()] + helper(pos+1)
        elif match := re.match(r"\d+", line[pos]):
            return [TOK_INT(int(match.group()))] + helper(pos + match.span()[1])
    return helper(0)


def parse_main(toks):
    remaining_toks, expr = parse(toks)
    if len(remaining_toks) != 1 or not isinstance(remaining_toks[0], TOK_EOF):
        raise ValueError("Tokens remaining after parsing")
    return expr


def parse(toks):
    return parse_operator(toks)


def parse_operator(toks):
    toks_after_primary, expr1 = parse_primary(toks)
    look = lookahead(toks_after_primary)
    if isinstance(look, TOK_ADD):
        toks_after_add = toks_after_primary[1:]
        toks_after_parse, expr2 = parse_operator(toks_after_add)
        return toks_after_parse, Add(expr1, expr2)
    elif isinstance(look, TOK_MULT):
        toks_after_mult = toks_after_primary[1:]
        toks_after_parse, expr2 = parse_operator(toks_after_mult)
        return toks_after_parse, Mult(expr1, expr2)
    else:
        return toks_after_primary, expr1


def parse_primary(toks):
    look = lookahead(toks)
    if isinstance(look, TOK_INT):
        return toks[1:], Int(look.val)
    elif isinstance(look, TOK_LPAREN):
        toks_after_lparen = toks[1:]
        toks_after_parse, expr = parse(toks_after_lparen)
        if isinstance(lookahead(toks_after_parse), TOK_RPAREN):
            return toks_after_parse[1:], expr
        raise ValueError("Did not find matching right parenthesis for left.")
    else:
        raise ValueError("Unexpected token in parse_primary")


def solve1(data):
    pass


def solve2(data):
    pass


if __name__ == "__main__":
    with open('../data/day18_test.txt', 'r') as f:
        data = f.read().split('\n')
    tokens = tokenize(data[0])
    print(data[0])
    print([str(tok) for tok in tokens])
    print(parse_main(tokens))
    # print(solve1(data))
    # print(solve2(data))
