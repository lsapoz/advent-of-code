from pathlib import Path
from collections import Counter
from itertools import combinations

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()


def is_valid(arrangement: str, group_sizes: tuple[int]):
    return tuple(len(x) for x in arrangement.replace(".", " ").strip().split()) == group_sizes


def get_valid_arrangements(record: str):
    springs, group_sizes = record.split()
    group_sizes = tuple([int(x) for x in group_sizes.split(",")])
    total_springs = sum(group_sizes)
    num_springs_missing = total_springs - Counter(springs)["#"]

    missing_positions = [i for i, char in enumerate(springs) if char == "?"]
    pos_combinations = list(combinations(missing_positions, num_springs_missing))

    num_valid = 0
    for comb in pos_combinations:
        res = list(springs)
        for pos in comb:
            res[pos] = "#"
        arrangement = "".join(res).replace("?", ".")
        if is_valid(arrangement, group_sizes):
            num_valid += 1

    return num_valid


total = 0
for line in lines:
    total += get_valid_arrangements(line)
print(total)
