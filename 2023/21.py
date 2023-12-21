from pathlib import Path
from collections import defaultdict

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
grid = [[x for x in line] for line in lines]
M, N = len(grid), len(grid[0])


def get_start():
    for i in range(M):
        for j in range(N):
            if grid[i][j] == "S":
                return (i, j)


def bfs(start: tuple[int, int], target_steps: int):
    def _is_point_valid(_x, _y):
        return 0 <= _x < M and 0 <= _y < N and grid[_x][_y] != "#"

    q = defaultdict(set)
    q[0].add(start)
    for i in range(target_steps):
        for x, y in q[i]:
            for dx, dy in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                nx, ny = x + dx, y + dy
                if _is_point_valid(nx, ny):
                    q[i + 1].add((nx, ny))
    return len(q[target_steps])


for i in range(M):
    for j in range(N):
        if grid[i][j] == "S":
            print(bfs(get_start(), 64))
