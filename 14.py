
from collections import defaultdict
from typing import DefaultDict

X = 0
Y = 1

grid:DefaultDict[tuple, str] = defaultdict(lambda:'.')
max_x = (99999999999, -99999999999)
max_y = (99999999999, -99999999999)

def print_grid(g, cur = None):
    for y in range(0 if max_y[0] > 0 else max_y[0], max_y[1] + 1):
        for x in range(max_x[0], max_x[1] + 1):
            if cur is not None and (x,y) == cur:
                print('+', end='')
            else:
                print(g[(x,y)], end='')
        print()
    print()

with open('14.txt') as f:
    for line in f.read().splitlines():
        pts = line.split(' -> ')
        pairs = []
        for p in pts:
            cs = p.split(',')
            pairs.append((int(cs[X]), int(cs[Y])))
        
        for i in range(0, len(pairs) - 1):
            p1 = pairs[i]
            p2 = pairs[i + 1]

            if p1[Y] < max_y[0]: max_y = (p1[Y], max_y[1])
            if p1[Y] > max_y[1]: max_y = (max_y[0], p1[Y])
            if p1[X] < max_x[0]: max_x = (p1[X], max_x[1])
            if p1[X] > max_x[1]: max_x = (max_x[0], p1[X])

            if p2[Y] < max_y[0]: max_y = (p2[Y], max_y[1])
            if p2[Y] > max_y[1]: max_y = (max_y[0], p2[Y])
            if p2[X] < max_x[0]: max_x = (p2[X], max_x[1])
            if p2[X] > max_x[1]: max_x = (max_x[0], p2[X])

            if p1[Y] == p2[Y]:
                if p1[X] < p2[X]:
                    for x in range(p1[X], p2[X] + 1):
                        grid[(x, p1[Y])] = '#'
                else:
                    for x in range(p2[X], p1[X] + 1):
                        grid[(x, p1[Y])] = '#'
            else:
                if p1[Y] < p2[Y]:
                    for y in range(p1[Y], p2[Y] + 1):
                        grid[(p1[X], y)] = '#'
                else:
                    for y in range(p2[Y], p1[Y] + 1):
                        grid[(p1[X], y)] = '#'
                    
def apply(p:tuple, d:tuple):
    return (p[0] + d[0], p[1] + d[1])                    

def drop_sand(g:DefaultDict, cur:tuple) -> tuple:
    below = apply(cur, (0, 1))
    if g[below] == '.': return below

    diag_left = apply(cur, (-1, 1))
    if g[diag_left] == '.': return diag_left

    diag_right = apply(cur, (1, 1))
    if g[diag_right] == '.': return diag_right

    return None

sand_drop = (500, 0)
cur_sand = sand_drop

#print_grid(grid, cur_sand)

units = 0
while True:
    next_sand = drop_sand(grid, cur_sand)
    if next_sand is None:
        units += 1
        grid[cur_sand] = 'o'
        cur_sand = sand_drop
    elif cur_sand[Y] > max_y[1] + 10:
        break
    else:
        cur_sand = next_sand
    #print_grid(grid, cur_sand)

#print_grid(grid)

print('part1', units)