import re
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

        xdist = abs(sensors[-1][X] - beacons[-1][X])
        ydist = abs(sensors[-1][Y] - beacons[-1][Y])

        min_y = min(min_y, sensors[-1][Y] - ydist, beacons[-1][Y] - ydist)
        min_x = min(min_x, sensors[-1][X] - xdist, beacons[-1][X] - xdist)
        max_y = max(max_y, sensors[-1][Y] + ydist, beacons[-1][Y] + ydist)
        max_x = max(max_x, sensors[-1][X] + xdist, beacons[-1][X] + xdist)

if max_x - min_x < 1_000_000:
    y_target = 10
else:
    y_target = 2000000

beacon_set = set(beacons)
sensor_set = set(sensors)

sensor_sorted = sorted(sensors, key=lambda s:abs(s[Y] - y_target))
dists_sorted = [dists_map[s] for s in sensor_sorted]
ydists_sorted = [abs(s[Y] - y_target) for s in sensor_sorted]

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

p1()

#lp = LineProfiler()
#lp_w = lp(p1)
#lp_w()
#lp.print_stats()            


