import math

with open('09.txt') as f:
    moves = [(y[0], int(y[1])) for y in (x.split(' ') for x in f.read().splitlines())]

head = (0, 0)
rope = [head for _ in range(1, 10)]
tail_visited = set()
tail_visited.add(rope[-1])

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

def is_adj(p1, p2):
    if p1 == p2:
        return True
    if (p1[1] == p2[1]) and (p1[0] == p2[0] - 1 or p1[0] == p2[0] + 1):
        return True
    if (p1[0] == p2[0]) and (p1[1] == p2[1] - 1 or p1[1] == p2[1] + 1):
        return True
    if (abs(p1[0] - p2[0]) == 1 and abs(p1[1] - p2[1]) == 1):
        return True
    return False

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

for move in moves:
    match move[0]:
        case 'R':
            d = (1, 0)
        case 'L':
            d = (-1, 0)
        case 'U':
            d = (0, 1)
        case 'D':
            d = (0, -1)

    #print(move)

    for i in range(0, move[1]):
        head = apply(head, d)

        #print_grid(head, rope, tail_visited)

        prev = head
        for i in range(0, len(rope)):
            knot = rope[i]
            if is_adj(prev, knot):
                prev = rope[i]
                continue

            if knot[0] == prev[0]:
                if knot[1] < prev[1]:
                    knot = apply(knot, (0, 1))
                else:
                    knot = apply(knot, (0, -1))
            elif knot[1] == prev[1]:
                if knot[0] < prev[0]:
                    knot = apply(knot, (1, 0))
                else:
                    knot = apply(knot, (-1, 0))
            else:
                for pm in pos_map.items():
                    test = apply(prev, pm[0])
                    if knot == test:
                        knot = apply(knot, pm[1])
            rope[i] = knot
            prev = rope[i]

            #print_grid(head, rope, tail_visited)

        tail_visited.add(rope[-1])

#print(tail_visited)
print('part2', len(tail_visited))
