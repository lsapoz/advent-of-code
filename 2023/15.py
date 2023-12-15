from pathlib import Path
from collections import defaultdict

steps = Path(__file__).resolve().with_suffix(".txt").read_text().replace("\n", "").split(",")


def HASH(s: str):
    val = 0
    for char in s:
        val += ord(char)
        val *= 17
        val %= 256
    return val


print(f"Part 1: {sum(HASH(step) for step in steps)}")

boxes: dict[int, dict[str, int]] = defaultdict(dict)
for step in steps:
    op = "=" if "=" in step else "-"
    focal_length = int(step[-1]) if op == "=" else None
    label = step[:-2] if op == "=" else step[:-1]

    box_no = HASH(label)
    if op == "=":
        boxes[box_no][label] = focal_length
    else:
        boxes[box_no].pop(label, None)

total = 0
for box_no, lenses in boxes.items():
    for idx, focal_length in enumerate(lenses.values()):
        total += (box_no + 1) * (idx + 1) * focal_length
print(f"Part 2: {total}")
