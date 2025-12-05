from pathlib import Path
from typing import List

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()


def get_max(subset: str):
    curr_max_idx = 0
    curr_max_val = 0
    for i, num in enumerate(subset):
        if int(num) > curr_max_val:
            curr_max_idx = i
            curr_max_val = int(num)
    return (curr_max_idx, curr_max_val)


def get_joltage(bank: str, num_digits: int):
    curr_idx = 0
    joltage = ""
    for i in range(1, num_digits + 1):
        end_idx = -num_digits + i
        subset = bank[curr_idx:end_idx] if end_idx < 0 else bank[curr_idx:]
        idx, digit = get_max(subset)
        curr_idx += idx + 1
        joltage += str(digit)
    return int(joltage)


def get_total_joltage(banks: List[str], num_digits: int):
    total = 0
    for bank in banks:
        total += get_joltage(bank, num_digits)
    return total


print(f"Part 1: {get_total_joltage(lines, 2)}")
print(f"Part 2: {get_total_joltage(lines, 12)}")
