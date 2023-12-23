from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
M, N = len(lines), len(lines[0])
points = {}
for i in range(M):
    for j in range(N):
        points[(i, j)] = lines[i][j]
        if points[(i, j)] == "S":
            START = (i, j)
            points[(i, j)] == "."


def bfs(start: tuple[int, int], target_steps: int):
    def _is_point_valid(_x, _y):
        return points[(_x % M, _y % N)] != "#"

    prev = set([start])
    for _ in range(target_steps):
        curr = set()
        for x, y in prev:
            for dx, dy in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                nx, ny = x + dx, y + dy
                if _is_point_valid(nx, ny):
                    curr.add((nx, ny))
        prev = curr
    return len(curr)


print(f"Part 1: {bfs(START, 64)}")


# 131 x 131 square
# start in the center at (65, 65)
# no obstacles directly up, down, left, right of the start
# perimeter has no obstacles
# after 65 steps, reach the perimeter of the first grid
# every 131 steps after that, reach the perimeter of the next set of grids
# target steps = 26501365 = 65 + 131 * 202300
f0 = bfs(START, 65)
f1 = bfs(START, 65 + 131)
f2 = bfs(START, 65 + (131 * 2))


# from day 9
def extrapolate(vals: list[int]):
    diffs, all_zero = [], True
    for i in range(1, len(vals)):
        diffs.append(vals[i] - vals[i - 1])
        if diffs[-1] != 0:
            all_zero = False
    next_val = 0 if all_zero else extrapolate(diffs)
    return vals[-1] + next_val


vals = [f0, f1, f2]
while len(vals) <= 202300:
    vals.append(extrapolate(vals[len(vals) - 3 : len(vals)]))
print(f"Part 2: {vals[-1]}")
