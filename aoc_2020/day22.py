def game_score(deck):
    return sum(i * card for i, card in enumerate(deck[::-1], 1))


def solve1(deck_a, deck_b):
    while deck_a and deck_b:
        a, b = deck_a.pop(0), deck_b.pop(0)
        if a > b:
            deck_a += [a, b]
        else:
            deck_b += [b, a]
    return game_score(deck_a if deck_a else deck_b)


def solve2(deck_a, deck_b):
    def play(deck_a, deck_b):
        mem = set()
        while deck_a and deck_b:
            if (game := (tuple(deck_a), tuple(deck_b))) in mem:
                return 1, deck_a
            mem.add(game)

            a, b = deck_a.pop(0), deck_b.pop(0)
            if len(deck_a) >= a and len(deck_b) >= b:
                winner, _ = play(deck_a[:a], deck_b[:b])
            else:
                winner = int(b > a) + 1

            if winner == 1:
                deck_a += [a, b]
            else:
                deck_b += [b, a]

        return (1, deck_a) if deck_a else (2, deck_b)
    return game_score(play(deck_a, deck_b)[1])


if __name__ == "__main__":
    with open('../data/day22.txt', 'r') as f:
        _, player_a, player_b = f.read().split('Player')
    player_a = list(map(int, player_a[3:].split()))
    player_b = list(map(int, player_b[3:].split()))
    print(solve1(player_a[::], player_b[::]))
    print(solve2(player_a[::], player_b[::]))
