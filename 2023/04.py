from pathlib import Path
import re

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

total = 0
for line in lines:
    _, all_nums = line.split(":")
    winning_nums, my_nums = [[int(num) for num in nums.split(" ") if num.isnumeric()] for nums in all_nums.split("|")]
    overlap = set(winning_nums).intersection(set(my_nums))
    total += 2 ** (len(overlap) - 1) if len(overlap) > 0 else 0
print(total)
