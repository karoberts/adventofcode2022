from copy import copy, deepcopy
from datetime import datetime
import re

ORE = 'o'
CLAY = 'c'
OBSIDIAN = 'ob'
GEODE = 'g'

ore_costs = [-1]
clay_costs = [-1]
obsidian_costs = [-1]
geode_costs = [-1]

with open('19.txt') as f:
    for line in f.read().splitlines():
        m = re.match(r'^Blueprint (\d+): Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore\. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obsidian\.', line)
        blueprint_id = int(m.group(1))
        ore_costs.append(int(m.group(2)))
        clay_costs.append(int(m.group(3)))
        obsidian_costs.append({ORE: int(m.group(4)), CLAY: int(m.group(5))})
        geode_costs.append({ORE: int(m.group(6)), OBSIDIAN: int(m.group(7))})

#print(ore_costs)
#print(clay_costs)
#print(obsidian_costs)
#print(geode_costs)

cur_max = 0

def count_ore(bp_id:int, ore:int):
    return 1 if ore > ore_costs[bp_id] else 0

def make_key(minute:int, rs:dict, rb:dict, orb:dict, ors:dict, g, ob, c, o):
    return f':[{minute}]{ors[ORE]}=>{rs[ORE]},{ors[CLAY]}=>{rs[CLAY]},{ors[OBSIDIAN]}=>{rs[OBSIDIAN]},{ors[GEODE]}=>{rs[GEODE]} / {orb[ORE]}=>{rb[ORE]},{orb[CLAY]}=>{rb[CLAY]},{orb[OBSIDIAN]}=>{rb[OBSIDIAN]},{orb[GEODE]}=>{rb[GEODE]} ({o},{c},{ob},{g})'

nodes = 0
memo = {}
hits = 0

def evaluate(bp_id:int, resources:dict, robots:dict, minute:int, key:str) -> int:
    global memo
    global hits
    global cur_max
    global nodes

    #print('rs=', resources, 'ro=', robots, 'm=', minute, 'mx=', cur_max)

    nodes += 1

    key = f'{minute}{resources}{robots}'
    if key in memo:
        hits += 1
        return memo[key]
    memo[key] = resources[GEODE]

    if minute == 25:
        #print(resources[GEODE], robots[GEODE], resources, robots)
        if resources[GEODE] > cur_max:
            cur_max = resources[GEODE]
            print('rs=', resources, 'ro=', robots, 'm=', minute, 'mx=', cur_max)
            #print('key=', key)
        return resources[GEODE]

    n_geodes = 1 if resources[ORE] >= geode_costs[bp_id][ORE] and resources[OBSIDIAN] >= geode_costs[bp_id][OBSIDIAN] else 0

    # check if we can still make that many geodes
    #max_possible_bots = robots[GEODE] + n_geodes
    #max_possible = resources[GEODE] + (max_possible_bots * (25 - minute))
    #for i in range(minute, 25 - minute, 3):
    #    max_possible += 1
    #if max_possible < cur_max:
    #    return -1

    #if needed > 0 and (25 - minute) * (robots[GEODE] + (1 if n_geodes > 0 else 0) + 1) < needed:
    #    #print(needed, (25 - minute) * (robots[GEODE] + (1 if n_geodes > 0 else 0) + 2), robots[GEODE], minute)
    #    return -1

    #if minute > 23 and resources[GEODE] < 2:
        #return -1

    if nodes % 1_000_000 == 0:
    #if resources[GEODE] > 2:
        print(datetime.now(), 'hits=', hits, nodes, resources[GEODE], robots[GEODE], minute, cur_max)

    #print(' ' * minute, minute, resources[GEODE])

    max_v = 0

    g = n_geodes #for g in range(n_geodes, -1, -1):
    if True:
        n_obsidian = 1 if g == 0 and resources[ORE] >= obsidian_costs[bp_id][ORE] and resources[CLAY] >= obsidian_costs[bp_id][CLAY] else 0
        ob = n_obsidian
        for ob in range(n_obsidian, -1, -1):
            if clay_costs[bp_id] >= ore_costs[bp_id]:
                n_clay = 1 if ob == 0 and g == 0 and resources[ORE] >= clay_costs[bp_id] else 0
                for c in range(n_clay, -1, -1):
                    n_ore = 1 if c == 0 and ob == 0 and g == 0 and resources[ORE] >= ore_costs[bp_id] else 0
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

                        max_v = max(max_v, evaluate(bp_id, new_resources, new_robots, minute + 1, ''))# key+make_key(minute, new_resources, new_robots, robots, resources, g, ob, c, o)))
            else:
                n_ore = 1 if ob == 0 and g == 0 and resources[ORE] >= ore_costs[bp_id] else 0
                for o in range(n_ore, -1, -1):
                    n_clay = 1 if o == 0 and ob == 0 and g == 0 and resources[ORE] >= clay_costs[bp_id] else 0
                    for c in range(n_clay, -1, -1):
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

                        max_v = max(max_v, evaluate(bp_id, new_resources, new_robots, minute + 1, ''))# key+make_key(minute, new_resources, new_robots, robots, resources, g, ob, c, o)))

    return max_v

