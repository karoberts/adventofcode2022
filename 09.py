import math

with open('09.txt') as f:
    moves = [(y[0], int(y[1])) for y in (x.split(' ') for x in f.read().splitlines())]

head = (0, 0)
tail = head
tail_visited = set()
tail_visited.add(tail)


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
    return False

def apply(p:tuple, d:tuple):
    return (p[0] + d[0], p[1] + d[1])

def print_grid(h, t, v):
    for y in range(5, -2, -1):
        for x in range(-2, 6):
            if (x,y) == h:
                print('H', end='')
            elif (x,y) == t:
                print('T', end='')
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

        if is_adj(head, tail):
            continue

        if tail[0] == head[0]:
            if tail[1] < head[1]:
                tail = apply(tail, (0, 1))
            else:
                tail = apply(tail, (0, -1))
        elif tail[1] == head[1]:
            if tail[0] < head[0]:
                tail = apply(tail, (1, 0))
            else:
                tail = apply(tail, (-1, 0))
        else:
            for pm in pos_map.items():
                test = apply(head, pm[0])
                if tail == test:
                    tail = apply(tail, pm[1])

        tail_visited.add(tail)
        #print_grid(head, tail, tail_visited)

#print(tail_visited)
print('part1', len(tail_visited))
