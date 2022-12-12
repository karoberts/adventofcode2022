from collections import defaultdict
from math import prod
from typing import DefaultDict, List, Set
import heapq

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
            match c:
                case 'S':
                    grid[(x,y)] = 0
                    start = (x,y)
                case 'E':
                    grid[(x,y)] = 25
                    end = (x,y)
                case _:
                    grid[(x,y)] = ord(c) - ord('a')
            x += 1
        y += 1
    max_y = y - 1
    max_x = x - 1

# me = (x,y), tgt = (x,y), grid, _max=(max_x, max_y)
def dijkstra(me:tuple[int,int], tgt:tuple[int,int], grid:DefaultDict[tuple[int,int], int], _max:tuple[int,int]) -> int:
    I_COST = 0
    I_X = 1
    I_Y = 2
    I_KEY = 3
    I_VALID = 4

    def get_neighbors(x,y):
        tests = [ (1, 0), (-1, 0), (0, -1), (0, 1) ]
        ns = []

        for t in tests:
            test_x = x + t[0]
            test_y = y + t[1]
            if test_x < 0 or test_y < 0 or test_x > _max[0] or test_y > _max[1]:
                continue
            test_key = (test_x, test_y)

            if grid[test_key] <= grid[(x,y)] + 1:
                # [ cost, x, y, key ]
                ns.append( [1, test_x, test_y, test_key, True] )

        return ns

    dist = defaultdict(lambda:999999999)
    dist[me] = 0
    prev = {me: None}

    h = []
    heapq.heappush(h, [dist[me], me[0], me[1], me, True])
    finder = {me: h[0]}
    inq = set()
    inq.add(me)

    while len(h) > 0:
        u = heapq.heappop(h)
        if not u[I_VALID]:
            continue
        inq.remove(u[I_KEY])
        if u[I_X] == tgt[0] and u[I_Y] == tgt[1]:
            return u[I_COST]
        uk = u[I_KEY]
        for v in get_neighbors(u[I_X], u[I_Y]):
            alt = dist[uk] + v[I_COST]
            if alt < dist[v[I_KEY]]:
                dist[v[I_KEY]] = alt
                prev[v[I_KEY]] = (uk, v[I_COST], v[I_X], v[I_Y])
                entry = [alt, v[I_X], v[I_Y], v[I_KEY], True]
                if v[I_KEY] in inq:
                    finder[v[I_KEY]][I_VALID] = False
                inq.add(v[I_KEY])
                finder[v[I_KEY]] = entry

                heapq.heappush(h, entry)

    return dist[tgt]

#print_grid(grid)

shortest = dijkstra(start, end, grid, (max_x, max_y))
print('part1', shortest)

paths = []
for new_start in (k[0] for k in grid.items() if k[1] == 0):
    paths.append(dijkstra(new_start, end, grid, (max_x, max_y)))
print('part2', min(paths))
