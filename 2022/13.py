from pathlib import Path
import json

here = Path(__file__).parent
lines = Path(here/"13.txt").read_text().splitlines()

pairs = [(json.loads(lines[i]), json.loads(lines[i+1])) for i in range(0, len(lines), 3)]

def correct_order(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return None if left == right else left < right
    if isinstance(left, int) and isinstance(right, list):
        return correct_order([left], right)
    if isinstance(left, list) and isinstance(right, int):
        return correct_order(left, [right])
    for i in range(min(len(left), len(right))):
        result = correct_order(left[i], right[i])
        if result is not None:
            return result
    return correct_order(len(left), len(right))

correct_pair_indices = 0
for i, (left, right) in enumerate(pairs):
    if correct_order(left, right):
        correct_pair_indices += i + 1
print(f"Part 1: {correct_pair_indices}")
