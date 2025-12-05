from pathlib import Path

grid = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
M, N = len(grid), len(grid[0])

dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def count_adjacent_rolls(x: int, y: int):
    total = 0
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < M and 0 <= ny < N and grid[nx][ny] == "@":
            total += 1
    return total


num_accessible = 0
for i in range(M):
    for j in range(N):
        if grid[i][j] == "@" and count_adjacent_rolls(i, j) < 4:
            num_accessible += 1
print(f"Part 1: {num_accessible}")
