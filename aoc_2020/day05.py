def pass_to_id(boarding_pass):
    binary_pass = boarding_pass.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')
    row = int(binary_pass[:7], 2)
    col = int(binary_pass[7:], 2)
    return (row * 8) + col


def solve1(boarding_passes):
    return max(pass_to_id(boarding_pass) for boarding_pass in boarding_passes)


def solve2(boarding_passes):
    seat_ids = [pass_to_id(boarding_pass) for boarding_pass in boarding_passes]
    high = max(seat_ids)
    low = min(seat_ids)
    n = (high * (high + 1) // 2) - ((low - 1) * low // 2)
    total = sum(seat_ids)
    return n - total


if __name__ == "__main__":
    with open('../data/day5.txt', 'r') as f:
        data = f.read().split('\n')
    print(solve1(data))
    print(solve2(data))
