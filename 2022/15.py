from pathlib import Path
from collections import namedtuple
from typing import List, Set, Tuple
import re

here = Path(__file__).parent
lines = Path(here/"15.txt").read_text().splitlines()

Point = namedtuple("Point", "x y")
beacons: Set[Point] = set()
pairs: List[Tuple[Point, Point]] = []  # list (sensor, beacon) pairs

for line in lines:
    sx, sy, bx, by = [int(x) for x in re.sub('[^-0-9]', ' ', line).split()]
    sensor, beacon = Point(sx, sy), Point(bx, by)
    beacons.add(beacon)
    pairs.append((sensor, beacon))

# find the number of positions in a given row that cannot contain a beacon
def beaconless(row: int) -> int:
    positions: Set[Point] = set()
    for pair in pairs:
        sensor, beacon = pair
        manhattan_distance = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)

        # check if beacon's detection diamond reaches the target row
        vertical_distance_from_row = abs(row - sensor.y)
        if vertical_distance_from_row <= manhattan_distance:
            num_positions_each_side = manhattan_distance - vertical_distance_from_row
            for x in range(sensor.x - num_positions_each_side, sensor.x + num_positions_each_side + 1):
                positions.add(Point(x, row))

    return len(positions.difference(beacons))

print(f'Part 1: {beaconless(2000000)}')
