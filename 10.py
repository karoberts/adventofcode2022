
from collections import defaultdict
from types import LambdaType
from typing import DefaultDict

from letterrecognizer import recognize_letter

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
    

registers['X'] = 1
cycle = 1
crt:DefaultDict[int, str] = defaultdict(lambda:'  ')
pixel = 0

for cmd in cmds:
    x = registers['X']
    for i in range(0, cmd.cycles):
        px = pixel % 40
        if px == x - 1 or px == x or px == x + 1:
            crt[pixel] = '\u2588' * 2

        cycle += 1
        pixel += 1

    cmd.func(registers)

grid = [defaultdict(lambda:False) for _ in range(0, 8)] # 40 wide, 4 pixels wide + 1 space == 8 letters

for p in range(0, pixel, 40):
    for px in range(0, 40):
        #print(crt[px + p], end='')
        letter_idx = px // 5
        if crt[px + p] != '  ':
            grid[letter_idx][(px % 5, p // 40)] = True
    #print()

print('part2 ', end='')
for g in grid:
    print(recognize_letter(g), end='')
print()