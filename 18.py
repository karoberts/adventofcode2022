
X = 0
Y = 1
Z = 2

with open('18.txt') as f:
    cubes = [(int(p[X]), int(p[Y]), int(p[Z])) for p in (l.split(',') for l in f.read().splitlines())]

cube_set = set(cubes)

adj_map = [
    ( 0,  0, -1), ( 0,  0,  1),
    ( 0, -1,  0), ( 0, -1,  0),
    (-1,  0,  0), (-1,  0,  0)
]

open_faces = 0

for c in cubes:
    for face_adj in adj_map:
        adj_cube = (c[X] + face_adj[X], c[Y] + face_adj[Y], c[Z] + face_adj[Z])
        if adj_cube not in cube_set:
            open_faces += 1

print('part1', open_faces)