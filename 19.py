from collections import defaultdict
from copy import copy
from datetime import datetime
from math import prod
import re

ORE = 'o'
CLAY = 'c'
OBSIDIAN = 'ob'
GEODE = 'g'

ore_costs = [-1]
clay_costs = [-1]
obsidian_costs = [-1]
geode_costs = [-1]
max_ore_costs = [-1]

with open('19.txt') as f:
    for line in f.read().splitlines():
        m = re.match(r'^Blueprint (\d+): Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore\. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obsidian\.', line)
        blueprint_id = int(m.group(1))
        ore_costs.append(int(m.group(2)))
        clay_costs.append(int(m.group(3)))
        obsidian_costs.append({ORE: int(m.group(4)), CLAY: int(m.group(5))})
        geode_costs.append({ORE: int(m.group(6)), OBSIDIAN: int(m.group(7))})
        max_ore_costs.append(max(ore_costs[-1], clay_costs[-1], obsidian_costs[-1][ORE], geode_costs[-1][ORE]))

#print(ore_costs)
#print(clay_costs)
#print(obsidian_costs)
#print(geode_costs)

cur_max = 0

def make_key(minute:int, rs:dict, rb:dict, orb:dict, ors:dict, g, ob, c, o):
    return f':[{minute}]{ors[ORE]}=>{rs[ORE]},{ors[CLAY]}=>{rs[CLAY]},{ors[OBSIDIAN]}=>{rs[OBSIDIAN]},{ors[GEODE]}=>{rs[GEODE]} / {orb[ORE]}=>{rb[ORE]},{orb[CLAY]}=>{rb[CLAY]},{orb[OBSIDIAN]}=>{rb[OBSIDIAN]},{orb[GEODE]}=>{rb[GEODE]} ({o},{c},{ob},{g})'

nodes = 0
memo = {}
hits = 0
hits_c = defaultdict(lambda:0)
miss_c = defaultdict(lambda:0)

def evaluate(bp_id:int, resources:dict, robots:dict, minute:int, key:str, tgt:int) -> int:
    global memo
    global hits
    global cur_max
    global nodes

    nodes += 1

    if robots[OBSIDIAN] >= geode_costs[bp_id][OBSIDIAN] and robots[CLAY] >= obsidian_costs[bp_id][CLAY] and robots[ORE] >= max_ore_costs[bp_id]:
        max_expected = resources[GEODE] + robots[GEODE] * (tgt - minute - 3)
        if max_expected < cur_max:
            return -1

    n_geodes = 1 if resources[ORE] >= geode_costs[bp_id][ORE] and resources[OBSIDIAN] >= geode_costs[bp_id][OBSIDIAN] else 0

    if minute == tgt - 2:
        geodes = resources[GEODE] + robots[GEODE] + robots[GEODE] + n_geodes
        if geodes > cur_max:
            cur_max = geodes
            print('rs=', resources, 'ro=', robots, 'm=', minute, 'mx=', cur_max)
        return geodes

    if minute > tgt - 15:
        key = f'{minute}{resources}{robots}'
        if key in memo:
            hits_c[minute] += 1
            hits += 1
            return memo[key]
        else:
            miss_c[minute] += 1
        memo[key] = resources[GEODE]

    max_v = 0

    g = n_geodes
    if True:
        n_obsidian = 1 if g == 0 and resources[ORE] >= obsidian_costs[bp_id][ORE] and resources[CLAY] >= obsidian_costs[bp_id][CLAY] and robots[OBSIDIAN] < geode_costs[bp_id][OBSIDIAN] else 0
        for ob in range(n_obsidian, -1, -1):
            n_clay = 1 if ob == 0 and g == 0 and resources[ORE] >= clay_costs[bp_id] and robots[CLAY] < obsidian_costs[bp_id][CLAY] else 0
            for c in range(n_clay, -1, -1):
                n_ore = 1 if c == 0 and ob == 0 and g == 0 and resources[ORE] >= ore_costs[bp_id] and robots[ORE] < max_ore_costs[bp_id] else 0
                for o in range(n_ore, -1, -1):
                    new_resources = copy(resources)

                    if g == 1 or ob == 1 or c == 1 or o == 1:
                        new_robots = copy(robots)
                        new_robots[ORE] += o
                        new_robots[CLAY] += c
                        new_robots[OBSIDIAN] += ob
                        new_robots[GEODE] += g

                        new_resources[ORE] -= (ore_costs[bp_id] * o + clay_costs[bp_id] * c + obsidian_costs[bp_id][ORE] * ob + geode_costs[bp_id][ORE] * g)
                        new_resources[CLAY] -= obsidian_costs[bp_id][CLAY] * ob
                        new_resources[OBSIDIAN] -= geode_costs[bp_id][OBSIDIAN] * g
                    else:
                        new_robots = robots

                    new_resources[ORE] += robots[ORE]
                    new_resources[CLAY] += robots[CLAY]
                    new_resources[OBSIDIAN] += robots[OBSIDIAN]
                    new_resources[GEODE] += robots[GEODE]

                    max_v = max(max_v, evaluate(bp_id, new_resources, new_robots, minute + 1, '', tgt))

    return max_v

starting_resources = {ORE: 0, CLAY:0, OBSIDIAN:0, GEODE: 0}
starting_robots = {ORE: 1, CLAY:0, OBSIDIAN:0, GEODE: 0}

r_map = {}
if len(ore_costs) < 4:
    r_map[1] = 9
    r_map[2] = 12
    pass
else:
    r_map[1] = 0
    r_map[2] = 15
    r_map[3] = 5
    r_map[4] = 0
    r_map[5] = 9
    r_map[6] = 4
    r_map[7] = 0
    r_map[8] = 0
    r_map[9] = 0
    r_map[10] = 0
    r_map[11] = 2
    r_map[12] = 10
    r_map[13] = 1
    r_map[14] = 1
    r_map[15] = 0
    r_map[16] = 2
    r_map[17] = 0
    r_map[18] = 0
    r_map[19] = 1
    r_map[20] = 5
    r_map[21] = 0
    r_map[22] = 7
    r_map[23] = 8
    r_map[24] = 5
    r_map[25] = 1
    r_map[26] = 0
    r_map[27] = 0
    r_map[28] = 0
    r_map[29] = 7
    r_map[30] = 1

# this will exec the search, about 1 min for part 1
# r_map.clear()

rs = []
for i in range(1, len(ore_costs)):
    if i in r_map:
        #print(f'!! bp {i} max = {r_map[i]}')
        rs.append((i, r_map[i]))
        continue
    cur_max = 0
    node = 0
    memo.clear()
    hits = 0
    r = evaluate(i, copy(starting_resources), copy(starting_robots), 1, '', 25)
    print(f'!! bp {i} max = {r}')
    rs.append((i, r))
#print(rs)

s = sum(r[0] * r[1] for r in rs)
print('part1', s)

if len(ore_costs) < 4:
    print('test mode - quit')
    quit()

r_map.clear()
r_map[1] = 11
r_map[2] = 79
r_map[3] = 43

# this will exec the search, about 5.5min for part 2
#r_map.clear()

rs = []
for i in range(1, 4):
    #print(f'bp {i}')
    if i in r_map:
        #print(f'!! bp {i} max = {r_map[i]}')
        rs.append(r_map[i])
        continue
    cur_max = 0
    node = 0
    memo.clear()
    hits = 0
    r = evaluate(i, copy(starting_resources), copy(starting_robots), 1, '', 33)
    print(f'!! bp {i} max = {r}')
    rs.append(r)

#print(rs)
print('part2', prod(rs))