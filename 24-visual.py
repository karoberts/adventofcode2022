from collections import defaultdict
import heapq
import time
from typing import DefaultDict, List
import curses

X = 0
Y = 1

min_x = 0
min_y = 0
max_x = 0
max_y = 0
width = 0
height = 0
start = None
end = None

grid:DefaultDict = defaultdict(lambda:'#')
blizzards:dict = {}

dir_map = {
    '^': 'U',
    '>': 'R',
    '<': 'L',
    'v': 'D'
}

dir_map_rev = {v:k for (k,v) in dir_map.items()}

def print_grid(g, bs:dict, me:tuple = None):
    FG_BRI_RED    = '\033[91m'
    MOD_NORMAL    = '\033[0m'
    for y in range(min_y, max_y + 1):
        for x in range(min_y, max_x + 1):
            if (x,y) == me:
                print(FG_BRI_RED + 'E' + MOD_NORMAL, end='')
            elif (x,y) in bs:
                if isinstance(bs[(x,y)], int):
                    print(bs[(x,y)], end='')
                else:
                    print(dir_map_rev[bs[(x,y)]], end='')
            else:
                print(g[(x,y)], end='')
        print()
    print()

with open('24.txt') as f:
    y = 0
    for line in f.read().splitlines():
        x = 0
        for c in line:
            if c == '.':
                grid[(x, y)] = '.'
            elif c in dir_map.keys():
                blizzards[(x,y)] = dir_map[c]
                grid[(x, y)] = '.'
            x += 1
        y += 1
    min_y = min_x = 0
    max_y = y - 1
    max_x = x - 1
    width = max_x - 1
    height = max_y - 1

adj_dir_map = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
}

adj_map:List = [
    adj_dir_map['U'], adj_dir_map['D'], adj_dir_map['L'], adj_dir_map['R']
]

memo:dict = {}
def compute_blizzards(bs:dict, minute:int) -> dict:
    if minute == 0:
        return bs
    if minute in memo:
        return memo[minute]

    new_bs = {}
    for b in bs.items():
        x = b[0][X]
        y = b[0][Y]
        new_pos = None
        if b[1] == 'U':
            y -= 1
            y -= ((minute-1) % height)
            if y <= 0:
                y = height + y

            new_pos = (b[0][X], y)
        elif b[1] == 'D':
            y += 1
            y += ((minute-1) % height)
            if y > height:
                y = y - height

            new_pos = (b[0][X], y)
        elif b[1] == 'L':
            x -= 1
            x -= ((minute-1) % width)
            if x <= 0:
                x = width + x

            new_pos = (x, b[0][Y])
        elif b[1] == 'R':
            x += 1
            x += ((minute-1) % width)
            if x > width:
                x -= width

            new_pos = (x, b[0][Y])

        if new_pos in new_bs:
            if new_bs[new_pos] in adj_dir_map.keys():
                new_bs[new_pos] = 2
            elif isinstance(new_bs[new_pos], int):
                new_bs[new_pos] += 1
        else:
            new_bs[new_pos] = b[1]
    
    memo[minute] = new_bs
    return new_bs

# me = [(x,y)], tgt = (x,y), grid, _max=(max_x, max_y)
def dijkstra(me:tuple, tgt:tuple, bs:dict, init_minute:int, _max:tuple) -> int:
    I_COST = 0
    I_KEY = 1
    I_VALID = 2

    def get_neighbors(pos:tuple, m_next:int) -> List[List]:
        ns = []
        bs_next = compute_blizzards(bs, m_next)

        # wait
        if pos not in bs_next:# and pos != me:
            ns.append( [1, (pos, m_next), True] )

        for t in adj_map:
            test_pos = (pos[0] + t[0], pos[1] + t[1])
            if test_pos == tgt:
                ns.append( [1, (test_pos, m_next), True] )
                break
            if test_pos[X] < 1 or test_pos[Y] < 1 or test_pos[X] >= _max[X] or test_pos[Y] >= _max[Y]:
                continue

            if test_pos not in bs_next:
                ns.append( [1, (test_pos, m_next), True] )

        return ns

    dist = defaultdict(lambda:999999999)
    prev = {}
    dist[(me,init_minute)] = 0
    prev[(me,init_minute)] = None

    h = []
    finder = {}
    inq = set()
    heapq.heappush(h, [0, (me, init_minute), True])
    finder[(me, init_minute)] = h[-1]
    inq.add((me, init_minute))

    while len(h) > 0:
        u = heapq.heappop(h)
        if not u[I_VALID]:
            continue
        inq.remove(u[I_KEY])
        if u[I_KEY][0] == tgt:
            path = []
            p = u[I_KEY]
            while p[0] != me:
                path.append(p)
                p = prev[p][0]
            path.reverse()
            return (u[I_COST], path)
        uk = u[I_KEY]
        for v in get_neighbors(u[I_KEY][0], u[I_KEY][1] + 1):
            alt = dist[uk] + v[I_COST]
            if alt < dist[v[I_KEY]]:
                dist[v[I_KEY]] = alt
                prev[v[I_KEY]] = (uk, v[I_COST])
                entry = [alt, v[I_KEY], True]
                if v[I_KEY] in inq:
                    finder[v[I_KEY]][I_VALID] = False
                inq.add(v[I_KEY])
                finder[v[I_KEY]] = entry

                heapq.heappush(h, entry)

    return dist[tgt]

