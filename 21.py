import re

monkeys:dict = {}

with open('21.txt') as f:
    for line in f.read().splitlines():
        parts = line.split(': ')
        monkey_id = parts[0]
        m = re.match(r'^([a-z]{4}) ([+\-*\/]) ([a-z]{4})$', parts[1])
        if m is None:
            monkeys[monkey_id] = (0, int(parts[1]))
        else:
            monkeys[monkey_id] = (1, m.group(1), m.group(2), m.group(3))

def process(monkey_id:str) -> int:
    m = monkeys[monkey_id]
    if m[0] == 0:
        return m[1]
    
    v_a = process(m[1])
    v_b = process(m[3])

    match m[2]:
        case '+': return v_a + v_b
        case '-': return v_a - v_b
        case '*': return v_a * v_b
        case '/': return v_a // v_b
        case _: raise Exception()

v = process('root')
print('part1', v)

def find_human(monkey_id:str) -> bool:
    m = monkeys[monkey_id]
    if m[0] == 0:
        return monkey_id == 'humn'
    
    return find_human(m[1]) or find_human(m[3])

def monkey_math_print(monkey_id:str):
    m = monkeys[monkey_id]
    if monkey_id == 'humn': return monkey_id
    if m[0] == 0:
        return m[1]

    if find_human(m[1]):
        v_a = monkey_math_print(m[1])
        v_b = process(m[3])
    else:
        v_a = process(m[1])
        v_b = monkey_math_print(m[3])

    return f'({v_a} {m[2]} {v_b})'

def monkey_math(monkey_id:str, stack:list):
    m = monkeys[monkey_id]
    if monkey_id == 'h': return monkey_id
    if m[0] == 0:
        return m[1]

    if find_human(m[1]):
        v_a = monkey_math(m[1], stack)
        v_b = process(m[3])
    else:
        v_a = process(m[1])
        v_b = monkey_math(m[3], stack)

    stack.append(v_b)
    stack.append(m[2])
    stack.append(v_a)

    return '.'

root = monkeys['root']

if find_human(root[1]):
    root_v = process(root[3])
    root_h = 1
    #print('human on A, value on B', root_v)
elif find_human(root[3]):
    root_v = process(root[1])
    root_h = 3
    #print('human on B, value on A', root_v)

st = []
monkey_math(root[root_h], st)

tgt = root_v
while len(st) > 0:
    triplet = (st.pop(), st.pop(), st.pop())

    #print(triplet, tgt)
    if triplet[2] == '.': 
        match triplet[1]: # 5 // .
            case '/': tgt = 1 / (tgt * triplet[0])
            case '*': tgt = tgt // triplet[0]
            case '-': tgt = -1 * (tgt - triplet[0])
            case '+': tgt = tgt - triplet[0]
    else:
        match triplet[1]: # . / 5
            case '/': tgt = tgt * triplet[2]
            case '*': tgt = tgt // triplet[2]
            case '-': tgt = tgt + triplet[2]
            case '+': tgt = tgt - triplet[2]

print('part2', tgt)

# double check
monkeys['humn'] = (0, tgt)
v = process(root[root_h])
if v != root_v:
    print('FAIL', v, root_v)

# 150 = ((4 + (2 * (humn - 3))) // 4)
# 150 * 4 = (4 + (2 * (humn - 3)))
# 150 * 4 - 4 = (2 * (humn - 3))
# (150 * 4 - 4) // 2 = humn - 3
# (150 * 4 - 4) // 2 + 3 = humn