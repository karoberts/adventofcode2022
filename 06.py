buffer = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'
buffer = 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'
with open('06.txt') as f:
    buffer = f.readline()

def find_marker(buffer, ucount):
    for i in range(0, len(buffer)):
        if i >= ucount and len(set(buffer[i-ucount:i])) == ucount:
            return i
    return -1

print('part1', find_marker(buffer, 4))
print('part2', find_marker(buffer, 14))