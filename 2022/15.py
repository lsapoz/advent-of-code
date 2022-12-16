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


def manhattan(a: Point, b: Point):
    return abs(a.x - b.x) + abs(a.y - b.y)

# find the number of positions in a given row that cannot contain a beacon
def beaconless(row: int) -> int:
    positions: Set[Point] = set()
    for sensor, beacon in pairs:
        manhattan_distance = manhattan(sensor, beacon)

        # check if beacon's detection diamond reaches the target row
        vertical_distance_from_row = abs(row - sensor.y)
        if vertical_distance_from_row <= manhattan_distance:
            num_positions_each_side = manhattan_distance - vertical_distance_from_row
            for x in range(sensor.x - num_positions_each_side, sensor.x + num_positions_each_side + 1):
                positions.add(Point(x, row))

    return len(positions.difference(beacons))


# check if a given point is in the detection diamond of any beacon
def is_in_detection_diamond(point: Point) -> bool:
    for sensor, beacon in pairs:
        if manhattan(sensor, point) <= manhattan(sensor, beacon):
            return True
    return False


# find the first point on the outside perimeter of a beacon's detection diamond 
# that is not located within any other beacon's detection diamond
def missing_beacon(cap: int) -> Point:
    for sensor, beacon in pairs:
        md = manhattan(sensor, beacon) 

        for y in range(max(0, sensor.y - md - 1), min(cap, sensor.y + md + 1) + 1):
            vd = abs(y - sensor.y)  # vertical distance of the current row from the sensor
            hd = md - vd  # horizontal distance of the edge of the current row from the center

            perimiter_points = [Point(sensor.x - hd - 1, y), Point(sensor.x + hd + 1, y)]
            for point in perimiter_points:
                if 0 <= point.x <= cap and not is_in_detection_diamond(point):
                    return point


print(f'Part 1: {beaconless(2000000)}')

beacon = missing_beacon(4000000)
print(f'Part 2: {4000000 * beacon.x + beacon.y}')
