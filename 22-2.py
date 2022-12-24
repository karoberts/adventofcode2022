
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

RIGHT = 1 + 0j
LEFT = -1 + 0j
UP = -1j
DOWN = 0 + 1j

direc_score_map = {
    RIGHT: 0,
    DOWN: 1,
    LEFT: 2,
    UP: 3
}

edge_map = {}

def match_direc(direc):
    if direc == UP: return '^'
    elif direc == RIGHT: return '>'
    elif direc == DOWN: return 'v'
    elif direc == LEFT: return '<'

if row_boundaries[1][0] < 40:
    y_end_print = 14
    x_end_print = 18
    xs = row_boundaries[1][0]
    xe = row_boundaries[1][1]
    for y in range(1, 5):
        # left of 1 to top of 3
        edge_map[(xs - 1, y, LEFT)] = (y + 4, 5, DOWN)
        # top of 3 to left of 1
        edge_map[(y + 4, 4, UP)] = (xs, y, RIGHT)

        # right of 1 to right of 6
        edge_map[(xe + 1, y, RIGHT)] = (16, 5 - y + row_boundaries[y][1] - 4, LEFT)
        # right of 6 to right of 1
        edge_map[(17, 5 - y + row_boundaries[y][1] - 4, RIGHT)] = (xe, y, LEFT)

        # left of 2 to bottom of 6
        edge_map[(0, col_boundaries[1][0] + y - 1, LEFT)] = (12 + 5 - y, 12, UP)
        # bottom of 6 to left of 2
        edge_map[(12 + y, col_boundaries[9][1] + 1, DOWN)] = (1, col_boundaries[1][0] + 5 - y - 1, RIGHT)

        # right of 4 to top of 6
        edge_map[(13, 4 + y, RIGHT)] = (12 + 5 - y, 9, DOWN)
        # top of 6 to right of 4 
        edge_map[(12 + 5 - y, 8, UP)] = (12, col_boundaries[1][0] + y - 1, LEFT)
        pass

    for x in range(1, 5):
        # top of 1 to top of 2
        edge_map[(xs + x - 1, 0, UP)] = (5 - x, col_boundaries[x][0], DOWN)
        # top of 2 to top of 1
        edge_map[(5 - x, col_boundaries[x][0] - 1, UP)] = (xs + x - 1, 1, DOWN)

        # bottom of 2 to bottom of 5
        edge_map[(x, 9, DOWN)] = (5 - x + 8, 12, UP)
        # bottom of 5 to bottom of 2
        edge_map[(5 - x + 8, 13, DOWN)] = (x, 8, UP)

        # bottom of 3 to left of 5
        edge_map[(5 - x + 4, 9, DOWN)] = (9, 8 + x, RIGHT)
        # left of 5 to bottom of 3
        edge_map[(8, x + 8, LEFT)] = (5 - x + 4, 8, UP)

        pass
else:
    y_end_print = 202
    x_end_print = 152

    xs = row_boundaries[1][0]
    xe = row_boundaries[1][1]
    for x in range(1, 51):
        # top of 1 to left of 6
        edge_map[(xs + x - 1, 0, UP)] = (1, 150 + x, RIGHT)
        # left of 6 to top of 1
        edge_map[(0, 150 + x, LEFT)] = (xs + x - 1, 1, DOWN)

        # top of 2 to bottom of 6
        edge_map[(xs + x + 49, 0, UP)] = (x, 200, UP)
        # bottom of 6 to top of 2
        edge_map[(x, 201, DOWN)] = (xs + x + 49, 1, DOWN)

        # right of 2 to right of 5
        edge_map[(151, x, RIGHT)] = (100, 100 + 51 - x, LEFT)
        # right of 5 to right of 2
        edge_map[(101, 100 + 51 - x, RIGHT)] = (150, x, LEFT)

        # bottom of 2 to right of 3
        edge_map[(100 + x, 51, DOWN)] = (100, 50 + x, LEFT)
        # right of 3 to bottom of 2
        edge_map[(101, 50 + x, RIGHT)] = (100 + x, 50, UP)

        # left of 1 to left of 4
        edge_map[(50, x, LEFT)] = (1, 51 - x + 100, RIGHT)
        # left of 4 to left of 1
        edge_map[(0, 51 - x + 100, LEFT)] = (51, x, RIGHT)

        # left of 3 to top of 4
        edge_map[(50, x + 50, LEFT)] = (x, 101, DOWN)
        # top of 4 to left of 3
        edge_map[(x, 100, UP)] = (51, x + 50, RIGHT)

        # bottom of 5 to right of 6
        edge_map[(50 + x, 151, DOWN)] = (50, 150 + x, LEFT)
        # right of 6 to bottom of 5
        edge_map[(51, 150 + x, RIGHT)] = (50 + x, 150, UP)


edge_map_coords = dict((((e[0], e[1]), match_direc(e[2])) for e in edge_map.values()))

def print_it(p):
    MOD_NORMAL = '\033[0m'
    FG_MAGENTA   = '\033[35m'
    FG_BRI_GREEN  = '\033[92m'

    for y in range(-2, y_end_print):
        for x in range(-2, x_end_print):
            c = (x,y)
            #if (x, y, LEFT) in edge_map:
            #    print('<', end='')
            #elif (x, y, UP)  in edge_map:
            #    print('^', end='')
            #elif (x, y, RIGHT)  in edge_map:
            #    print('>', end='')
            #elif (x, y, DOWN)  in edge_map:
            #    print('v', end='')
            #elif c in edge_map_coords:
            #    print(FG_MAGENTA + edge_map_coords[c] + MOD_NORMAL, end='')
            if c in grid:
                if p == c:
                    print(FG_MAGENTA + grid[c] + MOD_NORMAL, end='')
                elif c == (row_boundaries[1][0], 1):
                    print(FG_BRI_GREEN + grid[c] + MOD_NORMAL, end='')
                else:
                    print(grid[c], end='')
            else:
                print(' ', end='')
        print()

#print_it(None)
#quit()

pos = complex(row_boundaries[1][0], 1)
direc = 1 + 0j # facing right

grid[(int(pos.real), int(pos.imag))] = '>'

#print('loc', pos, direc)

d_pos = 0
while d_pos < len(directions):
    d = re.match(r'^(\d+|[LR])', directions[d_pos:])
    d_pos += len(d.group(0))
    (x,y) = (int(pos.real), int(pos.imag))
    match d.group(1):
        case 'L':
            #print("turn left", pos, match_direc(direc))
            direc *= -1j
            grid[(x,y)] = match_direc(direc)
        case 'R':
            #print("turn right", pos, direc)
            direc *= 1j
            grid[(x,y)] = match_direc(direc)
        case _:
            #print(f'move {int(d.group(1))} spaces', pos, match_direc(direc))
            for i in range(0, int(d.group(1))):
                new_pos = pos + direc
                (x,y) = (int(new_pos.real), int(new_pos.imag))
                new_direc = direc
                if (x,y,direc) in edge_map:
                    #print('  cube move', x,y,match_direc(direc), 'to', edge_map[(x,y,direc)])
                    (x,y,new_direc) = edge_map[(x,y,direc)]
                if (x,y) in grid and grid[(x,y)] == '#':
                    break
                direc = new_direc
                grid[(x,y)] = match_direc(direc)
                pos = complex(x, y)

    #print('  to', pos, match_direc(direc))

#(x,y) = (int(pos.real), int(pos.imag))
#print_it((x,y))

print('part2', 1000 * int(pos.imag) + 4 * int(pos.real) + direc_score_map[direc] )

