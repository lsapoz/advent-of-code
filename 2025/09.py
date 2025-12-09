from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
points = [tuple(int(x) for x in line.split(",")) for line in lines]


def get_rectangle_area(p1: tuple[int, int], p2: tuple[int, int]):
    x1, y1 = p1
    x2, y2 = p2
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)


def is_rectangle_in_polygon(p1: tuple[int, int], p2: tuple[int, int]):
    p1_x, p1_y = p1
    p2_x, p2_y = p2
    rect_min_x, rect_max_x = min(p1_x, p2_x), max(p1_x, p2_x)
    rect_min_y, rect_max_y = min(p1_y, p2_y), max(p1_y, p2_y)

    # check to see if any edge in the polygon intersects the rectangle
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        edge_min_x, edge_max_x = min(x1, x2), max(x1, x2)
        edge_min_y, edge_max_y = min(y1, y2), max(y1, y2)

        if x1 == x2:  # vertical edge
            x_intersects_rect = rect_min_x < x1 < rect_max_x
            y_overlaps_rect = (
                edge_min_y <= rect_min_y < edge_max_y
                or edge_min_y < rect_max_y <= edge_max_y
            )
            if x_intersects_rect and y_overlaps_rect:
                return False
        else:  # horizontal edge
            y_intersects_rect = rect_min_y < y1 < rect_max_y
            x_overlaps_rect = (
                edge_min_x <= rect_min_x < edge_max_x
                or edge_min_x < rect_max_x <= edge_max_x
            )
            if y_intersects_rect and x_overlaps_rect:
                return False

    return True


part1, part2 = 0, 0
for i in range(len(points)):
    for j in range(i + 1, len(points)):
        area = get_rectangle_area(points[i], points[j])
        part1 = max(part1, area)
        if is_rectangle_in_polygon(points[i], points[j]):
            part2 = max(part2, area)
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
