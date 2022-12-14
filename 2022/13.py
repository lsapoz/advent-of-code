from pathlib import Path
import functools
import json

here = Path(__file__).parent
lines = Path(here/"13.txt").read_text().splitlines()

pairs = [(json.loads(lines[i]), json.loads(lines[i+1])) for i in range(0, len(lines), 3)]

def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return left - right
    if isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    if isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])
    for i in range(min(len(left), len(right))):
        result = compare(left[i], right[i])
        if result != 0:
            return result
    return compare(len(left), len(right))

correct_pair_indices = 0
for i, (left, right) in enumerate(pairs):
    if compare(left, right) < 0:
        correct_pair_indices += i + 1
print(f"Part 1: {correct_pair_indices}")

divider1, divider2 = [[2]], [[6]]
packets = [divider1, divider2]
for left, right in pairs:
    packets.extend([left, right])
packets.sort(key=functools.cmp_to_key(compare))
decoder_key = (packets.index(divider1) + 1) * (packets.index(divider2) + 1)
print(f"Part 2: {decoder_key}")
