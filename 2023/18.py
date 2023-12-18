from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

NUM_TO_DIR = {"0": "R", "1": "D", "2": "L", "3": "U"}
DIR_MAP = {"U": (-1, 0), "D": (1, 0), "R": (0, 1), "L": (0, -1)}


def calc_lava(part2=False):
    def _part_1_parser(_line: str):
        dir, steps, _ = _line.split()
        return (dir, int(steps))

    def _part_2_parser(_line: str):
        _, _, color = _line.split()
        dir = NUM_TO_DIR[color[-2]]
        steps = int(color[2:7], 16)
        return (dir, steps)

    x, y = 0, 0
    num_perimeter_points = 0
    polygon_area = 0
    parser = _part_2_parser if part2 else _part_1_parser
    for line in lines:
        prev_point = (x, y)
        dir, steps = parser(line)
        num_perimeter_points += steps

        dx, dy = DIR_MAP[dir]
        x += dx * steps
        y += dy * steps

        # https://en.wikipedia.org/wiki/Shoelace_formula
        x1, y1 = prev_point
        x2, y2 = x, y
        polygon_area += (x1 * y2) - (x2 * y1)
    polygon_area = abs(polygon_area) // 2

    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    # polygon_area = internal_area + (num_perimeter_points / 2) - 1
    # => internal_area = polygon_area - (num_perimeter_points / 2) + 1
    internal_area = polygon_area - (num_perimeter_points // 2) + 1

    return internal_area + num_perimeter_points


print(f"Part 1: {calc_lava()}")
print(f"Part 2: {calc_lava(True)}")
