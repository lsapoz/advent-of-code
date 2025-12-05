from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()


def get_max(bank: str):
    curr_max_idx = 0
    curr_max_val = 0
    for i, num in enumerate(bank):
        if int(num) > curr_max_val:
            curr_max_idx = i
            curr_max_val = int(num)
    return (curr_max_idx, curr_max_val)


total = 0
for line in lines:
    idx, digit1 = get_max(line[:-1])
    _, digit2 = get_max(line[idx + 1 :])
    total += int(str(digit1) + str(digit2))
print(f"Part 1: {total}")
