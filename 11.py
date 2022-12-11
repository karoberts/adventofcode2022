from copy import deepcopy
from math import prod
import re
from types import FunctionType
from typing import List

class Monkey:
    id:int
    items:List[int]
    operation:tuple
    test:int
    iftrue:int
    iffalse:int
    inspection_ct:int
    opfunc:FunctionType

    def __init__(self, id:int, items:List[int], operation:tuple, test:int, iftrue:int, iffalse:int, opfunc:FunctionType) -> None:
        self.id = id
        self.items = items
        self.operation = operation
        self.test = test
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.inspection_ct = 0
        self.opfunc = opfunc
        pass

    def __str__(self) -> str:
        return f'Monkey {self.id}: Op={self.operation} Test={self.test} true={self.iftrue} false={self.iffalse}, ic={self.inspection_ct} items={self.items}'

monkeys:List[Monkey] = []

def add_old_i(old:int, i:int): return old + i
def add_old_old(old:int, _:int): return old + old
def mul_old_i(old:int, i:int): return old * i
def mul_old_old(old:int, _:int): return old * old

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
        op = (-1 if m3.group(1) == 'old' else int(m3.group(1)), m3.group(2), -1 if m3.group(3) == 'old' else int(m3.group(3)))
        match op:
            case (-1, '+', -1): opfunc = add_old_old
            case (-1, '+', _):  opfunc = add_old_i
            case (-1, '*', -1): opfunc = mul_old_old
            case (-1, '*', _):  opfunc = mul_old_i
        m = Monkey(
            int(m1.group(1)),
            [int(x) for x in m2.group(1).split(', ')],
            op,
            int(m4.group(1)),
            int(m5.group(1)),
            int(m6.group(1)),
            opfunc
        )
        monkeys.append(m)

monkeys_p2 = deepcopy(monkeys)

def run(max_round:int, ms:List[Monkey], factor:int, factor_func:FunctionType) -> None:

    for _ in range(1, max_round):
        for m in ms:
            for item in m.items:
                new_worry = factor_func(m.opfunc(item, m.operation[2]))
                if new_worry % m.test == 0:
                    ms[m.iftrue].items.append(new_worry)
                else:
                    ms[m.iffalse].items.append(new_worry)
                m.inspection_ct += 1
            m.items.clear()

run(21, monkeys, 3, lambda i: i // 3)
monkeys.sort(key = lambda m: m.inspection_ct, reverse=True)
print('part1', monkeys[0].inspection_ct * monkeys[1].inspection_ct)

mod = prod((m.test for m in monkeys_p2))
run(10001, monkeys_p2, 1, lambda i: i % mod)
#for m in monkeys_p2:
    #print(m)
monkeys_p2.sort(key = lambda m: m.inspection_ct, reverse=True)
print('part2', monkeys_p2[0].inspection_ct * monkeys_p2[1].inspection_ct)