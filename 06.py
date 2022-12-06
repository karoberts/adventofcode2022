buffer = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'
buffer = 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'
with open('06.txt') as f:
    buffer = f.readline()

window_set = set()
window_list = []
p1 = -1
for i, c in enumerate(buffer):
    if len(window_list) == 4:
        window_list.pop(0)
    window_list.append(c)

    if len(window_list) == 4 and len(set(window_list)) == 4:
        p1 = i + 1
        break

print('part1', p1)