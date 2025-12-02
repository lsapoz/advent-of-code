from pathlib import Path
import re

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

dirs = {"L": -1, "R": 1}

dial = 50
num_zeros = 0
for line in lines:
    direction, distance = line[0], int(line[1:])
    dial = (dial + (dirs[direction] * distance)) % 100
    num_zeros += 1 if dial == 0 else 0
print(f"Part 1: {num_zeros}")
