import ast
import functools
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
                return 0
            return -1
        elif not l_int and not r_int:
            if len(left) == 0 and len(right) == 0:
                return -1
            if len(left) == 0:
                if debug: print(f"{' ' * (indent+2)}- Left side ran out of items, so inputs are in the right order")
                return 1
            if len(right) == 0:
                if debug: print(f"{' ' * (indent+2)}- Right side ran out of items, so inputs are not in the right order")
                return 0
            r = compare(left[0], right[0], indent + 2)
        elif l_int:
            if len(right) == 0:
                if debug: print(f"{' ' * (indent+1)}- Right side ran out of items, so inputs are not in the right order")
                return 0
            r = compare([left], right, indent + 2)
        elif r_int:
            if len(left) == 0:
                if debug: print(f"{' ' * (indent+1)}- Left side ran out of items, so inputs are in the right order")
                return 1
            r = compare(left, [right], indent + 2)

        match r:
            case 0: return 0
            case 1: return 1
            case -1:
                if l_int or r_int:
                    return -1
                left = left[1:]
                right = right[1:]

s = 0
for i, g in enumerate(groups):
    left = g[0]
    right = g[1]

    if debug: print(f'== Pair {i+1} ==')
    r = compare(left, right)
    if debug: print()
    if r:
        s += (i + 1)

print('part1', s)

flattened = []
for g in groups:
    flattened.append(g[0])
    flattened.append(g[1])

flattened.append([[2]])
flattened.append([[6]])
ordering = {}

for i in range(0, len(flattened)):
    for j in range(0, len(flattened)):
        if i == j: continue
        ordering[(i,j)] = compare(flattened[i], flattened[j])

key_func = functools.cmp_to_key(lambda a, b: -1 if ordering[(a,b)] == 0 else 1)
ordered = sorted([x for x in range(0, len(flattened))], key = key_func)
ordered.reverse()

p = 1
for i, o in enumerate(ordered):
    if flattened[o] == [[2]] or flattened[o] == [[6]]:
        p *= (i + 1)

print('part2', p)