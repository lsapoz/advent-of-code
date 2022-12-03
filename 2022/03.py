from pathlib import Path

here = Path(__file__).parent
lines = Path(here/"03.txt").read_text().splitlines()

total_priority = 0
for line in lines:
    mid = len(line) // 2
    first_half, second_half = line[:mid], line[mid:]
    duplicate = set(first_half).intersection(set(second_half)).pop()
    if duplicate.islower():
        priority = ord(duplicate) - (ord('a')) + 1
    else:
        priority = ord(duplicate) - (ord('A')) + 27
    total_priority += priority
print(f"Total Priority: {total_priority}")
