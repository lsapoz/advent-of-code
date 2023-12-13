from pathlib import Path
from collections import deque

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

grid = [[x for x in line] for line in lines]
M, N = len(grid), len(grid[0])
S = next(((i, j) for i in range(M) for j in range(N) if grid[i][j] == "S"), None)

CARDINAL_DIRS = [(-1, 0), (0, -1), (0, 1), (1, 0)]
ORDINAL_DIRS = [*CARDINAL_DIRS, (-1, -1), (-1, 1), (1, -1), (1, 1)]
CARDINAL_DIR_MAP = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
PIPE_DIR_MAP = {
    "|": ["N", "S"],
    "-": ["E", "W"],
    "L": ["N", "E"],
    "J": ["N", "W"],
    "7": ["S", "W"],
    "F": ["S", "E"],
}


def trace_loop():
    # check if point is in grid bounds and is a pipe
    def _is_point_valid(_x, _y):
        return _x >= 0 and _x < M and _y >= 0 and _y < N and grid[_x][_y] in PIPE_DIR_MAP.keys()

    # check if we can move from one pipe to another (i.e. do they line up)
    def _is_move_valid(_x, _y, _nx, _ny):
        dir = (_x - _nx, _y - _ny)
        pipe = grid[_nx][_ny]
        return dir in [CARDINAL_DIR_MAP[d] for d in PIPE_DIR_MAP[pipe]]

    # find the two pipes next to the start which fit
    x, y = S
    surrounding = [(x + dx, y + dy) for dx, dy in CARDINAL_DIR_MAP.values()]
    valid_surrounding = [(nx, ny) for nx, ny in surrounding if _is_point_valid(nx, ny) and _is_move_valid(x, y, nx, ny)]
    assert len(valid_surrounding) == 2

    # figure out what pipe must be under S
    inverse_cardinal_dir_map = {v: k for k, v in CARDINAL_DIR_MAP.items()}
    inverse_pipe_dir_map = {tuple(sorted(v)): k for k, v in PIPE_DIR_MAP.items()}
    s_dirs = []
    for nx, ny in valid_surrounding:
        dir = (nx - x, ny - y)
        s_dirs.append(inverse_cardinal_dir_map[dir])
    s_pipe_shape = inverse_pipe_dir_map[(tuple(sorted(s_dirs)))]

    # replace S with its actual pipe shape
    grid[x][y] = s_pipe_shape

    # BFS in both directions from the start
    # once we hit the same pipe in the same number of steps, we've found our loop
    q = deque([(nx, ny, 1, x, y) for nx, ny in valid_surrounding])  # tuple of (curr_x, curr_y, steps, prev_x, prev_y)
    visited = set([(x, y, 0)])  # tuple of (x, y, steps)
    while q:
        point = q.popleft()
        x, y, dist, px, py = point
        if (x, y, dist) in visited:
            return set([(_x, _y) for _x, _y, _ in visited]), dist  # (loop points, max steps)
        visited.add((x, y, dist))
        for next_dir in PIPE_DIR_MAP[lines[x][y]]:
            dx, dy = CARDINAL_DIR_MAP[next_dir]
            nx, ny = x + dx, y + dy
            if (nx, ny) != (px, py) and _is_point_valid(nx, ny) and _is_move_valid(x, y, nx, ny):
                q.append((nx, ny, dist + 1, x, y))


def count_enclosed(_loop_points):
    # turn a grid coord into a 3x3 representation
    def _expand_space(_char: str):
        empty = {(i, j): "." for i in range(3) for j in range(3)}
        pipes = []
        match _char:
            case "|":
                pipes = [(0, 1), (1, 1), (2, 1)]
            case "-":
                pipes = [(1, 0), (1, 1), (1, 2)]
            case "L":
                pipes = [(0, 1), (1, 1), (1, 2)]
            case "J":
                pipes = [(0, 1), (1, 1), (1, 0)]
            case "7":
                pipes = [(1, 0), (1, 1), (2, 1)]
            case "F":
                pipes = [(1, 2), (1, 1), (2, 1)]
        return {**empty, **{(i, j): "0" for i, j in pipes}}

    # expand the grid's resolution to account for space between pipes
    expanded_grid = [[0] * (N * 3) for _ in range((M * 3))]
    for i in range(M):
        for j in range(N):
            expanded = _expand_space(grid[i][j] if (i, j) in _loop_points else ".")
            for (x, y), val in expanded.items():
                expanded_grid[(i * 3) + x][(j * 3) + y] = val

    # flood fill
    assert grid[0][0] not in _loop_points
    q = deque([(0, 0)])
    expanded_grid[0][0] = "X"
    while q:
        x, y = q.popleft()
        for dx, dy in CARDINAL_DIRS:
            nx, ny = x + dx, y + dy
            if nx >= 0 and nx < M * 3 and ny >= 0 and ny < N * 3 and expanded_grid[nx][ny] == ".":
                expanded_grid[nx][ny] = "X"
                q.append((nx, ny))

    # any points in the original grid that map to a 3x3 empty space must be enclosed
    num_enclosed = 0
    for i in range(M):
        for j in range(N):
            x, y = i * 3, j * 3
            if all(expanded_grid[x + dx][y + dy] == "." for dx, dy in ORDINAL_DIRS):
                num_enclosed += 1
    return num_enclosed


loop_points, max_steps = trace_loop()
print(f"Part 1: {max_steps}")
print(f"Part 2: {count_enclosed(loop_points)}")
