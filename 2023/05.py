from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()


class Map:
    def __init__(self, maps: list[list[int]]):
        self.maps = [(m[1], m[1] + m[2], m[0]) for m in maps]  # (in_start, in_end, out_start)
        self.maps.sort()

    def convert(self, input: int) -> int:
        for in_start, in_end, out_start in self.maps:
            if input < in_start:
                return input
            if in_start <= input < in_end:
                offset = input - in_start
                return out_start + offset
        return input


seeds = [int(x) for x in lines[0].split()[1:]]
map_defs: list[list[int]] = []
for line in lines[2:]:
    if line and line[0].isalpha():
        map_defs.append([])
    elif line and line[0].isnumeric():
        map_defs[-1].append([int(x) for x in line.split()])
maps = [Map(md) for md in map_defs]

lowest = float("inf")
for seed in seeds:
    for map in maps:
        seed = map.convert(seed)
    lowest = min(lowest, seed)
print(lowest)
