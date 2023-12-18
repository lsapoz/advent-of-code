from pathlib import Path
import heapq

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
grid = tuple(tuple(int(x) for x in line) for line in lines)
M, N = len(grid), len(grid[0])

CARDINAL_DIR_MAP = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}


def dijkstra():
    def _is_point_valid(_x, _y):
        return 0 <= _x < M and 0 <= _y < N

    def _next_dirs(_dir, _moves):
        dirs = []
        if _moves < 3 and _dir in CARDINAL_DIR_MAP.keys():
            dirs.append(_dir)
        if _dir in "NS":
            dirs.extend(["E", "W"])
        elif _dir in "EW":
            dirs.extend(["N", "S"])
        else:
            dirs.extend(["N", "S", "E", "W"])
        return dirs

    heap = [(0, 0, 0, "X", 0)]  # cost, x, y, dir, consecutive moves
    visited = set()

    while heap:
        cost, x, y, curr_dir, moves = heapq.heappop(heap)

        if (x, y, curr_dir, moves) in visited:
            continue
        visited.add((x, y, curr_dir, moves))

        if x == M - 1 and y == N - 1:
            return cost

        for next_dir in _next_dirs(curr_dir, moves):
            dx, dy = CARDINAL_DIR_MAP[next_dir]
            nx, ny = x + dx, y + dy
            if _is_point_valid(nx, ny):
                heapq.heappush(heap, (cost + grid[nx][ny], nx, ny, next_dir, 1 if next_dir != curr_dir else moves + 1))


print(dijkstra())
