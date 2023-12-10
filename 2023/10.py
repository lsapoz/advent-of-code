from pathlib import Path
from collections import deque

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

dirs = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}

pipe_dirs = {
    "|": ["N", "S"],
    "-": ["E", "W"],
    "L": ["N", "E"],
    "J": ["N", "W"],
    "7": ["S", "W"],
    "F": ["S", "E"],
}


def get_start():
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            if char == "S":
                return (x, y)


def is_point_valid(_x, _y):
    return _x >= 0 and _x < len(lines) and _y >= 0 and _y < len(lines[0]) and lines[_x][_y] in pipe_dirs.keys()


def is_move_valid(_x, _y, _nx, _ny):
    dir = (_x - _nx, _y - _ny)
    pipe = lines[_nx][_ny]
    return dir in [dirs[d] for d in pipe_dirs[pipe]]


def bfs(start: tuple[int, int]):
    x, y = start
    surrounding = [(x + dx, y + dy) for dx, dy in dirs.values()]
    q = deque([(nx, ny, 1, x, y) for nx, ny in surrounding if is_point_valid(nx, ny) and is_move_valid(x, y, nx, ny)])
    visited = set()
    while q:
        point = q.popleft()
        x, y, dist, px, py = point  # tuple of (curr_x, curr_y, steps_from_s, prev_x, prev_y)
        if (x, y, dist) in visited:
            return dist
        visited.add((x, y, dist))
        for next_dir in pipe_dirs[lines[x][y]]:
            dx, dy = dirs[next_dir]
            nx, ny = x + dx, y + dy
            if (nx, ny) != (px, py) and is_point_valid(nx, ny) and is_move_valid(x, y, nx, ny):
                q.append((nx, ny, dist + 1, x, y))


print(bfs(get_start()))
