with open("01.txt") as f:
    elves = [0]
    for line in (l.strip() for l in f):
        if len(line) == 0:
            elves.append(0)
        else:
            elves[-1] += int(line)
    
print("part1", max(elves))

top_three = (sorted(elves, key=lambda x:-x))[0:3]
print("part2", sum(top_three))