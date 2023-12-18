from pathlib import Path
from collections import deque
from statistics import mean

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

DIR_MAP = {"U": (-1, 0), "D": (1, 0), "R": (0, 1), "L": (0, -1)}

# map out the edges
x, y = 0, 0
points = set([(x, y)])
for idx, line in enumerate(lines):
    dir, steps, color = line.split()
    for i in range(int(steps)):
        dx, dy = DIR_MAP[dir]
        x += dx
        y += dy
        points.add((x, y))

total = len(points)

# convert to a grid
x_values, y_values = zip(*points)
min_x, max_x = min(x_values), max(x_values)
min_y, max_y = min(y_values), max(y_values)
offset_x, offset_y = -1 * min_x, -1 * min_y
M, N = max_x - min_x + 1, max_y - min_y + 1

grid = [[" " for _ in range(N)] for _ in range(M)]
for i in range(min_x, max_x + 1):
    for j in range(min_y, max_y + 1):
        x, y = i + offset_x, j + offset_y
        grid[x][y] = "#" if (i, j) in points else "."

# flood fill the grid
# would be nice to figure out starting coordinates programmatically...
q = deque([(317, 1)])
while q:
    x, y = q.popleft()
    for dx, dy in DIR_MAP.values():
        nx, ny = x + dx, y + dy
        if nx >= 0 and nx < M and ny >= 0 and ny < N and grid[nx][ny] == ".":
            grid[nx][ny] = "#"
            q.append((nx, ny))
            total += 1

print(total)
