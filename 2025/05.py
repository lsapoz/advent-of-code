from pathlib import Path
from typing import List, Tuple

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()


def merge_ranges(ranges: List[Tuple[int, int]]):
    sorted_ranges = sorted(ranges)
    merged = []
    for curr in sorted_ranges:
        if not merged or merged[-1][1] < curr[0]:
            merged.append(curr)
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], curr[1]))
    return merged


split_idx = lines.index("")
ranges = [(int(r[0]), int(r[1])) for r in (x.split("-") for x in lines[:split_idx])]
merged_ranges = merge_ranges(ranges)
ingredients = [int(x) for x in lines[split_idx + 1 :]]


def is_fresh(ingredient: int):
    for a, b in merged_ranges:
        if a <= ingredient <= b:
            return True
    return False


part1 = 0
for ingredient in ingredients:
    part1 += 1 if is_fresh(ingredient) else 0
print(f"Part 1: {part1}")

part2 = 0
for a, b in merged_ranges:
    part2 += b - a + 1
print(f"Part 2: {part2}")
