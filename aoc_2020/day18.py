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


def parse_main1(toks):
    remaining_toks, expr = parse1(toks)
    if len(remaining_toks) != 1 or not isinstance(remaining_toks[0], TOK_EOF):
        raise ValueError("Tokens remaining after parsing")
    return expr


def parse1(toks):
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


def parse_primary(toks, parser=parse1):
    look = lookahead(toks)
    if isinstance(look, TOK_INT):
        return toks[1:], Int(look.val)
    elif isinstance(look, TOK_LPAREN):
        toks_after_lparen = toks[1:]
        toks_after_parse, expr = parser(toks_after_lparen)
        if isinstance(lookahead(toks_after_parse), TOK_RPAREN):
            return toks_after_parse[1:], expr
        raise ValueError("Did not find matching right parenthesis")
    else:
        raise ValueError("Unexpected token in parse_primary")


def parse_main2(toks):
    remaining_toks, expr = parse2(toks)
    if len(remaining_toks) != 1 or not isinstance(remaining_toks[0], TOK_EOF):
        raise ValueError("Tokens remaining after parsing")
    return expr


def parse2(toks):
    return parse_mult(toks)


def parse_mult(toks):
    toks_after_add, expr1 = parse_add(toks)
    look = lookahead(toks_after_add)
    if isinstance(look, TOK_MULT):
        toks_after_mult = toks_after_add[1:]
        toks_after_parse, expr2 = parse_mult(toks_after_mult)
        return toks_after_parse, Mult(expr1, expr2)
    else:
        return toks_after_add, expr1


def parse_add(toks):
    toks_after_primary, expr1 = parse_primary(toks, parse2)
    look = lookahead(toks_after_primary)
    if isinstance(look, TOK_ADD):
        toks_after_add = toks_after_primary[1:]
        toks_after_parse, expr2 = parse_add(toks_after_add)
        return toks_after_parse, Add(expr1, expr2)
    else:
        return toks_after_primary, expr1


def evaluate(expression):
    if isinstance(expression, Int):
        return expression.val
    elif isinstance(expression, Add):
        return evaluate(expression.a) + evaluate(expression.b)
    elif isinstance(expression, Mult):
        return evaluate(expression.a) * evaluate(expression.b)
    else:
        raise ValueError("Unknown expression encountered ")


def solve1(data):
    total = 0
    for line in data:
        tokens = tokenize(line)
        # Parser is backwards so reverse tokens and flip parenthesesœ
        tokens = ['X' if isinstance(tok, TOK_LPAREN) else tok for tok in tokens]
        tokens = [TOK_LPAREN() if isinstance(tok, TOK_RPAREN) else tok for tok in tokens]
        tokens = [TOK_RPAREN() if isinstance(tok, str) else tok for tok in tokens][::-1][1:] + [TOK_EOF()]
        total += evaluate(parse_main1(tokens))
    return total


def solve2(data):
    return sum(evaluate(parse_main2(tokenize(line))) for line in data)


if __name__ == "__main__":
    with open('../data/day18.txt', 'r') as f:
        data = f.read().split('\n')
    print(solve1(data))
    print(solve2(data))
