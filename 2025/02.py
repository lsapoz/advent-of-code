from pathlib import Path

ranges = Path(__file__).resolve().with_suffix(".txt").read_text().split(",")


def is_invalid(num: int):
    str_num = str(num)
    mid_point, remainder = divmod(len(str_num), 2)
    if remainder != 0:
        return False
    left, right = str_num[:mid_point], str_num[mid_point:]
    return left == right


invalid_sum = 0
for r in ranges:
    split_range = r.split("-")
    left, right = int(split_range[0]), int(split_range[1])
    for id in range(left, right + 1):
        if is_invalid(id):
            invalid_sum += id
print(f"Part 1: {invalid_sum}")
