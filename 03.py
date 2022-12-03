with open('03.txt') as f:
    lines = f.read().splitlines()

def calc_priority(s):
    if s.isupper():
        return (ord(s) - ord('A') + 27)
    else:
        return (ord(s) - ord('a') + 1)

priority = 0
for line in lines:
    l = len(line) // 2
    c1s = set(line[0:l])
    c2s = set(line[l:])
    shared = c1s.intersection(c2s)

    for s in shared:
        priority += calc_priority(s)

print('part1', priority)

priority = 0
for i in range(0, len(lines) - 2, 3):
    r1 = set(lines[i])
    r2 = set(lines[i + 1])
    r3 = set(lines[i + 2])

    badge = r1.intersection(r2).intersection(r3)

    for s in badge:
        priority += calc_priority(s)

print('part2', priority)