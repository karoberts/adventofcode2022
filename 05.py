import re
from collections import defaultdict

stacks = defaultdict(lambda:[])
commands = []

with open('05.txt') as f:
    mode = 'STACKS'
    for line in f.read().splitlines():
        if mode == 'STACKS':
            if line[0:2] != ' 1':
                for i in range(0, len(line), 4):
                    crate = line[i + 1]
                    if crate != ' ':
                        stacks[i//4 + 1].append(crate)
            else:
                for s in stacks.values():
                    s.reverse()
                mode = 'COMMANDS'
        elif mode == 'COMMANDS':
            if line == '': continue
            m = re.match(r'^move (\d+) from (\d) to (\d)$', line)
            commands.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))

stacks_2 = {}
for s in stacks.items():
    stacks_2[s[0]] = s[1].copy()

def print_stacks(s):
    for i in range(1, len(s) + 1):
        print('stack', i, s[i])
    print()

#print_stacks(stacks)

for cmd in commands:
    amt = cmd[0]
    mv_from = cmd[1]
    mv_to = cmd[2]

    for i in range(0, amt):
        stacks[mv_to].append(stacks[mv_from].pop())

    #print_stacks(stacks)


p1 = ''
for i in range(1, len(stacks) + 1):
    p1 += stacks[i][-1]
print('part1', p1)

for cmd in commands:
    amt = cmd[0]
    mv_from = cmd[1]
    mv_to = cmd[2]

    items = []
    for i in range(0, amt):
        items.append(stacks_2[mv_from].pop())

    for i in reversed(items):
        stacks_2[mv_to].append(i)


p2 = ''
for i in range(1, len(stacks_2) + 1):
    p2 += stacks_2[i][-1]
print('part2', p2)