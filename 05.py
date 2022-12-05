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