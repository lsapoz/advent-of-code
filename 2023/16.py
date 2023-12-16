from pathlib import Path
from collections import deque

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
grid = tuple(tuple(x for x in line) for line in lines)

CARDINAL_DIR_MAP = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}


def bfs(start: tuple[int, int, str]):
    def _is_point_valid(_x, _y):
        return 0 <= _x < len(grid) and 0 <= _y < len(grid[0])

    def _next_dirs(_char, _dir):
        match (_char, _dir):
            case (".", _) | ("-", "E") | ("-", "W") | ("|", "N") | ("|", "S"):
                return _dir
            case ("/", "E") | ("\\", "W"):
                return "N"
            case ("/", "N") | ("\\", "S"):
                return "E"
            case ("/", "W") | ("\\", "E"):
                return "S"
            case ("/", "S") | ("\\", "N"):
                return "W"
            case ("-", "N") | ("-", "S"):
                return "EW"
            case ("|", "E") | ("|", "W"):
                return "NS"

    visited = set()
    q = deque([start])
    while q:
        x, y, dir = q.popleft()
        visited.add((x, y, dir))
        char = grid[x][y]
        next_dirs = _next_dirs(char, dir)
        for dir in next_dirs:
            dx, dy = CARDINAL_DIR_MAP[dir]
            nx, ny = x + dx, y + dy
            if _is_point_valid(nx, ny) and (nx, ny, dir) not in visited:
                q.append((nx, ny, dir))
    return len(set((x, y) for (x, y, _) in visited))


print(f"Part 1: {bfs((0, 0, 'E'))}")

most_tiles = 0
for x in range(len(grid)):
    most_tiles = max(most_tiles, bfs((x, 0, "E")))
    most_tiles = max(most_tiles, bfs((x, len(grid[0]) - 1, "W")))
for y in range(len(grid[0])):
    most_tiles = max(most_tiles, bfs((0, y, "S")))
    most_tiles = max(most_tiles, bfs((len(grid) - 1, y, "N")))
print(f"Part 2: {most_tiles}")
