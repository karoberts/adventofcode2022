from collections import defaultdict
from math import prod
import time
from typing import DefaultDict, List, Set
import heapq
import curses

grid = defaultdict(lambda:0)

max_x = 0
max_y = 0
start = None
end = None

def print_grid(g):
    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            print(chr(g[(x,y)] + ord('a')), end='')
        print()
    print()

with open('12.txt') as f:
    y = 0
    for line in f.read().splitlines():
        x = 0
        for c in line:
            if c == 'S':
                grid[(x,y)] = 0
                start = (x,y)
            elif c == 'E':
                grid[(x,y)] = 25
                end = (x,y)
            else:
                grid[(x,y)] = ord(c) - ord('a')
            x += 1
        y += 1
    max_y = y - 1
    max_x = x - 1

# me = [(x,y)], tgt = (x,y), grid, _max=(max_x, max_y)
def dijkstra(me:List[tuple], tgt:tuple, grid:DefaultDict[tuple, int], _max:tuple):
    I_COST = 0
    I_KEY = 1
    I_VALID = 2
    ADJ_TESTS = [ (1, 0), (-1, 0), (0, -1), (0, 1) ]

    def get_neighbors(pos:tuple) -> List[List]:
        ns = []

        for t in ADJ_TESTS:
            test_pos = (pos[0] + t[0], pos[1] + t[1])
            if test_pos[0] < 0 or test_pos[1] < 0 or test_pos[0] > _max[0] or test_pos[1] > _max[1]:
                continue

            if grid[test_pos] <= grid[pos] + 1:
                # [ cost, key, True ]
                ns.append( [1, test_pos, True] )

        return ns

    dist = defaultdict(lambda:999999999)
    prev = {}
    for p_me in me:
        dist[p_me] = 0
        prev[p_me] = None

    h = []
    finder = {}
    inq = set()
    for p_me in me:
        heapq.heappush(h, [dist[p_me], p_me, True])
        finder[p_me] = h[-1]
        inq.add(p_me)

    while len(h) > 0:
        u = heapq.heappop(h)
        if not u[I_VALID]:
            continue
        inq.remove(u[I_KEY])
        if u[I_KEY] == tgt:
            path = []
            p = tgt
            while p != me[0]:
                path.append(p)
                p = prev[p][0]
            path.reverse()

            return (u[I_COST], path)
        uk = u[I_KEY]
        for v in get_neighbors(u[I_KEY]):
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
    
    return (dist[tgt], None)

#print_grid(grid)

(shortest, path) = dijkstra([start], end, grid, (max_x, max_y))
#print('part1', shortest)

#starts = [k[0] for k in grid.items() if k[1] == 0]
#shortest = dijkstra(starts, end, grid, (max_x, max_y))
#print('part2', shortest)

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

    curses.init_color(127, 900, 900, 900)

    curses.init_color(128, 0, 996, 0)
    curses.init_color(129, 308, 964, 0)
    curses.init_color(130, 429, 925, 0)
    curses.init_color(131, 519, 886, 0)
    curses.init_color(132, 589, 847, 0)
    curses.init_color(133, 656, 800, 0)
    curses.init_color(134, 710, 753, 0)
    curses.init_color(135, 761, 703, 0)
    curses.init_color(136, 808, 648, 0)
    curses.init_color(137, 851, 582, 0)
    curses.init_color(138, 894, 507, 0)
    curses.init_color(139, 929, 414, 0)
    curses.init_color(140, 968, 289, 0)
    curses.init_color(141, 996, 93, 93)
    curses.init_color(142, 980, 316, 316)
    curses.init_color(143, 968, 425, 425)
    curses.init_color(144, 964, 507, 507)
    curses.init_color(145, 960, 574, 574)
    curses.init_color(146, 960, 632, 632)
    curses.init_color(147, 960, 687, 687)
    curses.init_color(148, 964, 738, 738)
    curses.init_color(149, 968, 785, 785)
    curses.init_color(150, 972, 832, 832)
    curses.init_color(151, 980, 875, 875)
    curses.init_color(152, 984, 921, 921)
    curses.init_color(153, 992, 960, 960)
    curses.init_color(154, 999, 999, 999)
    curses.init_color(155, 0, 800, 800)
    colors = []
    bgcolors = []
    for i in range(0, 28):
        #curses.init_color(128 + i, i * ((1000//52) + (1000//104)), 1000 - ((i * 1000//52) + (1000//104)), 0)
        curses.init_pair(128 + i, 127, 128 + i)
        curses.init_pair(200 + i, curses.COLOR_BLACK, 128 + i)
        colors.append(curses.color_pair(128 + i))
        bgcolors.append(curses.color_pair(200 + i))

    COLOR_START = 27
    COLOR_TARGET = 26
    COLOR_PATH = curses.color_pair(COLOR_YELLOW_BLACK)

    block = bytes([0xE2,0x96, 0x88])

    def print_grid(g, p):
        path_set = set(p)
        sx = 0
        sy = 0
        rows, cols = stdscr.getmaxyx()
        for y in range(0, max_y + 1):
            for x in range(0, max_x + 1):
                c = (x,y)
                if sx < cols and sy < rows:
                    if c == start:
                        stdscr.addstr(sy, sx, 'S', bgcolors[COLOR_START])
                    elif c == end:
                        stdscr.addstr(sy, sx, 'T', bgcolors[COLOR_TARGET])
                    elif c in path_set:
                        stdscr.addstr(sy, sx, chr(grid[c] + ord('a')), bgcolors[g[c]])
                    else:
                        #stdscr.addstr(sy, sx, chr(grid[c] + ord('a')), colors[g[c]])
                        stdscr.addstr(sy, sx, ' ', colors[g[c]])
                        #stdscr.addstr(sy, sx, block, colors[g[c]])

                #stdscr.getch()
                    
                sx += 1
                #print(chr(g[(x,y)] + ord('a')), end='')
            sx = 0
            sy += 1
        alt = chr(grid[p[-1]] + ord('a'))
        stdscr.addstr(max_y + 2, 0, f'Steps: {len(p) + 1}, Altitude: {alt}')
        stdscr.refresh()

    for i in range(1, len(path)):
        print_grid(grid, path[:i])
        time.sleep(0.010)
    stdscr.getch()

    for i in range(curses.COLORS):
        curses.init_color(i, *save_colors[i])    

curses.wrapper(main)
