from pathlib import Path

ranges = Path(__file__).resolve().with_suffix(".txt").read_text().split(",")


def is_invalid_part_1(num: int):
    str_num = str(num)
    mid_point, remainder = divmod(len(str_num), 2)
    if remainder != 0:
        return False
    left, right = str_num[:mid_point], str_num[mid_point:]
    return left == right


def is_invalid_part_2(num: int):
    str_num = str(num)
    length = len(str_num)
    divisors = [i for i in range(1, len(str_num)) if length % i == 0]

    for divisor in divisors:
        parts = [str_num[i : i + divisor] for i in range(0, length, divisor)]
        if len(set(parts)) == 1:
            return True
    return False


part1, part2 = 0, 0
for r in ranges:
    split_range = r.split("-")
    left, right = int(split_range[0]), int(split_range[1])
    for id in range(left, right + 1):
        if is_invalid_part_1(id):
            part1 += id
        if is_invalid_part_2(id):
            part2 += id
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
