from ast import List
from collections import defaultdict
from typing import DefaultDict

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

def print_grid(g:DefaultDict, s_idx:int, sp:tuple):
    global tallest_pt
    sh = set((sp[X] + t[X], sp[Y] - t[Y]) for t in shapes[s_idx]) if s_idx is not None else set()
    y_start = shape_sizes[s_idx][Y] if s_idx is not None else 0
    for y in range(tallest_pt + 4 + y_start, -2, -1):
        for x in range(-1, 8):
            if x == -1 or x == 7:
                if y == -1:
                    print('+', end='')
                else:
                    print('|', end='')
            elif y == -1:
                print('-', end='')
            elif (x,y) in sh:
                print('@', end='')
            elif y == tallest_pt:
                print('\033[91m' + g[x,y] + '\033[0m', end='')
            else:
                print(g[x,y], end='')
        print()
    print()

#print_grid(grid, shape_idx, shape_ul)

n_rocks = 0
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
        if n_rocks == 2022:
            break
        shape_idx = (shape_idx + 1) % len(shapes)
        shape_ul = (2, tallest_pt + shape_sizes[shape_idx][Y] + 3)

    #print_grid(grid, shape_idx, shape_ul)
    x = 5

#print_grid(grid, None, None)
#print('rocks', n_rocks, 'height', tallest_pt)
print('part1', tallest_pt + 1) 

        

