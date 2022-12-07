from typing import List


with open('07.txt') as f:
    lines = f.read().splitlines()

class Node:
    dirs: List
    files: List
    name: str
    size: int
    isdir: bool

    def __init__(self, name: str, isdir: bool, parent, size: int = None):
        self.name = name
        self.dirs = []
        self.files = []
        self.size = -1
        self.isdir = isdir
        self.size = size
        self.parent = parent

def print_tree(node:Node, indent:int):
    if node.isdir:
        print(' ' * indent, f'- {node.name} (dir) [{node.size}]')
        for c in node.dirs:
            print_tree(c, indent + 2)
        for c in node.files:
            print_tree(c, indent + 2)
    else:
        print(' ' * indent, f'- {node.name} (file, size={node.size})')

def calc_sizes(node:Node):
    if node.isdir:
        s = 0
        for c in node.dirs:
            s += calc_sizes(c)
        for c in node.files:
            s += c.size
        node.size = s
        return s

def find_p1(node:Node):
    if node.isdir:
        s = 0
        if node.size < 100000:
            s = node.size
        for c in node.dirs:
            s += find_p1(c)
        return s

def find_p2(node:Node, val:int):
    if node.isdir:
        s = 999999999999
        if node.size > val:
            s = node.size
        for c in node.dirs:
            v = find_p2(c, val)
            if v < s:
                s = v
        return s

cur = None
root = Node('/', True, None)

for line in lines:
    #print(line)
    if line[0] == '$':
        cmds = line.split(' ')
        if cmds[1] == 'cd':
            if cmds[2] == '/':
                cur = root
            elif cmds[2] == '..':
                cur = cur.parent
            else:
                for d in cur.dirs:
                    if d.name == cmds[2]:
                        cur = d
                        break
        elif cmds[1] == 'ls':
            pass
    elif line.startswith('dir '):
        dir = line.split(' ')[1]
        newnode = Node(dir, True, cur)
        cur.dirs.append(newnode)
        pass
    else:
        fi = line.split(' ')
        cur.files.append(Node(fi[1], False, cur, int(fi[0])))
        pass

calc_sizes(root)
#print_tree(root, 0)

print('part1', find_p1(root))

val = 30_000_000 - (70_000_000 - root.size)

print('part2', find_p2(root, val))

# 10862928 high