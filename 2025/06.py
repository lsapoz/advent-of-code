from pathlib import Path
from math import prod

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
grid = list(zip(*[[x for x in line.split()] for line in lines]))  # transpose the grid

total = 0
for line in grid:
    op = line[-1]
    numbers = [int(x) for x in line[:-1]]
    total += sum(numbers) if op == "+" else prod(numbers)
print(f"Part 1: {total}")
