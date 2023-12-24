from pathlib import Path
import z3

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

hailstones = [(tuple(map(int, line.replace(" @", ",").split(", ")))) for line in lines]
MIN, MAX = 200000000000000, 400000000000000


def get_line(hailstone: tuple[int, ...]):
    # y = mx + b
    # b = y - mx
    # b = y - (dy/dx)x
    x, y, z, dx, dy, dz = hailstone
    m = dy / dx
    b = y - (m * x)
    return (m, b)


def in_future(hailstone: tuple[int, ...], px: int, py: int):
    x, y, z, dx, dy, dz = hailstone
    x_in_future = px > x if dx > 0 else px < x
    y_in_future = py > y if dy > 0 else py < y
    return x_in_future and y_in_future


total = 0
for i in range(len(hailstones)):
    for j in range(i + 1, len(hailstones)):
        h1, h2 = hailstones[i], hailstones[j]
        m1, b1 = get_line(h1)
        m2, b2 = get_line(h2)

        if m2 - m1 == 0:
            continue

        x = (b1 - b2) / (m2 - m1)
        y = (m2 * x) + b2
        if MIN <= x <= MAX and MIN <= y <= MAX and in_future(h1, x, y) and in_future(h2, x, y):
            total += 1
print(f"Part 1: {total}")

s = z3.Solver()
x, y, z, dx, dy, dz = (z3.Int(var) for var in ["x", "y", "z", "dx", "dy", "dz"])
for idx, h in enumerate(hailstones):
    hx, hy, hz, hdx, hdy, hdz = h
    t = z3.Int(f"t{idx}")
    s.add(t >= 0)
    s.add(x + dx * t == hx + hdx * t)
    s.add(y + dy * t == hy + hdy * t)
    s.add(z + dz * t == hz + hdz * t)
s.check()
m = s.model()
print(f"Part 2: {m[x].as_long() + m[y].as_long() + m[z].as_long()}")
