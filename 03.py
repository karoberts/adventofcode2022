with open('03.txt') as f:
    lines = f.read().splitlines()

priority = 0
for line in lines:
    l = len(line) // 2
    c1s = set(line[0:l])
    c2s = set(line[l:])
    shared = c1s.intersection(c2s)

    for s in shared:
        if s.isupper():
            priority += (ord(s) - ord('A') + 27)
        else:
            priority += (ord(s) - ord('a') + 1)

print('part1', priority)