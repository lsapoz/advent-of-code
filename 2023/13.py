from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

patterns = [[]]
for line in lines:
    if len(line) == 0:
        patterns.append([])
    else:
        patterns[-1].append(line)


def check_horizontal_symmetry(pattern):
    num_rows = len(pattern)
    rows = list(map(tuple, pattern))
    for i in range(1, num_rows):
        num_on_side = min(i, num_rows - i)
        top = rows[i - num_on_side : i]
        bottom = list(reversed(rows[i : i + num_on_side]))
        if top == bottom:
            return i
    return 0


total = 0
for pattern in patterns:
    val = check_horizontal_symmetry(pattern)
    if val > 0:
        total += 100 * val
    else:
        total += check_horizontal_symmetry(list(zip(*pattern)))
print(total)
