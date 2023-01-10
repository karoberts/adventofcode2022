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
memo = defaultdict(lambda:-1)

def make_key(minute:int, rs:dict, rb:dict, orb:dict, ors:dict, g, ob, c, o):
    return f':[{minute}]{ors[ORE]}=>{rs[ORE]},{ors[CLAY]}=>{rs[CLAY]},{ors[OBSIDIAN]}=>{rs[OBSIDIAN]},{ors[GEODE]}=>{rs[GEODE]} / {orb[ORE]}=>{rb[ORE]},{orb[CLAY]}=>{rb[CLAY]},{orb[OBSIDIAN]}=>{rb[OBSIDIAN]},{orb[GEODE]}=>{rb[GEODE]} ({o},{c},{ob},{g})'

def evaluate(bp_id:int, resources:dict, robots:dict, minute:int, tgt:int) -> int:
    global cur_max
    global memo

    if minute == tgt:
        #if resources[GEODE] > cur_max:
        #    cur_max = resources[GEODE]
        #    print('rs=', resources, 'ro=', robots, 'm=', minute, 'mx=', cur_max)
        return resources[GEODE]

    max_v = resources[GEODE]

    made_g = False
    made_ob = False
    made_c = False
    made_o = False

    if resources[GEODE] > memo[minute]:
        memo[minute] = resources[GEODE]
    elif resources[GEODE] < memo[minute]:
        return -1

    for m in range(minute, tgt):
        if made_g and (made_ob or robots[OBSIDIAN] >= geode_costs[bp_id][OBSIDIAN]) and (made_c or robots[CLAY] >= obsidian_costs[bp_id][CLAY]) and (made_o or robots[ORE] >= max_ore_costs[bp_id]):
            break

        if not made_g and resources[ORE] >= geode_costs[bp_id][ORE] and resources[OBSIDIAN] >= geode_costs[bp_id][OBSIDIAN]:
            next_resources = copy(resources)
            next_resources[ORE] -= geode_costs[bp_id][ORE]
            next_resources[OBSIDIAN] -= geode_costs[bp_id][OBSIDIAN]

            next_resources[ORE] += robots[ORE]
            next_resources[CLAY] += robots[CLAY]
            next_resources[OBSIDIAN] += robots[OBSIDIAN]
            next_resources[GEODE] += robots[GEODE]

            robots[GEODE] += 1
            max_v = max(max_v, evaluate(bp_id, next_resources, robots, m + 1, tgt))
            robots[GEODE] -= 1
            made_g = True

        if not made_ob and resources[ORE] >= obsidian_costs[bp_id][ORE] and resources[CLAY] >= obsidian_costs[bp_id][CLAY] and robots[OBSIDIAN] < geode_costs[bp_id][OBSIDIAN]:
            next_resources = copy(resources)
            next_resources[ORE] -= obsidian_costs[bp_id][ORE]
            next_resources[CLAY] -= obsidian_costs[bp_id][CLAY]

            next_resources[ORE] += robots[ORE]
            next_resources[CLAY] += robots[CLAY]
            next_resources[OBSIDIAN] += robots[OBSIDIAN]
            next_resources[GEODE] += robots[GEODE]

            robots[OBSIDIAN] += 1
            max_v = max(max_v, evaluate(bp_id, next_resources, robots, m + 1, tgt))
            robots[OBSIDIAN] -= 1
            made_ob = True
            
        if not made_c and resources[ORE] >= clay_costs[bp_id] and robots[CLAY] < obsidian_costs[bp_id][CLAY]:
            next_resources = copy(resources)
            next_resources[ORE] -= clay_costs[bp_id]

            next_resources[ORE] += robots[ORE]
            next_resources[CLAY] += robots[CLAY]
            next_resources[OBSIDIAN] += robots[OBSIDIAN]
            next_resources[GEODE] += robots[GEODE]

            robots[CLAY] += 1
            max_v = max(max_v, evaluate(bp_id, next_resources, robots, m + 1, tgt))
            robots[CLAY] -= 1
            made_c = True

        if not made_o and resources[ORE] >= ore_costs[bp_id] and robots[ORE] < max_ore_costs[bp_id]:
            next_resources = copy(resources)
            next_resources[ORE] -= ore_costs[bp_id]

            next_resources[ORE] += robots[ORE]
            next_resources[CLAY] += robots[CLAY]
            next_resources[OBSIDIAN] += robots[OBSIDIAN]
            next_resources[GEODE] += robots[GEODE]

            robots[ORE] += 1
            max_v = max(max_v, evaluate(bp_id, next_resources, robots, m + 1, tgt))
            robots[ORE] -= 1
            made_o = True

        resources[ORE] += robots[ORE]
        resources[CLAY] += robots[CLAY]
        resources[OBSIDIAN] += robots[OBSIDIAN]
        resources[GEODE] += robots[GEODE]

    return max_v


starting_resources = {ORE: 0, CLAY:0, OBSIDIAN:0, GEODE: 0}
starting_robots = {ORE: 1, CLAY:0, OBSIDIAN:0, GEODE: 0}

rs = []
for i in range(1, len(ore_costs)):
    cur_max = 0
    memo.clear()
    r = evaluate(i, copy(starting_resources), copy(starting_robots), 1, 25)
    #print(f'!! bp {i} max = {r}')
    rs.append((i, r))

s = sum(r[0] * r[1] for r in rs)
print('part1', s)

rs = []
for i in range(1, min(len(ore_costs), 4)):
    cur_max = 0
    memo.clear()
    r = evaluate(i, copy(starting_resources), copy(starting_robots), 1, 33)
    #print(f'!! bp {i} max = {r}')
    rs.append(r)

#print(rs)
print('part2', prod(rs))