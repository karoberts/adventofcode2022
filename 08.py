from collections import defaultdict
from math import prod
from typing import DefaultDict, Set

grid = defaultdict(lambda:0)

max_x = 0
max_y = 0
with open('08.txt') as f:
    y = 0
    for line in f.read().splitlines():
        x = 0
        for c in line:
            grid[(x,y)] = int(c)
            x += 1
        y += 1
    max_y = y - 1
    max_x = x - 1

visible = set()

def check(g:DefaultDict, x:int, y:int, h:int, visible:Set) -> int:
    c = (x,y)
    if g[c] > h:
        visible.add(c)
        return g[c]
    return h

for y in range(0, max_y + 1):
    cur_h1 = -1
    cur_h2 = -1
    for x in range(0, max_x + 1):
        cur_h1 = check(grid, x, y, cur_h1, visible)
    for x in range(max_x, -1, -1):
        cur_h2 = check(grid, x, y, cur_h2, visible)

for x in range(0, max_x + 1):
    cur_h1 = -1
    cur_h2 = -1
    for y in range(0, max_y + 1):
        cur_h1 = check(grid, x, y, cur_h1, visible)
    for y in range(max_y, -1, -1):
        cur_h2 = check(grid, x, y, cur_h2, visible)

print('part1', len(visible))

"""
for y in range(0, max_y + 1):
    for x in range(0, max_x + 1):
        c = (x,y)
        if c in visible:
            print('*', end='')
        else:
            print(grid[(x,y)], end='')
    print()
"""