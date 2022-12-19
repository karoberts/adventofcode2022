from collections import defaultdict
import re
from typing import DefaultDict, List

valves:dict[str, int] = {}
openable_valves:set[str] = set()
tunnels:dict[tuple, List[str]] = {}

with open('16.txt') as f:
    for line in f.read().splitlines():
        m = re.match(r'^Valve ([A-Z][A-Z]) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? ([A-Z, ]+)$', line)
        p_valve = m.group(1)
        p_rate = int(m.group(2))
        p_tunnels = [t for t in m.group(3).split(', ')]
        #print(p_valve, p_rate, p_tunnels)
        valves[p_valve] = p_rate
        if p_rate > 0:
            openable_valves.add(p_valve)
        tunnels[p_valve] = p_tunnels

#print(valves)
#print(tunnels)
#print(c_openable)

cur_max = 0
nodes = 0

# 1915 AA:OU:VX:XD[o]:CD:LU[o]:BT:KS[o]:QA:YC[o]:FQ:AJ:LU:IZ:SX[o]:LV:HQ[o]:LV:SX:ZE:HJ[o]:MW:TE:LA

# AA:DD[o]:CC:BB[o]:AA:II:JJ[o]:II:AA:DD:EE:FF:GG:HH[o]:GG:FF:EE[o]:DD:CC[o]

def recur(cur_valve:str, cur_time:int, cur_pressure:int, cur_open:set, cur_key:str, since_last_open:set):
    global cur_max
    global nodes

    nodes += 1

    if len(cur_open) == len(openable_valves) or cur_time >= 30:
        if len(cur_open) == len(openable_valves):
            new_pressure = sum(valves[c] for c in cur_open)
            cur_pressure += new_pressure * (30 - cur_time)

        if cur_max < cur_pressure:
            print(cur_pressure, cur_key, cur_time)
        cur_max = max(cur_max, cur_pressure)
        return cur_pressure

    max_v = 0

    new_pressure = sum(valves[c] for c in cur_open) * (30 - cur_time)
    remaining_pressure = 0
    #remaining_pressure += (sum(valves[v] for v in openable_valves.difference(cur_open))) * (30 - cur_time)
    for i, v in enumerate(sorted(openable_valves.difference(cur_open), reverse=True)):
        remaining_pressure += (30 - cur_time - i + 3) * valves[v]
    remaining_pressure += cur_pressure
    remaining_pressure += new_pressure

    if remaining_pressure < cur_max:
        return max_v

    #if nodes % 1000000 == 0:
    #    print(nodes, cur_key, cur_time, cur_pressure, remaining_pressure)

    new_pressure = sum(valves[c] for c in cur_open)
    for t in tunnels[cur_valve]:
        if t in since_last_open:
            continue

        if cur_time < 29 and t not in cur_open and valves[t] > 0:
            new_open = set(cur_open)
            new_open.add(t)
            max_v = max(max_v, recur(t, cur_time + 2, cur_pressure + new_pressure + new_pressure, new_open, cur_key + f':{t}[o]', set()))

        new_slo = set(since_last_open)
        new_slo.add(t)
        max_v = max(max_v, recur(t, cur_time + 1, cur_pressure + new_pressure, cur_open, cur_key + f':{t}', new_slo))

    return max_v

c = recur('AA', 0, 0, set(), 'AA', set(['AA']))
print('part1', c)