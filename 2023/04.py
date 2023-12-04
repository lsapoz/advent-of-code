from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

points = [0] * len(lines)
copies = [1] * len(lines)
for idx, line in enumerate(lines):
    _, all_nums = line.split(":")
    winning_nums, my_nums = [[int(num) for num in nums.split(" ") if num.isnumeric()] for nums in all_nums.split("|")]
    overlap = set(winning_nums).intersection(set(my_nums))
    points[idx] = 2 ** (len(overlap) - 1) if len(overlap) > 0 else 0
    for i in range(idx + 1, min(idx + len(overlap) + 1, len(lines))):
        copies[i] += copies[idx]
print(f"Part 1: {sum(points)}")
print(f"Part 2: {sum(copies)}")
