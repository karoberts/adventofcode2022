from collections import defaultdict
from typing import DefaultDict, List, Set

grid = defaultdict(lambda:'.')
elves = set()

X = 0
Y = 1

min_x = 0
min_y = 0
max_x = 0
max_y = 0
start = None
end = None

def print_grid(g):
    for y in range(min_y, max_y + 1):
        for x in range(min_y, max_x + 1):
            if (x,y) in elves:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()

with open('23.txt') as f:
    y = 0
    for line in f.read().splitlines():
        x = 0
        for c in line:
            grid[(x, y)] = '.'
            if c == '#':
                elves.add((x,y))
            x += 1
        y += 1
    min_y = min_x = 0
    max_y = y - 1
    max_x = x - 1

dir_map = {
    'N': (0, -1),
    'NW': (-1, -1),
    'NE': (1, -1),
    'S': (0, 1),
    'SW': (-1, 1),
    'SE': (1, 1),
    'W': (-1, 0),
    'E': (1, 0),
}

adj_map = [
    dir_map['NW'], dir_map['N'], dir_map['NE'],
    dir_map['W'],                dir_map['E'],
    dir_map['SW'], dir_map['S'], dir_map['SE']
]

instructions = [
    ('N', ['N', 'NE', 'NW']),
    ('S', ['S', 'SE', 'SW']),
    ('W', ['W', 'NW', 'SW']),
    ('E', ['E', 'NE', 'SE']),
]

#print_grid(grid)

for round in range(0, 10):
    e_proposals = {}
    n_elves = set()
    for e in elves:
        for a in adj_map:
            if (e[X] + a[X], e[Y] + a[Y]) in elves:
                break
        else:
            n_elves.add(e)
            continue

        for i in instructions:
            for i2 in i[1]:
                d = dir_map[i2]
                p = (e[X] + d[X], e[Y] + d[Y])
                if p in elves:
                    break
            else:
                d2 = dir_map[i[0]]
                e_proposals[e] = (e[X] + d2[X], e[Y] + d2[Y])
                break
        if e not in e_proposals:
            n_elves.add(e)
            continue

    ep_counts = defaultdict(lambda:0)
    for ep in e_proposals.values():
        ep_counts[ep] += 1

    for ep in e_proposals.items():
        if ep_counts[ep[1]] == 1:
            n_elves.add(ep[1])
        else:
            n_elves.add(ep[0])

    elves = n_elves
    instructions.append(instructions.pop(0))
    for e in elves:
        min_y = min(min_y, e[Y])
        min_x = min(min_x, e[X])
        max_y = max(max_y, e[Y])
        max_x = max(max_x, e[X])

    if len(e_proposals) == 0:
        print('done')
        break

    #print_grid(grid)

#print_grid(grid)

min_x = min_y = 9999999
max_x = max_y = -9999999
for e in elves:
    min_y = min(min_y, e[Y])
    min_x = min(min_x, e[X])
    max_y = max(max_y, e[Y])
    max_x = max(max_x, e[X])

c = 0
for y in range(min_y, max_y + 1):
    for x in range(min_y, max_x + 1):
        if (x,y) not in elves:
            c += 1

print('part1', c)