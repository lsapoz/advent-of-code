from pathlib import Path
import math

here = Path(__file__).parent
lines = Path(here/"09.txt").read_text().splitlines()

directions = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, 1),
    'D': (0, -1)
}

def are_touching(x1, y1, x2, y2):
    return math.dist((x1, y1), (x2, y2)) <= math.sqrt(2)

def in_same_row_or_column(x1, y1, x2, y2):
    return x1 == x2 or y1 == y2

def get_diagonal_step(x1, y1, x2, y2):
    dx = 1 if x1 - x2 > 0 else -1
    dy = 1 if y1 - y2 > 0 else -1
    return dx, dy

hx, hy = 0, 0
tx, ty = 0, 0
visited = set()
for line in lines:
    direction, magnitude = line.split()
    hdx, hdy = directions[direction]
    for i in range(int(magnitude)):
        hx, hy = hx + hdx, hy + hdy

        if are_touching(hx, hy, tx, ty):
            tdx, tdy = 0, 0
        elif in_same_row_or_column(hx, hy, tx, ty):
            tdx, tdy = hdx, hdy
        else:
            tdx, tdy = get_diagonal_step(hx, hy, tx, ty)

        tx, ty = tx + tdx, ty + tdy
        visited.add((tx, ty))

print(f"Tail visited {len(visited)} positions")        
