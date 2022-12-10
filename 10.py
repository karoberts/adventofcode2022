
from collections import defaultdict
from types import LambdaType
from typing import DefaultDict


class Command:
    def __init__(self, name:str, cycles:int, func:LambdaType) -> None:
        self.name = name
        self.cycles = cycles
        self.func = func

    @staticmethod
    def func_addx(registers:DefaultDict[str, int], v:int) -> None:
        registers['X'] += v

    @staticmethod
    def func_noop(_:DefaultDict[str, int]) -> None:
        pass

cmds = []

with open('10.txt') as f:
    for line in f.read().splitlines():
        parts = line.split(' ')
        #print(parts)
        match parts[0]:
            case 'addx': 
                f = (lambda vs: (lambda r: Command.func_addx(r, vs)))(int(parts[1]))
                cmds.append(Command(parts[0], 2, f))
            case 'noop':
                cmds.append(Command(parts[0], 1, lambda _: Command.func_noop))

cycle = 1
registers:DefaultDict[str, int] = defaultdict(lambda:1)
registers['X'] = 1

cycles_of_interest = set([20, 60, 100, 140, 180, 220])
cycles_of_interest_val = []

for cmd in cmds:
    for i in range(0, cmd.cycles):
        if cycle in cycles_of_interest:
            cycles_of_interest_val.append(registers['X'] * cycle)
        cycle += 1

    cmd.func(registers)

#print(cycles_of_interest_val)
print('part1', sum(cycles_of_interest_val))
    

     
