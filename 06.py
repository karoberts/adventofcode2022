buffer = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'
buffer = 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'
with open('06.txt') as f:
    buffer = f.readline()

def find_marker(buffer, ucount):
    window_list = []
    for i, c in enumerate(buffer):
        if len(window_list) == ucount:
            window_list.pop(0)
        window_list.append(c)

        if len(window_list) == ucount and len(set(window_list)) == ucount:
            return i + 1
    return -1

print('part1', find_marker(buffer, 4))
print('part2', find_marker(buffer, 14))