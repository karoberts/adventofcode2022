with open("01.txt") as f:
    elves = [0]
    cur_elf = 0
    for line in (l.strip() for l in f):
        if len(line) == 0:
            cur_elf += 1
            elves.append(0)
        else:
            elves[cur_elf] += int(line)
    
m = max(enumerate(elves), key = lambda x:x[1])
print("part1", m[1])