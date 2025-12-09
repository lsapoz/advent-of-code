from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
points = [tuple(int(x) for x in line.split(",")) for line in lines]

max_area = 0
for i in range(len(points)):
    for j in range(i + 1, len(points)):
        x1, y1 = points[i]
        x2, y2 = points[j]
        max_area = max(max_area, (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1))
print(f"Part 1: {max_area}")
