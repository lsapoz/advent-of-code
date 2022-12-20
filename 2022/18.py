from pathlib import Path

here = Path(__file__).parent
lines = Path(here/"18.txt").read_text().splitlines()
cubes = set([tuple(int(c) for c in line.split(',')) for line in lines])

sides = set([(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)])

surface_area = 0
for x, y, z in cubes:
    surrounding = set((x + dx, y + dy, z + dz) for (dx, dy, dz) in sides)
    uncovered = surrounding.difference(cubes)
    surface_area += len(uncovered)

print(surface_area)
