from collections import defaultdict
from math import prod
from typing import DefaultDict, List, Set

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

def count_look(g:DefaultDict, house:tuple, delta:tuple, height:int) -> int:
    def apply(p:tuple, d:tuple):
        return (p[0] + d[0], p[1] + d[1])

    pos = apply(house, delta)
    cur_h = height
    vis = []
    while pos[0] >= 0 and pos[1] >= 0 and pos[0] <= max_x and pos[1] <= max_y:
        vis.append(pos)
        if g[pos] >= cur_h:
            return vis
        pos = apply(pos, delta)
    return vis

scores = []

for y in range(0, max_y + 1):
    for x in range(0, max_x + 1):
        house = (x,y)
        v1 = count_look(grid, house, (-1, 0), grid[house]) 
        v2 = count_look(grid, house, (0, -1), grid[house]) 
        v3 = count_look(grid, house, (1, 0), grid[house])
        v4 = count_look(grid, house, (0, 1), grid[house])
        score = len(v1) * len(v2) * len(v3) * len(v4)
        scores.append(score)

print('part2', max(scores))