def evaluate2(bp_id:int, resources:dict, robots:dict, minute:int, key:str, target_geodes:int) -> int:

    def distribute_minutes(target_bots, amount_per):
        bot_minutes = []

        if target_bots % amount_per != 0:
            tgt = target_bots // amount_per
            for _ in range(0, amount_per):
                bot_minutes.append(tgt)
            leftover = target_bots - tgt * amount_per
            p = 0
            while leftover > 0:
                bot_minutes[p] += 1
                leftover -= 1
                p += 1
        else:
            bot_minutes.append(target_bots // amount_per)
        return bot_minutes

    # need 9 geodes
    # need 9 geode robots for 1 minute
    # need 1 geode robots for 9 minutes

    for i in range(1, target_geodes + 1):
        geode_bot_minutes = distribute_minutes(target_geodes, i)
        print(f'{i} geode bots for {geode_bot_minutes} minutes')

        target_obsidian = geode_costs[bp_id][OBSIDIAN]
        target_ore_g = geode_costs[bp_id][ORE]

        for g_bm in geode_bot_minutes:
            time_g = 24 - g_bm - 1
            print(f'  can I make {target_obsidian} obs and {target_ore_g} ore in {time_g} minutes?', end='')
            if target_obsidian > time_g or target_ore_g > time_g:
                print(f'  NO')
                continue
            else:
                print(f'  YES')

            for j in range(1, (target_obsidian) + 1):
                obsidian_bot_minutes = distribute_minutes(target_obsidian, j)
                print(f'  {j} obsidian bots for {obsidian_bot_minutes} minutes')

                target_clay = obsidian_costs[bp_id][CLAY]
                target_ore_ob = obsidian_costs[bp_id][ORE]

                for ob_gm in obsidian_bot_minutes:
                    time_ob = time_g - ob_gm - 1
                    print(f'    can I make {target_clay} clay in {time_ob} minutes? ', end='')
                    if target_clay > time_ob:
                        print(f'  NO')
                        continue
                    else:
                        print(f'  YES')

                    print(f'    can I make {target_ore_ob} ore in {time_ob} minutes? ', end='')
                    if target_ore_ob > time_ob:
                        print(f'  NO')
                        continue
                    else:
                        print(f'  YES')

                print('LOOKS OK')

                """
            for j in range(1, (target_ore_g) + 1):
                obsidian_bot_minutes = distribute_minutes(target_ore_g, j)
                print(f'  {j} obsidian bots for {obsidian_bot_minutes} minutes')

                target_clay = obsidian_costs[bp_id][CLAY]
                target_ore_ob = obsidian_costs[bp_id][ORE]

                fail = False
                for ob_gm in obsidian_bot_minutes:
                    time_ob = time_g - ob_gm - 1
                    print(f'    can I make {target_clay} clay and {target_ore_ob} ore in {time_ob} minutes? ', end='')
                    if target_clay > time_ob or target_ore_ob > time_ob:
                        print(f'  NO')
                        fail = True
                        break
                    else:
                        print(f'  YES')

                if fail:
                    continue

                    clay_bot_minutes = distr

                    target_ore_cl = clay_costs[bp_id]

                    for k in range(1, (target_ore3) + 1):
                        bot_minutes3 = []

                        if target_ore3 % k != 0:
                            tgt = target_ore3 // k
                            for _ in range(0, k):
                                bot_minutes3.append(tgt)
                            leftover = target_ore3 - tgt * k
                            p = 0
                            while leftover > 0:
                                bot_minutes3[p] += 1
                                leftover -= 1
                                p += 1
                        else:
                            bot_minutes3.append(target_ore3 // k)

                        print(f'      {k} bots for {bot_minutes3} minutes')
                        for bm3 in bot_minutes3:
                            time3 = time2 - bm3 - 1
                            print(f'      can I make {target_ore3} ore in {time3} minutes? ', end='')
                            if target_clay > time2 or target_ore2 > time2:
                                print(f'  NO')
                                fail = True
                                break
                            else:
                                print(f'  YES')
                        else:
                            print('ok?')
                """

def evaluate3(bp_id:int, resources:dict, robots:dict, minute:int, key:str, target_geodes:int) -> int:
    def can_make_geode():
        return resources[OBSIDIAN] >= geode_costs[bp_id][OBSIDIAN] and resources[ORE] >= geode_costs[bp_id][ORE]
    def can_make_obsidian():
        return resources[CLAY] >= obsidian_costs[bp_id][CLAY] and resources[ORE] >= obsidian_costs[bp_id][ORE]
    def can_make_clay():
        return resources[ORE] >= clay_costs[bp_id]
    def can_make_ore():
        return resources[ORE] >= ore_costs[bp_id]

    def apply_robots():
        resources[ORE] += robots[ORE]
        resources[CLAY] += robots[CLAY]
        resources[OBSIDIAN] += robots[OBSIDIAN]
        resources[GEODE] += robots[GEODE]

    for minute in range(1, 25):
        new_bots = []
        if can_make_geode():
            resources[OBSIDIAN] -= geode_costs[bp_id][OBSIDIAN]
            resources[ORE] -= geode_costs[bp_id][ORE]
            new_bots.append(GEODE)

        if can_make_obsidian():
            resources[CLAY] -= obsidian_costs[bp_id][CLAY]
            resources[ORE] -= obsidian_costs[bp_id][ORE]
            new_bots.append(OBSIDIAN)

        if can_make_clay():
            resources[ORE] -= clay_costs[bp_id]
            new_bots.append(CLAY)

        if can_make_ore():
            resources[ORE] -= ore_costs[bp_id]
            new_bots.append(ORE)
        
        apply_robots()

        for b in new_bots:
            robots[b] += 1

    return (resources, robots)

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
    pass

#r = evaluate(5, copy(starting_resources), copy(starting_robots), 1, '')
#print(f'!! bp max = {r}')
#quit()

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
    r = evaluate(i, copy(starting_resources), copy(starting_robots), 1, '')
    print(f'!! bp {i} max = {r}')
    rs.append((i, r))
#print(rs)

s = sum(r[0] * r[1] for r in rs)
print('part1', s)