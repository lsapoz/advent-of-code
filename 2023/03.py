from pathlib import Path
import re

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

number_positions = {}  # map (x, y) grid pos to number tuple (number, x, y_of_first_digit)
for x, line in enumerate(lines):
    for match in re.finditer("\d+", line):
        num = (int(match.group(0)), x, match.start(0))
        number_positions.update({(x, y): num for y in range(match.start(0), match.end(0))})

dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
part_numbers = set()
gear_ratio_sum = 0
for x, line in enumerate(lines):
    for y, char in enumerate(line):
        if not char.isnumeric() and char != ".":
            adjacent_nums = set()
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if (nx, ny) in number_positions:
                    adjacent_nums.add(number_positions[(nx, ny)])
            part_numbers.update(adjacent_nums)
            if len(adjacent_nums) == 2:
                gear_ratio_sum += adjacent_nums.pop()[0] * adjacent_nums.pop()[0]
print(f"Part 1: {sum(num[0] for num in part_numbers)}")
print(f"Part 2: {gear_ratio_sum}")
