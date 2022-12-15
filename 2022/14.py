from pathlib import Path
from collections import namedtuple

here = Path(__file__).parent
lines = Path(here/"14.txt").read_text().splitlines()

Point = namedtuple("Point", "x y")
source = Point(500, 0)
rocks, sand = set(), set()

for line in lines:
    points = [Point(*map(int, point.split(','))) for point in line.split(' -> ')]
    for from_point, to_point in zip(points, points[1:]):
        a, b = sorted([from_point, to_point])
        if a.x == b.x:
            rocks.update(Point(a.x, y) for y in range(a.y, b.y + 1))
        else:
            rocks.update(Point(x, a.y) for x in range(a.x, b.x + 1))
floor = max(y for x, y in rocks)

# take in current sand positon, return next positon
def drop(cp: Point) -> Point: 
    for dx, dy in [(0, 1), (-1, 1), (1, 1)]:
        np = Point(cp.x + dx, cp.y + dy)
        if np not in rocks and np not in sand:
            return np
    return cp

def fill():
    while True:
        cp, np = source, drop(source) 
        while cp != np:
            cp = np
            np = drop(cp)
            if np.y > floor:
                return
        sand.add(cp)

fill()
print(f"Part 1: {len(sand)}")
