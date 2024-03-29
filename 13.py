import ast
import functools
from math import prod
from typing import List

groups = []

debug = False

with open('13.txt') as f:
    lines = f.read().splitlines()
    for i in range(0, len(lines), 3):
        groups.append((ast.literal_eval(lines[i]), ast.literal_eval(lines[i+1])))

def compare(left, right, indent=0) -> bool:
    if debug: print(f"{' ' * indent}- Compare {left} vs {right}")

    while True:
        l_int = isinstance(left, int)
        r_int = isinstance(right, int)
        if l_int and r_int:
            if left < right:
                if debug: print(f"{' ' * (indent+2)}- Left side is smaller, so inputs are in the right order")
                return 1
            elif left > right:
                if debug: print(f"{' ' * (indent+2)}- Right side is smaller, so inputs are not in the right order")
                return -1
            return 0 
        elif not l_int and not r_int:
            if len(left) == 0 and len(right) == 0:
                return 0
            if len(left) == 0:
                if debug: print(f"{' ' * (indent+2)}- Left side ran out of items, so inputs are in the right order")
                return 1
            if len(right) == 0:
                if debug: print(f"{' ' * (indent+2)}- Right side ran out of items, so inputs are not in the right order")
                return -1
            r = compare(left[0], right[0], indent + 2)
        elif l_int:
            if len(right) == 0:
                if debug: print(f"{' ' * (indent+1)}- Right side ran out of items, so inputs are not in the right order")
                return -1
            r = compare([left], right, indent + 2)
        elif r_int:
            if len(left) == 0:
                if debug: print(f"{' ' * (indent+1)}- Left side ran out of items, so inputs are in the right order")
                return 1
            r = compare(left, [right], indent + 2)

        match r:
            case -1: return -1
            case 1: return 1
            case 0:
                if l_int or r_int:
                    return 0
                left = left[1:]
                right = right[1:]

s = 0
for i, g in enumerate(groups):
    left = g[0]
    right = g[1]

    if debug: print(f'== Pair {i+1} ==')
    r = compare(left, right)
    if debug: print()
    if r == 1:
        s += (i + 1)

print('part1', s)

flattened = [ [[2]], [[6]] ]
for g in groups:
    flattened.append(g[0])
    flattened.append(g[1])

key_func = functools.cmp_to_key(lambda a, b: compare(a,b))
ordered = sorted(flattened, key = key_func, reverse=True)

p = prod((i + 1 for i, o in enumerate(ordered) if o == [[2]] or o == [[6]]))

print('part2', p)