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

# me = [(x,y)], tgt = (x,y), grid, _max=(max_x, max_y)
def dijkstra(me:List[tuple[int,int]], tgt:tuple[int,int], grid:DefaultDict[tuple[int,int], int], _max:tuple[int,int]) -> int:
    I_COST = 0
    I_KEY = 1
    I_VALID = 2
    ADJ_TESTS = [ (1, 0), (-1, 0), (0, -1), (0, 1) ]

    def get_neighbors(pos:tuple[int,int]) -> List[List]:
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
            return u[I_COST]
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

    return dist[tgt]

#print_grid(grid)

shortest = dijkstra([start], end, grid, (max_x, max_y))
print('part1', shortest)

starts = [k[0] for k in grid.items() if k[1] == 0]
shortest = dijkstra(starts, end, grid, (max_x, max_y))
print('part2', shortest)
