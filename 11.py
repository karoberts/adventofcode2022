import re
from typing import List

class Monkey:
    id:int
    items:List[int]
    operation:tuple
    test:int
    iftrue:int
    iffalse:int
    inspection_ct:int

    def __init__(self, id:int, items:List[int], operation:tuple, test:int, iftrue:int, iffalse:int) -> None:
        self.id = id
        self.items = items
        self.operation = operation
        self.test = test
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.inspection_ct = 0
        pass

    def __str__(self) -> str:
        return f'Monkey {self.id}: Op={self.operation} Test={self.test} true={self.iftrue} false={self.iffalse}, ic={self.inspection_ct} items={self.items}'

monkeys:List[Monkey] = []

with open('11.txt') as f:
    lines = f.read().splitlines()
    i = 0
    while i < len(lines):
        m1 = re.match(r'^Monkey (\d+):$', lines[i])
        i += 1
        m2 = re.match(r'^  Starting items: ([\d, ]+)$', lines[i])
        i += 1
        m3 = re.match(r'^  Operation: new = (old|\d+) ([\*\+]) (old|\d+)$', lines[i])
        i += 1
        m4 = re.match(r'^  Test: divisible by (\d+)$', lines[i])
        i += 1
        m5 = re.match(r'^    If true: throw to monkey (\d+)$', lines[i])
        i += 1
        m6 = re.match(r'^    If false: throw to monkey (\d+)$', lines[i])
        i += 2
        m = Monkey(
            int(m1.group(1)),
            [int(x) for x in m2.group(1).split(', ')],
            (-1 if m3.group(1) == 'old' else int(m3.group(1)), m3.group(2), -1 if m3.group(3) == 'old' else int(m3.group(3))),
            int(m4.group(1)),
            int(m5.group(1)),
            int(m6.group(1))
        )
        monkeys.append(m)

def apply_op(m: Monkey, item:int):
    v1 = item if m.operation[0] == -1 else m.operation[0]
    v2 = item if m.operation[2] == -1 else m.operation[2]
    if m.operation[1] == '+':
        return v1 + v2
    else:
        return v1 * v2

for round in range(1, 21):
    #print('Round', round)
    for m in monkeys:
        for item in m.items:
            new_worry = apply_op(m, item)
            new_worry //= 3
            if new_worry % m.test == 0:
                monkeys[m.iftrue].items.append(new_worry)
            else:
                monkeys[m.iffalse].items.append(new_worry)
            m.inspection_ct += 1
        m.items = []

monkeys.sort(key = lambda m: m.inspection_ct, reverse=True)
print('part1', monkeys[0].inspection_ct * monkeys[1].inspection_ct)
