from pathlib import Path

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
print(total)
