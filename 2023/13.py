from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

patterns = [[]]
for line in lines:
    if len(line) == 0:
        patterns.append([])
    else:
        patterns[-1].append([x for x in line])


def check_horizontal_symmetry(pattern, orientation: str, to_ignore: tuple[str, int] = None):
    num_rows = len(pattern)
    rows = list(map(tuple, pattern))
    for i in range(1, num_rows):
        num_on_side = min(i, num_rows - i)
        top = rows[i - num_on_side : i]
        bottom = list(reversed(rows[i : i + num_on_side]))
        if top == bottom and (orientation, i) != to_ignore:
            return i
    return 0


def check_symmetry(pattern, to_ignore: tuple[str, int] = None):
    val = check_horizontal_symmetry(pattern, "h", to_ignore)
    if val > 0:
        return ("h", val)
    val = check_horizontal_symmetry(list(zip(*pattern)), "v", to_ignore)
    if val > 0:
        return ("v", val)
    return ("", 0)


def smudge(pattern, to_ignore: tuple[str, int]):
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            curr = pattern[i][j]
            pattern[i][j] = "." if curr == "#" else "."

            orientation, val = check_symmetry(pattern, to_ignore)
            if val > 0:
                return (orientation, val)
            pattern[i][j] = curr


part1 = 0
part2 = 0
for pattern in patterns:
    orientation, val = check_symmetry(pattern)
    part1 += val if orientation == "v" else val * 100

    orientation, val = smudge(pattern, (orientation, val))
    part2 += val if orientation == "v" else val * 100
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
