from pathlib import Path
from collections import namedtuple

here = Path(__file__).parent
lines = Path(here/"14.txt").read_text().splitlines()

Point = namedtuple("Point", "x y")
source = Point(500, 0)

rocks = set()
for line in lines:
    points = [Point(*map(int, point.split(','))) for point in line.split(' -> ')]
    for from_point, to_point in zip(points, points[1:]):
        a, b = sorted([from_point, to_point])
        if a.x == b.x:
            rocks.update(Point(a.x, y) for y in range(a.y, b.y + 1))
        else:
            rocks.update(Point(x, a.y) for x in range(a.x, b.x + 1))


def fill(floor: int, fall_through_floor: bool) -> int:   
    sand = set()

    # take in current sand positon, return next positon
    def drop(cp: Point) -> Point: 
        for dx, dy in [(0, 1), (-1, 1), (1, 1)]:
            np = Point(cp.x + dx, cp.y + dy)
            if np not in rocks and np not in sand and (fall_through_floor or np.y != floor):
                return np
        return cp

    while True:
        cp, np = source, drop(source)
        if cp == np:
            return len(sand) + 1

        while cp != np:
            cp = np
            np = drop(cp)
            if np.y > floor:
                return len(sand)
        sand.add(cp)

floor = max(y for x, y in rocks)
print(f"Part 1: {fill(floor, True)}")

floor += 2
print(f"Part 2: {fill(floor, False)}")
