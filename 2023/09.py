from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()


def extrapolate(vals: list[int]):
    diffs, all_zero = [], True
    for i in range(1, len(vals)):
        diffs.append(vals[i] - vals[i - 1])
        if diffs[-1] != 0:
            all_zero = False
    next_val = 0 if all_zero else extrapolate(diffs)
    return vals[-1] + next_val


total = 0
for line in lines:
    history = [int(x) for x in line.split()]
    total += extrapolate(history)
print(f"Part 1: {total}")
