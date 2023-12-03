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
for x, line in enumerate(lines):
    for y, char in enumerate(line):
        if not char.isnumeric() and char != ".":
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if nx >= 0 and ny >= 0 and nx < len(lines) and ny < len(line) and (nx, ny) in number_positions:
                    part_numbers.add(number_positions[(nx, ny)])
print(sum(num[0] for num in part_numbers))
