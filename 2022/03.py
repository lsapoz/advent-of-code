from pathlib import Path

here = Path(__file__).parent
lines = Path(here/"03.txt").read_text().splitlines()

def get_priority(letter):
    if letter.islower():
        return ord(letter) - (ord('a')) + 1
    return ord(letter) - (ord('A')) + 27

part_1_priority = 0
for line in lines:
    mid = len(line) // 2
    first_half, second_half = line[:mid], line[mid:]
    duplicate = set(first_half).intersection(set(second_half)).pop()
    part_1_priority += get_priority(duplicate)
print(f"Part 1 Priority: {part_1_priority}")

part_2_priority = 0
num_groups = len(lines) // 3
for i in range(num_groups):
    sets = [set(lines[3*i + j]) for j in range(3)]
    duplicate = sets[0].intersection(*sets[1:]).pop()
    part_2_priority += get_priority(duplicate)
print(f"Part 2 Priority: {part_2_priority}")
