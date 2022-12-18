from ast import List
from collections import defaultdict
from typing import DefaultDict
from datetime import datetime

X = 0
Y = 1

jets = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

with open('17.txt') as f: jets = f.readline().strip()

shapes = [
    ((0,0), (1,0), (2,0), (3,0)),
    ((1,0), (0,1), (1,1), (2,1), (1,2)),
    ((2,0), (2,1), (0,2), (1,2), (2,2)),
    ((0,0), (0,1), (0,2), (0,3)),
    ((0,0), (1,0), (0,1), (1,1))
]
shape_sizes = [
    (4,1), (3,3), (3,3), (1,4), (2,2)
]


grid:DefaultDict[tuple, str] = defaultdict(lambda:'.')
for x in range(0, 7):
    grid[(x,-1)] = '-'

shape_idx = 0
min_x = 0
max_x = 6
tallest_pt = -1
jet_idx = 0

shape = shapes[shape_idx]
shape_ul = (2, tallest_pt + shape_sizes[shape_idx][Y] + 3)

def detect_collision(s_idx:int, g:DefaultDict, p:tuple):
    for t in shapes[s_idx]:
        test_pos = (p[X] + t[X], p[Y] - t[Y])
        if g[test_pos] != '.' or test_pos[X] < 0 or test_pos[X] >= 7:
            return True
    return False

#print_grid(grid, shape_idx, shape_ul)

# in sample
# repeating pattern every 34 units, 53 total height difference

# in real
# repeating pattern every 1730 units, 2644 total height difference

#pattern = [x for x in [48,50,50,50,52,55,59,59,60,62,63,65,65,66,68,69,71,71,72,75,77,77,77,78,81,84,88,88,89,91,94,94,95,96,99]]
#print(len(pattern))

tgt = 6000 # 1000000000000

pats_y = []
pats_rock = []
pats_tallest = []

bottom = -1
n_rocks = 0
st = datetime.now()
while True:
    shape = shapes[shape_idx]

    if jets[jet_idx] == '<':
        new_pos = (shape_ul[X] - 1, shape_ul[Y])
        if not detect_collision(shape_idx, grid, new_pos):
            shape_ul = new_pos
    else:
        new_pos = (shape_ul[X] + 1, shape_ul[Y])
        if not detect_collision(shape_idx, grid, new_pos):
            shape_ul = new_pos

    jet_idx = (jet_idx + 1) % len(jets)

    #print_grid(grid, shape_idx, shape_ul)
    x = 5

    new_pos = (shape_ul[X], shape_ul[Y] - 1)
    if not detect_collision(shape_idx, grid, new_pos):
        shape_ul = new_pos
    else:
        tallest_pt = max(tallest_pt, shape_ul[Y])
        for t in shape:
            sp = (shape_ul[X] + t[X], shape_ul[Y] - t[Y])
            grid[sp] = '#'
        n_rocks += 1
        #print('rocks', n_rocks, 'height', tallest_pt)
        if n_rocks == 1000000000000:
            break
        if n_rocks % 100_000 == 0:
            print(datetime.now(), datetime.now() - st, n_rocks, tallest_pt + 1, bottom, len(grid))
            st = datetime.now()
        shape_idx = (shape_idx + 1) % len(shapes)
        shape_ul = (2, tallest_pt + shape_sizes[shape_idx][Y] + 3)

        ys = []
        for x in range(0, 7):
            for y in range(tallest_pt, -1, -1):
                if grid[(x,y)] == '#':
                    ys.append(y)
                    break
            else:
                ys.append(0)
        #print(n_rocks, tallest_pt, 'ys', [tallest_pt - y for y in ys])
        #print(tallest_pt - ys[0])
        pats_y.append(tallest_pt - ys[0])
        pats_tallest.append(tallest_pt)
        pats_rock.append(n_rocks)

        if n_rocks >= tgt:
            st = 1730 if len(jets) > 100 else 35
            for ln in range(st, st + 2):
                #print(ln)
                for i in range(0, len(pats_y) - ln):
                    if pats_y[i:i+ln] == pats_y[i+ln:i+ln+ln]:
                        #print('found repeat', i, ln)

                        pats = pats_tallest[i:i+ln]
                        #print(pats)

                        start_rock = i + 1

                        tgt = 1000000000000

                        position = (tgt - start_rock) % ln
                        index = (tgt - start_rock) // ln
                        delta = pats_tallest[start_rock + ln] - pats_tallest[start_rock]
                        starting = index * delta
                        #print('position', position)
                        #print('pattern', pats[position])
                        #print('index', index)
                        #print('starting', starting)
                        #print('height', starting + pats[position] + 1, tallest_pt)
                        print('part2', starting + pats[position] + 1)

                        quit()
            print('none found')
            quit()
