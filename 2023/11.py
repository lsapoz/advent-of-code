from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

empty_rows = [True] * len(lines)
empty_cols = [True] * len(lines[0])
galaxies = []
for i, line in enumerate(lines):
    for j, char in enumerate(line):
        if char == "#":
            empty_rows[i] = False
            empty_cols[j] = False
            galaxies.append((i, j))
empty_rows = [idx for idx, is_empty in enumerate(empty_rows) if is_empty]
empty_cols = [idx for idx, is_empty in enumerate(empty_cols) if is_empty]

distances = []
for i in range(len(galaxies)):
    for j in range(i + 1, len(galaxies)):
        (x1, y1), (x2, y2) = galaxies[i], galaxies[j]
        dist = abs(x1 - x2) + abs(y1 - y2)
        extra = 0
        for empty_row in empty_rows:
            if empty_row in range(min(x1, x2), max(x1, x2)):
                extra += 1
        for empty_col in empty_cols:
            if empty_col in range(min(y1, y2), max(y1, y2)):
                extra += 1
        distances.append((dist, extra))
print(f"Part 1: {sum(dist + extra for dist, extra in distances)}")
print(f"Part 2: {sum(dist + (extra * (1000000 - 1)) for dist, extra in distances)}")
