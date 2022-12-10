import math

with open('09.txt') as f:
    moves = [(y[0], int(y[1])) for y in (x.split(' ') for x in f.read().splitlines())]

"""
-- --
-...-
 .H.
-...-
-- --

"""

pos_map = {
    (-2, 1): (1, -1),
    (-2, 2): (1, -1),
    (-1, 2): (1, -1),

    (-2, -1): (1, 1),
    (-2, -2): (1, 1),
    (-1, -2): (1, 1),

    (2, 1): (-1, -1),
    (2, 2): (-1, -1),
    (1, 2): (-1, -1),

    (2, -1): (-1, 1),
    (2, -2): (-1, 1),
    (1, -2): (-1, 1),
}

delta_map = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1)
}

def is_adj(p1, p2):
    x_d = abs(p1[0] - p2[0])
    y_d = abs(p1[1] - p2[1])
    sd = x_d + y_d
    return sd == 1 or sd == 0

def apply(p:tuple, d:tuple):
    return (p[0] + d[0], p[1] + d[1])

def print_grid(h, r, v):
    m = 10
    for y in range(m, -m, -1):
        for x in range(-m, m):
            kid = -1
            for i, k in enumerate(r):
                if (x,y) == k:
                    kid = i
                    break
            if (x,y) == h:
                print('H', end='')
            elif kid >= 0:
                print(kid + 1, end='')
            elif (x,y) == (0,0):
                print('s', end='')
            elif (x,y) in v:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()

def run(rope_len:int):
    head = (0, 0)
    rope = [head for _ in range(1, rope_len + 1)]
    tail_visited = set()
    tail_visited.add(rope[-1])

    for move in moves:
        d = delta_map[move[0]]

        for i in range(0, move[1]):
            head = apply(head, d)

            prev = head
            for i in range(0, len(rope)):
                knot = rope[i]
                if is_adj(prev, knot):
                    prev = rope[i]
                    continue

                if knot[0] == prev[0]:
                    kd = math.copysign(1, prev[1] - knot[1])
                    knot = apply(knot, (0, kd))
                elif knot[1] == prev[1]:
                    kd = math.copysign(1, prev[0] - knot[0])
                    knot = apply(knot, (kd, 0))
                else:
                    for pm in pos_map.items():
                        if knot == apply(prev, pm[0]):
                            knot = apply(knot, pm[1])
                            break
                rope[i] = knot
                prev = rope[i]

            tail_visited.add(rope[-1])
    return len(tail_visited)

print('part1', run(1))
print('part2', run(9))