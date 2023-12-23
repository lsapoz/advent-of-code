from pathlib import Path
from collections import defaultdict

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
grid = [[x for x in line] for line in lines]
M, N = len(grid), len(grid[0])
START, END = (0, 1), (M - 1, N - 2)
DIRS = [(-1, 0), (0, -1), (0, 1), (1, 0)]
SLOPES = "^<>v"


def get_edges(slippery=True):
    def _is_valid(_x, _y):
        return 0 <= _x < M and 0 <= _y < N and grid[_x][_y] != "#"

    edges = defaultdict(dict)
    for x in range(M):
        for y in range(N):
            if not _is_valid(x, y):
                continue
            valid_dirs = [DIRS[SLOPES.index(grid[x][y])]] if grid[x][y] in SLOPES and slippery else DIRS
            for dx, dy in valid_dirs:
                nx, ny = x + dx, y + dy
                if _is_valid(nx, ny):
                    edges[(x, y)][(nx, ny)] = 1

    for point, neighbors in edges.items():
        if len(neighbors) == 2:
            l, r = neighbors
            if slippery and any(grid[_x][_y] != "." for (_x, _y) in [point, l, r]):
                continue
            del edges[l][point]
            del edges[r][point]
            edges[l][r] = neighbors[l] + neighbors[r]
            edges[r][l] = edges[l][r]
    return edges


def dfs(x: int, y: int, edges: dict, visited: set, curr_path: int):
    if (x, y) == END:
        return curr_path

    visited.add((x, y))
    longest_path = 0

    for nx, ny in edges[(x, y)].keys():
        if (nx, ny) not in visited:
            length = edges[(x, y)][(nx, ny)]
            longest_path = max(longest_path, dfs(nx, ny, edges, visited, curr_path + length))

    visited.remove((x, y))
    return longest_path


print(f"Part 1: {dfs(*START, get_edges(), set(), 0)}")
print(f"Part 2: {dfs(*START, get_edges(slippery=False), set(), 0)}")
