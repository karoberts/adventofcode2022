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