from line_profiler import LineProfiler
from typing import List, Self

with open('20.txt') as f:
    numbers = [int(x) for x in f.read().splitlines()]

class Node:
    next: Self | None = None
    prev: Self | None = None
    value: int

    def __init__(self, value:int, prev:Self | None, next:Self | None = None) -> None:
        self.value = value
        self.next = next
        self.prev = prev

        if self.prev is not None:
            self.prev.next = self
        if self.next is not None:
            self.next.prev = self

    def move(self):
        if self.value == 0: return
        if self.value < 0:
            for _ in range(0, -1 * self.value):
                n = self.next
                p = self.prev
                p.next = n
                n.prev = p

                pp = p.prev
                pp.next = self
                self.prev = pp
                self.next = p
                p.prev = self
        else:
            for _ in range(0, self.value):
                n = self.next
                p = self.prev
                p.next = n
                n.prev = p

                nn = n.next
                n.next = self
                self.prev = n
                self.next = nn
                nn.prev = self

    def __str__(self) -> str:
        return str(self.value)

pointers:List[Node] = []
root:Node = Node(numbers[0], None, None)
pointers.append(root)
zero:Node = None
cur = root
for i in range(1, len(numbers)):
    new_node = Node(numbers[i], cur, None)
    if numbers[i] == 0:
        zero = new_node
    pointers.append(new_node)
    cur = new_node

cur.next = root
root.prev = cur

def print_it():
    cur = pointers[0]
    for i in range(0, len(numbers)):
        print(f'{cur.value}, ', end='')
        cur = cur.next
    print()

def p1():
    for p in pointers:
        p.move()

    vals = []
    cur = zero
    for i in range(0, 3001):
        if i == 1000 or i == 2000 or i == 3000:
            vals.append(cur.value)
        cur = cur.next
    return vals

vals = p1()
print('part1', sum(vals))