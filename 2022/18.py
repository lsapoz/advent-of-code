from pathlib import Path
from collections import deque

here = Path(__file__).parent
lines = Path(here/"18.txt").read_text().splitlines()

scanned_cubes = set([tuple(int(c) for c in line.split(',')) for line in lines])
sides = set([(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)])

def get_surface_area(cubes):
    surface_area = 0
    for x, y, z in cubes:
        surrounding = set((x + dx, y + dy, z + dz) for (dx, dy, dz) in sides)
        uncovered = surrounding.difference(cubes)
        surface_area += len(uncovered)
    return surface_area

def get_air_gaps(cubes):
    x_coords, y_coords, z_coords = zip(*cubes)
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    min_z, max_z = min(z_coords), max(z_coords)

    all_points = set()
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                all_points.add((x, y, z))

    flooded = set()
    q = deque([(min_x, min_y, min_z)])
    while q:
        x, y, z = q.popleft()
        for dx, dy, dz in sides:
            nx, ny, nz = x + dx, y + dy, z + dz
            c = (nx, ny, nz)
            if min_x <= nx <= max_x and min_y <= ny <= max_y and min_z <= nz <= max_z and c not in cubes and c not in flooded:
                flooded.add(c)
                q.append(c)

    return all_points - cubes - flooded

print(f"Part 1: {get_surface_area(scanned_cubes)}")
print(f"Part 2: {get_surface_area(scanned_cubes.union(get_air_gaps(scanned_cubes)))}")
