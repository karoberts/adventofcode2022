from typing import Tuple


games = []

# 1 = rock
# 2 = paper
# 3 = scissors

aMap = { 'A': 1, 'B': 2, 'C': 3 }
bMap = { 'X': 1, 'Y': 2, 'Z': 3 }

bMap2 = { 1: 0, 2: 3, 3: 6 }

winMap = { 
    (1, 1): 3, 
    (1, 2): 6,  
    (1, 3): 0,  

    (2, 1): 0, 
    (2, 2): 3,  
    (2, 3): 6,  

    (3, 1): 6, 
    (3, 2): 0,  
    (3, 3): 3,  
}

winMapRev = { 
    (1, 0): 3,
    (1, 3): 1,
    (1, 6): 2,

    (2, 0): 1,
    (2, 3): 2,
    (2, 6): 3,

    (3, 0): 2,
    (3, 3): 3,
    (3, 6): 1,
}

with open('02.txt') as f:
    for line in f.read().splitlines():
        games.append((aMap[line[0]], bMap[line[2]]))

score = sum(map(lambda x: x[1] + winMap[x], games))
print('part1', score)

def winMapFunc(x: Tuple) -> int:
    result = bMap2[x[1]]
    b = winMapRev[(x[0], result)]
    return b + result

score = sum(map(winMapFunc, games))
print('part2', score)