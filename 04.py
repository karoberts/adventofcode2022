import re
from collections import defaultdict
from typing import List, Set

groups = []

with open('04.txt') as f:
    lines = f.read().splitlines()
    for line in lines:
        m = re.match(r'^(\d+)-(\d+),(\d+)-(\d+)$', line)
        groups.append( ((int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))) )

def is_inside(g1, g2):
    if g1[0] >= g2[0] and g1[1] <= g2[1]:
        return True
    if g2[0] >= g1[0] and g2[1] <= g1[1]:
        return True
    return False

p1 = sum((1 for g in groups if is_inside(g[0], g[1])))
print('part1', p1)

covereds = []
for g in groups:
    c = set()
    for i in range(g[0][0], g[0][1] + 1): 
        c.add(i)
    for i in range(g[1][0], g[1][1] + 1): 
        if i in c:
            covereds.append(True)
            break

p2 = sum((1 for x in covereds if x))
print('part2', p2)