from pathlib import Path
from collections import defaultdict

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

bricks = {}  # brick num: brick coords
is_vertical = []  # idx = brick_num, True if vertical
max_x, max_y, max_z = 0, 0, 0
for idx, line in enumerate(lines):
    x1, y1, z1, x2, y2, z2 = map(int, line.replace("~", ",").split(","))
    if x1 != x2:
        bricks[idx] = [(x, y1, z1) for x in range(x1, x2 + 1)]
        is_vertical.append(False)
    elif y1 != y2:
        bricks[idx] = [(x1, y, z1) for y in range(y1, y2 + 1)]
        is_vertical.append(False)
    elif z1 != z2:
        bricks[idx] = [(x1, y1, z) for z in range(z1, z2 + 1)]
        is_vertical.append(True)
    else:
        bricks[idx] = [(x1, y1, z1)]
        is_vertical.append(False)
    max_x, max_y, max_z = max(max_x, x2), max(max_y, y2), max(max_z, z2)
M, N, O = max_x + 1, max_y + 1, max_z + 1

# build a grid with where each coordinate indicates which brick occupies that point
points = {v: brick_num for brick_num, points in bricks.items() for v in points}
grid = []
for i in range(M):
    grid.append([])
    for j in range(N):
        grid[i].append([])
        for k in range(O):
            grid[i][j].append(points.get((i, j, k), -1))


# for a set of points representing the lowest point of a brick
# find how far it can drop in the grid before running into something
def get_z_offset(_points: list[list[list[int]]]):
    k_curr = _points[0][2]  # assume all points have the same z
    for k_lower in reversed(range(1, k_curr)):
        for x, y, z in _points:
            if grid[x][y][k_lower] >= 0:
                return k_curr - k_lower - 1
    return k_curr - 1


# drop all bricks, working from the bottom up
# if vertical, drop the column down until it's hitting something
# if horizontal, drop them all down until any one brick is hitting something
dropped = set()
for k in range(1, O):
    for i in range(M):
        for j in range(N):
            brick_num = grid[i][j][k]
            if brick_num < 0 or brick_num in dropped:
                continue
            dropped.add(brick_num)
            points_to_check = [(i, j, k)] if is_vertical[brick_num] else bricks[brick_num]
            offset = get_z_offset(points_to_check)
            for idx, (x, y, z) in enumerate(bricks[brick_num]):
                bricks[brick_num][idx] = (x, y, z - offset)
                grid[x][y][z] = -1
                grid[x][y][z - offset] = brick_num


# for each brick, check if there is a brick directly above it
# if there is, it supports that brick
supported_by = defaultdict(set)  # brick_num: [bricks it is supported by]
for brick_num, points in bricks.items():
    for x, y, z in points:
        above = grid[x][y][z + 1]
        if above >= 0 and above != brick_num:
            supported_by[above].add(brick_num)

# assume we can disintegrate all bricks by default
# if any brick is supported by just one brick
# we can't disintegrate that brick
can_disintegrate = set(bricks.keys())
for support_bricks in supported_by.values():
    if len(support_bricks) == 1:
        critical_brick = support_bricks.pop()
        if critical_brick in can_disintegrate:
            can_disintegrate.remove(critical_brick)

print(f"Part 1: {len(can_disintegrate)}")
