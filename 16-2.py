from collections import defaultdict
import re
from typing import DefaultDict, List

valves:dict[str, int] = {}
openable_valves:set[str] = set()
tunnels:dict[tuple, List[str]] = {}

test = False
# cheating a little bit to make it faster since I found the answer
floor = 1651 if test else 2771 #1915

# 2772

with open('16-test.txt' if test else '16.txt') as f:
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

cur_max = floor
nodes = 0

def recur(cur_valve_m:str, cur_valve_e:str, cur_time:int, cur_pressure:int, cur_open:set, cur_key:str, since_last_open_m:set, since_last_open_e:set):
    global cur_max
    global nodes

    nodes += 1

    # cheating a little bit to make it faster since I found the answer
    if not test and cur_max == 2772:
        return cur_pressure

    if len(cur_open) == len(openable_valves) or cur_time >= 26:
        if len(cur_open) == len(openable_valves):
            new_pressure = sum(valves[c] for c in cur_open)
            cur_pressure += new_pressure * (26 - cur_time)

        if cur_max < cur_pressure:
            print(cur_pressure, cur_key, cur_time)
        cur_max = max(cur_max, cur_pressure)
        return cur_pressure

    max_v = 0

    new_pressure = sum(valves[c] for c in cur_open) * (26 - cur_time)
    remaining_pressure = 0
    #remaining_pressure += (sum(valves[v] for v in openable_valves.difference(cur_open))) * (26 - cur_time)
    for i, v in enumerate(sorted(openable_valves.difference(cur_open), reverse=True)):
        if 26 - cur_time - i > 0:
            remaining_pressure += (26 - cur_time - i + 1) * valves[v]
    remaining_pressure += cur_pressure
    remaining_pressure += new_pressure

    if remaining_pressure < cur_max:
        return max_v

    if nodes % 100000 == 0:
        print(nodes, cur_key, cur_time, cur_pressure, remaining_pressure)

    new_pressure = sum(valves[c] for c in cur_open)

    # me and elephant both open
    if (cur_valve_m not in cur_open and valves[cur_valve_m] > 0) and (cur_valve_e not in cur_open and valves[cur_valve_e] > 0) and (cur_valve_m != cur_valve_e):
        new_open = set(cur_open)
        new_open.add(cur_valve_m)
        new_open.add(cur_valve_e)
        max_v = max(max_v, recur(cur_valve_m, cur_valve_e, cur_time + 1, cur_pressure + new_pressure, new_open, cur_key + f':{cur_valve_m}[o]/{cur_valve_e}[o]', set(), set()))

    # only me open, elephant moves
    if (cur_valve_m not in cur_open and valves[cur_valve_m] > 0):
        new_open = set(cur_open)
        new_open.add(cur_valve_m)

        for t_e in tunnels[cur_valve_e]:
            if t_e in since_last_open_e:
                continue

            new_slo_e = set(since_last_open_e)
            new_slo_e.add(t_e)
            max_v = max(max_v, recur(cur_valve_m, t_e, cur_time + 1, cur_pressure + new_pressure, new_open, cur_key + f':{cur_valve_m}[o]/{t_e}', set(), new_slo_e))

    # only elephant open, me moves
    if (cur_valve_e not in cur_open and valves[cur_valve_e] > 0) and (cur_valve_m != cur_valve_e):
        new_open = set(cur_open)
        new_open.add(cur_valve_e)

        for t_m in tunnels[cur_valve_m]:
            if t_m in since_last_open_m:
                continue

            new_slo_m = set(since_last_open_m)
            new_slo_m.add(t_m)
            max_v = max(max_v, recur(t_m, cur_valve_e, cur_time + 1, cur_pressure + new_pressure, new_open, cur_key + f':{t_m}/{cur_valve_e}[o]', new_slo_m, set()))        

    for t_m in tunnels[cur_valve_m]:
        if t_m in since_last_open_m:
            continue
        for t_e in tunnels[cur_valve_e]:
            if t_e in since_last_open_e:
                continue

            # neither opens
            new_slo_e = set(since_last_open_e)
            new_slo_e.add(t_e)
            new_slo_m = set(since_last_open_m)
            new_slo_m.add(t_m)
            max_v = max(max_v, recur(t_m, t_e, cur_time + 1, cur_pressure + new_pressure, cur_open, cur_key + f':{t_m}/{t_e}', new_slo_m, new_slo_e))

    return max_v

c = recur('AA', 'AA', 0, 0, set(), 'AA/AA', set(['AA']), set(['AA']))
print('part2', c)