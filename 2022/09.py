from pathlib import Path
from collections import namedtuple
import math

here = Path(__file__).parent
lines = Path(here/"09.txt").read_text().splitlines()

Point = namedtuple("Point", "x y")

directions = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, 1),
    'D': (0, -1)
}

# return 1 if number is postive or -1 if negative (or 0 if 0)
def sign(x: int) -> int:
    return int(math.copysign(1, x))

# determine if two points are touching (including diagonally) 
def are_touching(a: Point, b: Point) -> bool:
    return math.dist(a, b) <= math.sqrt(2)

def in_same_row_or_column(a: Point, b: Point) -> bool:
    return (a.x == b.x) or (a.y == b.y)

# return the change in x,y position to move b towards a vertically or horizontally
def get_straight_step(a: Point, b: Point) -> tuple:
    if a.y == b.y:  # same row
        return sign(a.x - b.x), 0 
    return 0, sign(a.y - b.y), 

# return the change in x,y position to move point b towards point a diagonally 
def get_diagonal_step(a: Point, b: Point) -> tuple:
    return sign(a.x - b.x), sign(a.y - b.y)

# return the change in x,y position to move point b towards point a
def get_tail_movement(a: Point, b: Point) -> tuple:
    if are_touching(a, b):
        return 0, 0
    if in_same_row_or_column(a, b):
        return get_straight_step(a, b)
    return get_diagonal_step(a, b)

def unique_tail_positions(num_knots: int) -> int:
    visited = set()
    knots = [Point(0, 0) for _ in range(num_knots)]
    for line in lines:
        direction, magnitude = line.split()
        hdx, hdy = directions[direction]  # delta x,y for the head/leading knot
        for _ in range(int(magnitude)):
            knots[0] = Point(knots[0].x + hdx, knots[0].y + hdy)
            for i in range(1, num_knots):
                tdx, tdy = get_tail_movement(knots[i-1], knots[i])
                knots[i] = Point(knots[i].x + tdx, knots[i].y + tdy)
            visited.add(knots[-1])
    return len(visited)    

print(f"Part 1: {unique_tail_positions(2)}")        
print(f"Part 2: {unique_tail_positions(10)}")
