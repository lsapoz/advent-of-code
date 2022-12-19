from pathlib import Path
from collections import namedtuple
from typing import Dict, List, Optional, Set, Tuple

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
    grid: Set[Point] = set()  # set of all points representing stopped rocks
    height_deltas: List[int] = []  # list containing the change in height of the tower after every rock stops falling
    keys: Dict[Tuple, int] = {} # dict that maps a key of (shape_idx, jet_idx, height_delta) to the rock_idx

    def move(piece: Set[Point], offset: Point) -> Set[Point]:
        moved_piece: Set[Point] = set()
        for point in piece:
            new_point = Point(point.x + offset.x, point.y + offset.y)
            if new_point.x < 0 or new_point.x >= WIDTH or new_point.y < 0 or new_point in grid:
                return piece
            moved_piece.add(new_point)
        return moved_piece

    def push(piece: Set[Point], jet: str) -> Set[Point]:
        return move(piece, Point(1 if jet == '>' else -1, 0))

    def drop(piece: Set[Point]) -> Set[Point]:
        return move(piece, Point(0, -1))

    # track patterns in height diff
    # once a cycle is detected, return the # of rocks in each cycle
    def track_cycle(rock_idx: int, shape_idx: int, jet_idx: int, height_delta: int) -> Optional[int]:
        height_deltas.append(height_delta)
        key = (shape_idx, jet_idx, height_delta)
        if key in keys:
            cycle_length = rock_idx - keys[key]

            # check that the last cycle_length height deltas match the previous cycles exactly
            if len(height_deltas) > cycle_length * 2 and height_deltas[-cycle_length:] == height_deltas[-cycle_length*2:-cycle_length]:
                return cycle_length

        keys[key] = rock_idx
        return None

    rock_idx = 0
    jet_idx, top = -1, -1
    cycle_length = None
    while rock_idx < num_rocks:
        shape_idx = rock_idx % len(SHAPES)
        piece = spawn(SHAPES[shape_idx], top)
        while True:
            jet_idx = (jet_idx + 1) % len(jets)
            piece = push(piece, jets[jet_idx])

            dropped_piece = drop(piece)
            if dropped_piece == piece:
                break
            piece = dropped_piece
        height_delta = max(top, *[point.y for point in piece]) - top
        top += height_delta
        grid.update(piece)

        cycle_length = track_cycle(rock_idx, shape_idx, jet_idx, height_delta)
        rock_idx += 1
        
        if cycle_length:
            break

    current_height = top + 1
    if not cycle_length:
        return current_height

    cycles, remainder = divmod(num_rocks - rock_idx, cycle_length)
    cycle_height = sum(height_deltas[-cycle_length:])
    remainder_height = sum(height_deltas[-cycle_length:-cycle_length+remainder])

    return current_height + (cycles * cycle_height) + remainder_height


print(f"Part 1: {simulate(2022)}")
print(f"Part 2: {simulate(1000000000000)}")
