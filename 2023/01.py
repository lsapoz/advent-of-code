from pathlib import Path
import re

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

total = 0
for line in lines:
    first = next(x for x in line if x.isnumeric())
    last = next(x for x in reversed(line) if x.isnumeric())
    total += int(first + last)
print(f"Part 1: {total}")

mapping = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}
reversed_mapping = {k[::-1]: v for k, v in mapping.items()}
total = 0
for line in lines:
    first = re.search(f"\d|{'|'.join(mapping.keys())}", line).group(0)
    last = re.search(f"\d|{'|'.join(reversed_mapping.keys())}", line[::-1]).group(0)
    total += int(mapping.get(first, first) + reversed_mapping.get(last, last))
print(f"Part 2: {total}")