starting = (1,0)
target = (width, height + 1)

p1 = dijkstra(starting, target, blizzards, 0, (max_x, max_y))
minutes = p1[0]
path = p1[1]

#print('part1', minutes)

p2a = dijkstra(target, starting, blizzards, minutes, (max_x, max_y))
minutes_2 = p2a[0]
path_2 = p2a[1]

p2b = dijkstra(starting, target, blizzards, minutes + minutes_2, (max_x, max_y))
minutes_3 = p2b[0]
path_3 = p2b[1]

#print('part2', sum([minutes, minutes_2, minutes_3]))

def main(stdscr):

    stdscr.clear()
    curses.curs_set(0)
    curses.use_default_colors()
    # save the colors and restore it later
    save_colors = [curses.color_content(i) for i in range(curses.COLORS)]
    stdscr.refresh()

    COLOR_BLACK_WHITE = 0
    COLOR_BLACK_RED = 1
    COLOR_CYAN_BLACK = 2
    COLOR_WHITE_BLACK = 3
    COLOR_YELLOW_BLACK = 4
    COLOR_GREEN_BLACK = 5
    COLOR_BLACK_YELLOW = 6
    COLOR_BLACK_CYAN = 7

    curses.init_pair(COLOR_BLACK_RED, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(COLOR_CYAN_BLACK, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_WHITE_BLACK, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(COLOR_YELLOW_BLACK, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(COLOR_GREEN_BLACK, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_BLACK_YELLOW, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(COLOR_BLACK_CYAN, curses.COLOR_BLACK, curses.COLOR_CYAN)

    COLOR_WALLS = curses.color_pair(COLOR_WHITE_BLACK)
    COLOR_START = curses.color_pair(COLOR_BLACK_RED)
    COLOR_TARGET = curses.color_pair(COLOR_BLACK_CYAN)
    COLOR_PATH = curses.color_pair(COLOR_BLACK_CYAN)
    COLOR_BLIZZARD = curses.color_pair(COLOR_GREEN_BLACK)

    block = bytes([0xE2,0x96, 0x88])

    def print_grid_v(g, bs:dict, p, start, tgt):
        me = p[-1][0]
        sx = 0
        sy = 0
        rows, cols = stdscr.getmaxyx()
        for y in range(0, max_y + 1):
            for x in range(0, max_x + 1):
                c = (x,y)
                if sx < cols and sy < rows:
                    if c == me:
                        stdscr.addstr(sy, sx, 'X', COLOR_PATH)
                    elif c == start:
                        stdscr.addstr(sy, sx, 'S', COLOR_START)
                    elif c == tgt:
                        stdscr.addstr(sy, sx, 'T', COLOR_TARGET)
                    elif c in bs:
                        if isinstance(bs[c], int):
                            stdscr.addstr(sy, sx, str(bs[c]), COLOR_BLIZZARD)
                        elif bs[c] in dir_map_rev:
                            stdscr.addstr(sy, sx, dir_map_rev[bs[c]], COLOR_BLIZZARD)
                        else:
                            stdscr.addstr(sy, sx, '?', COLOR_START)
                    elif g[c] == '#':
                        stdscr.addstr(sy, sx, block, COLOR_WALLS)
                    else:
                        stdscr.addstr(sy, sx, '.', COLOR_WALLS)

                #stdscr.getch()
                    
                sx += 1
            sx = 0
            sy += 1

        if max_y + 4 < rows:
            stdscr.addstr(max_y + 4, 0, f'Minutes: {p[-1][1]}, Position: {me}')
        stdscr.refresh()

    delay = 0.001

    for i in range(1, len(path)):
        print_grid_v(grid, compute_blizzards(blizzards, path[i][1]), path[:i], starting, target)
        time.sleep(delay)
    print_grid_v(grid, compute_blizzards(blizzards, path[-1][1] + 1), [(target,path[-1][1])], starting, target)

    for i in range(1, len(path_2)):
        print_grid_v(grid, compute_blizzards(blizzards, path_2[i][1]), path_2[:i], target, starting)
        time.sleep(delay)
    print_grid_v(grid, compute_blizzards(blizzards, path[-1][1] + 1), [(starting,path_2[-1][1])], target, starting)

    for i in range(1, len(path_3)):
        print_grid_v(grid, compute_blizzards(blizzards, path_3[i][1]), path_3[:i], starting, target)
        time.sleep(delay)
    print_grid_v(grid, compute_blizzards(blizzards, path_3[-1][1] + 1), [(target,path_3[-1][1])], starting, target)
    stdscr.getch()

    for i in range(curses.COLORS):
        curses.init_color(i, *save_colors[i])    

curses.wrapper(main)