from collections import defaultdict
import re

X = 0
Y = 1

def manhat_dist(c1:tuple, c2:tuple) -> int:
    return abs(c1[X] - c2[X]) + abs(c1[Y] - c2[Y])

sensors = []
beacons = []
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

        min_y = min(min_y, sensors[-1][Y] - dists[-1], beacons[-1][Y] - dists[-1])
        min_x = min(min_x, sensors[-1][X] - dists[-1], beacons[-1][X] - dists[-1])
        max_y = max(max_y, sensors[-1][Y] + dists[-1], beacons[-1][Y] + dists[-1])
        max_x = max(max_x, sensors[-1][X] + dists[-1], beacons[-1][X] + dists[-1])

if max_x - min_x < 1_000_000:
    y_target = 10
else:
    y_target = 2000000

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

open_spots = 0

for x in range(min_x, max_x + 1):
    ok = 0
    c = (x, y_target)
    if c in sensor_set or c in beacon_set:
        ok = len(sensors)
    else:
        for i in range(0, len(sensors)):
            d = dists[i]
            s = sensors[i]
            b = beacons[i]

            xd = manhat_dist(c, s)
            if xd <= d:
                break
            ok += 1
        
    if ok != len(sensors):
        #print((x, y_target))
        open_spots += 1

print('part1', open_spots)
            


