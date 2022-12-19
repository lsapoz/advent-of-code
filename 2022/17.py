from pathlib import Path
from collections import namedtuple
from typing import  Set

here = Path(__file__).parent
jets = Path(here/"17.txt").read_text()

SHAPES = '-+L|o'
WIDTH = 7
LEFT_OFFSET = 2
BOTTOM_OFFSET = 4
Point = namedtuple("Point", "x y")


def spawn(shape: str, top: int) -> Set[Point]:
    ref_x = LEFT_OFFSET
    ref_y = top + BOTTOM_OFFSET

    if shape == '-':
        return set(Point(ref_x + i, ref_y) for i in range(4))
    if shape == '+':
        return set(Point(ref_x + i, ref_y + j) for (i, j) in [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)])
    if shape == 'L':
        return set(Point(ref_x + i, ref_y + j) for (i, j) in [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)])
    elif shape == '|':
        return set(Point(ref_x, ref_y + i) for i in range(4))
    elif shape == 'o':
        return set(Point(ref_x + i, ref_y + j) for (i, j) in [(0, 0), (0, 1), (1, 0), (1, 1)])


def simulate(num_rocks: int) -> int:
    grid: Set[Point] = set()

    def move(piece: Set[Point], offset: Point):
        moved_piece: Set[Point] = set()
        for point in piece:
            new_point = Point(point.x + offset.x, point.y + offset.y)
            if new_point.x < 0 or new_point.x >= WIDTH or new_point.y < 0 or new_point in grid:
                return piece
            moved_piece.add(new_point)
        return moved_piece

    def push(piece: Set[Point], jet: str):
        return move(piece, Point(1 if jet == '>' else -1, 0))

    def drop(piece: Set[Point]):
        return move(piece, Point(0, -1))

    jet, top = -1, -1
    for i in range(num_rocks):
        piece = spawn(SHAPES[i % len(SHAPES)], top)
        while True:
            jet = (jet + 1) % len(jets)
            piece = push(piece, jets[jet])

            dropped_piece = drop(piece)
            if dropped_piece == piece:
                break
            piece = dropped_piece
        top = max(top, *[point.y for point in piece])
        grid.update(piece)
    return top + 1


print(f"Part 1: {simulate(2022)}")
