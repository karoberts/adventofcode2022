from collections import defaultdict

X = 0
Y = 1
Z = 2

with open('18.txt') as f:
    cubes = [(int(p[X]), int(p[Y]), int(p[Z])) for p in (l.split(',') for l in f.read().splitlines())]

max_x = (min(c[X] for c in cubes), max(c[X] for c in cubes))
max_y = (min(c[Y] for c in cubes), max(c[Y] for c in cubes))
max_z = (min(c[Z] for c in cubes), max(c[Z] for c in cubes))
cube_set = set(cubes)


adj_map = [
    ( 0,  0, -1), ( 0,  0,  1),
    ( 0, -1,  0), ( 0,  1,  0),
    (-1,  0,  0), ( 1,  0,  0)
]

faces_open = []

for c in cubes:
    for face_adj in adj_map:
        adj_cube = (c[X] + face_adj[X], c[Y] + face_adj[Y], c[Z] + face_adj[Z])
        if adj_cube not in cube_set:
            faces_open.append(adj_cube)

print('part1', len(faces_open))

def find_outside(p:tuple, visited:set, known_closed:set):
    if p[X] == max_x[1] + 2 or p[Y] == max_y[1] + 2 or p[Z] == max_z[1] + 2:
        return False
    if p[X] == max_x[0] - 2 or p[Y] == max_y[0] - 2 or p[Z] == max_z[0] - 2:
        return False

    v = True
    for face_adj in adj_map:
        adj_cube = (p[X] + face_adj[X], p[Y] + face_adj[Y], p[Z] + face_adj[Z])
        if adj_cube in known_closed:
            return True
        if adj_cube in visited:
            continue
        if adj_cube in cube_set:
            continue
        visited.add(adj_cube)
        v = v and find_outside(adj_cube, visited, known_closed)
        if not v:
            return v

    return v

really_open = []
known_closed = set()
for open in faces_open:
    if not find_outside(open, set([open]), known_closed):
        really_open.append(open)
    else:
        known_closed.add(open)

print('part2', len(really_open))
