from pathlib import Path
import sys

sys.setrecursionlimit(3000)

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
grid = [[x for x in line] for line in lines]
M, N = len(grid), len(grid[0])
START, END = (0, 1), (M - 1, N - 2)
DIRS = [(-1, 0), (0, -1), (0, 1), (1, 0)]
SLOPES = "^<>v"


def dfs(x: int, y: int, visited: set, curr_path: int):
    def _is_valid(_x, _y):
        return 0 <= _x < M and 0 <= _y < N and grid[_x][_y] != "#"

    if (x, y) == END:
        return curr_path

    visited.add((x, y))
    longest_path = 0

    valid_dirs = [DIRS[SLOPES.index(grid[x][y])]] if grid[x][y] in SLOPES else DIRS
    for dx, dy in valid_dirs:
        nx, ny = x + dx, y + dy
        if _is_valid(nx, ny) and (nx, ny) not in visited:
            longest_path = max(longest_path, dfs(nx, ny, visited, curr_path + 1))

    visited.remove((x, y))
    return longest_path


print(f"Part 1: {dfs(*START, set(), 0)}")
