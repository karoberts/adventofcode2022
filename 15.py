import datetime
import re
from time import time
from line_profiler import LineProfiler

X = 0
Y = 1

def manhat_dist(c1:tuple, c2:tuple) -> int:
    return abs(c1[X] - c2[X]) + abs(c1[Y] - c2[Y])

sensors = []
beacons = []
dists_map = {}
dists = []
min_y = 0
min_x = 0
max_y = 0
max_x = 0

with open('15.txt') as f:
    for line in f.read().splitlines():
        m = re.match(r'Sensor at x=([\-\d]+), y=([\-\d]+): closest beacon is at x=([\-\d]+), y=([\-\d]+)', line)
        sensors.append( (int(m.group(1)), int(m.group(2))) )
        beacons.append( (int(m.group(3)), int(m.group(4))) )
        dists.append(manhat_dist(sensors[-1], beacons[-1]))
        dists_map[sensors[-1]] = dists[-1]

        xdist = abs(sensors[-1][X] - beacons[-1][X]) + 2
        ydist = abs(sensors[-1][Y] - beacons[-1][Y]) + 2

        min_y = min(min_y, sensors[-1][Y] - ydist, beacons[-1][Y] - ydist)
        min_x = min(min_x, sensors[-1][X] - xdist, beacons[-1][X] - xdist)
        max_y = max(max_y, sensors[-1][Y] + ydist, beacons[-1][Y] + ydist)
        max_x = max(max_x, sensors[-1][X] + xdist, beacons[-1][X] + xdist)

if max_x - min_x < 1_000_000:
    y_target = 10
    max_target = 20
else:
    y_target = 2000000
    max_target = 4_000_000

beacon_set = set(beacons)
sensor_set = set(sensors)

"""
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        if (x,y) in sensors:
            print('S', end='')
        elif (x,y) in beacons:
            print('B', end='')
        else:
            print('.', end='')
    print()
"""

"""
# my original approach, takes about 8.4 seconds
sensor_sorted = sorted(sensors, key=lambda s:abs(s[Y] - y_target))
dists_sorted = [dists_map[s] for s in sensor_sorted]
ydists_sorted = [abs(s[Y] - y_target) for s in sensor_sorted]

def p1():
    open_spots = 0
    for x in range(min_x, max_x + 1):
        c = (x, y_target)
        if c not in sensor_set and c not in beacon_set:
            for i in range(0, len(sensors)):
                xd = abs(c[X] - sensor_sorted[i][X]) + ydists_sorted[i]
                if xd <= dists_sorted[i]:
                    open_spots += 1
                    break

    print('part1', open_spots)
"""

# john's approach, about 820ms
def john_p1(yt):
    considered = set()
    for s in sensors:
        yd = abs(s[Y] - yt)
        d = dists_map[s]
        if d < yd: continue
        delt = d - yd
        for i in range(0, delt + 1):
            considered.add(s[X] - i)
            considered.add(s[X] + i)
        
    for b in beacons:
        if b[Y] == yt and b[X] in considered: considered.remove(b[X])
    for s in sensors:
        if s[Y] == yt and s[X] in considered: considered.remove(s[X])
    return considered

p1a = john_p1(y_target)
print('part1', len(p1a))

#p1()

# ~23.5 seconds and ~11.1 GB of memory for p2
start = datetime.datetime.now()
boundaries = []

for i, s in enumerate(sensors):
    #print(datetime.datetime.now(), f': sensor {i} of {len(sensors)}')
    lef = (s[X] - dists_map[s] - 1, s[Y])
    rig = (s[X] + dists_map[s] + 1, s[Y])

    bps = set()

    yd = 0
    for x in range(lef[X], s[X] + 1):
        if x >= 0:
            bps.add((x, s[Y] + yd))
            bps.add((x, s[Y] - yd))
        yd += 1

    yd = 0
    for x in range(rig[X], s[X], -1):
        if x <= max_target:
            bps.add((x, s[Y] + yd))
            bps.add((x, s[Y] - yd))
        yd += 1

    boundaries.append(bps)

done = False
for i in range(0, len(boundaries)):
    for j in range(i + 1, len(boundaries)):
        #print(datetime.datetime.now(), f': boundary {i}/{j} of {len(sensors)}')
        #intersections.append( boundaries[i].intersection(boundaries[j]) )
        ints = boundaries[i].intersection(boundaries[j])

        for c in ints:
            #if c[X] < 0 or c[X] > max_target or c[Y] < 0 or c[Y] > max_target:
            #    continue
            for i, s in enumerate(sensors):
                d = dists[i]
                di = manhat_dist(c, s)
                if di <= d:
                    break
            else:
                #print(c)
                tuning = c[X] * 4_000_000 + c[Y]
                print('part2', tuning)
                done = True
                break
        if done:
            break
    if done:
        break

#print(datetime.datetime.now() - start)

#lp = LineProfiler()
#lp_w = lp(john_p1)
#lp_w()
#lp.print_stats()            
