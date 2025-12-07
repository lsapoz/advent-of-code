from pathlib import Path
from collections import deque
from functools import cache

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
grid = [[x for x in line] for line in lines]
M, N = len(grid), len(grid[0])

start = (0, grid[0].index("S"))


def bfs():
    q = deque([start])
    visited = set([start])
    num_splits = 0

    def _visit(_x, _y):
        if (_x, _y) not in visited:
            visited.add((_x, _y))
            q.append((_x, _y))

    while q:
        x, y = q.popleft()
        if x == M:
            continue
        if grid[x][y] == "^":
            num_splits += 1
            _visit(x + 1, y - 1)
            _visit(x + 1, y + 1)
        else:
            _visit(x + 1, y)

    return num_splits


@cache
def dfs(x: int, y: int):
    paths = 0

    if x == M:
        return 1

    if grid[x][y] == "^":
        paths += dfs(x + 1, y - 1)
        paths += dfs(x + 1, y + 1)
    else:
        paths += dfs(x + 1, y)

    return paths


print(f"Part 1: {bfs()}")
print(f"Part 2: {dfs(*start)}")
