from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

total = 0
for line in lines:
    first = next(x for x in line if x.isnumeric())
    last = next(x for x in reversed(line) if x.isnumeric())
    total += int(first + last)
print(total)
