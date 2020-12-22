import re

INITIAL = "E"
DIRECTIONS = ("E", "N", "W", "S")
DIR_IDX = {"E": 0, "N": 1, "W": 2, "S": 3}


def process_movement(action, value, coords):
    if action == "N":
        coords['y'] += value
    elif action == "S":
        coords['y'] -= value
    elif action == "E":
        coords['x'] += value
    elif action == "W":
        coords['x'] -= value
    return coords


def update_direction(curr_direction, turn, angle):
    angle = (angle % 360) // 90
    curr = DIR_IDX[curr_direction]
    new_dir = (curr + angle) % 4 if turn == "L" else (curr - angle) % 4
    return DIRECTIONS[new_dir]


def solve1(instructions):
    coords = {'x': 0, 'y': 0}
    direction = INITIAL
    for action, value in instructions:
        if action == "L" or action == "R":
            direction = update_direction(direction, action, value)
        elif action == "F":
            coords = process_movement(direction, value, coords)
        else:
            coords = process_movement(action, value, coords)
    return abs(coords['x']) + abs(coords['y'])


WAYPOINT_START = (10, 1)


def update_waypoint(turn, angle, waypoint):
    angle = (angle % 360) // 90
    x, y = waypoint['x'], waypoint['y']
    if turn == "R":
        for _ in range(angle):
            x, y = y, -x
    elif turn == "L":
        for _ in range(angle):
            x, y = -y, x
    waypoint['x'], waypoint['y'] = x, y
    return waypoint


def solve2(instructions):
    waypoint = {'x': WAYPOINT_START[0], 'y': WAYPOINT_START[1]}
    ship = {'x': 0, 'y': 0}
    for action, value in instructions:
        if action == "L" or action == "R":
            waypoint = update_waypoint(action, value, waypoint)
        elif action == "F":
            ship['x'] += waypoint['x'] * value
            ship['y'] += waypoint['y'] * value
        else:
            waypoint = process_movement(action, value, waypoint)
    return abs(ship['x']) + abs(ship['y'])


if __name__ == "__main__":
    with open('../data/day12.txt', 'r') as f:
        data = [
            (action, int(value)) for action, value in
            re.findall(r"([NSEWLRF])(\d+)", f.read())
        ]
    print(solve1(data))
    print(solve2(data))
