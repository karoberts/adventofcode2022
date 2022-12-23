
from collections import defaultdict
import re

X = 0
Y = 1

grid:dict[tuple] = {}
row_boundaries:defaultdict[int, tuple] = defaultdict(lambda:(9999, -9999))
col_boundaries:defaultdict[int, tuple] = defaultdict(lambda:(9999, -9999))
directions:str = ''

with open('22.txt') as f:
    x = 1
    y = 1
    mode = 'grid'
    for line in f.read().splitlines():
        if line == '':
            mode = 'dir'
            continue
        if mode == 'grid':
            for c in line:
                if c != ' ':
                    rb = row_boundaries[y]
                    row_boundaries[y] = (min(rb[0], x), max(rb[1], x))
                    cb = col_boundaries[x]
                    col_boundaries[x] = (min(cb[0], y), max(cb[1], y))
                    grid[(x,y)] = c
                x += 1
            y += 1
            x = 1
        else:
            directions = line

direc_score_map = {
    1 + 0j: 0,
    0 + 1j: 1,
    -1 + 0j: 2,
    0 - 1j: 3
}

pos = complex(row_boundaries[1][0], 1)
direc = 1 + 0j # facing right

#print('loc', pos, direc)

d_pos = 0
while d_pos < len(directions):
    d = re.match(r'^(\d+|[LR])', directions[d_pos:])
    d_pos += len(d.group(0))
    match d.group(1):
        case 'L':
            #print("turn left", pos, direc)
            direc *= -1j
        case 'R':
            #print("turn right", pos, direc)
            direc *= 1j
        case _:
            #print(f'move {int(d.group(1))} spaces', pos, direc)
            for i in range(0, int(d.group(1))):
                new_pos = pos + direc
                (x,y) = (int(new_pos.real), int(new_pos.imag))
                if int(direc.real) != 0:
                    if x > row_boundaries[y][1]:
                        x = row_boundaries[y][0]
                    if x < row_boundaries[y][0]:
                        x = row_boundaries[y][1]
                else:
                    if y > col_boundaries[x][1]:
                        y = col_boundaries[x][0]
                    if y < col_boundaries[x][0]:
                        y = col_boundaries[x][1]
                if (x,y) in grid and grid[(x,y)] == '#':
                    break
                pos = complex(x, y)

    #print('  to', pos, direc)

print('part1', 1000 * int(pos.imag) + 4 * int(pos.real) + direc_score_map[direc] )

# 139264 too high
