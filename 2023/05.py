from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()


class Map:
    def __init__(self, maps: list[list[int]]):
        self.maps = [(m[1], m[1] + m[2], m[0] - m[1]) for m in maps]  # (src_start, src_end, dst_offset)
        self.maps.sort()

    def convert(self, input: int) -> int:
        for src_start, src_end, offset in self.maps:
            if src_start <= input < src_end:
                return input + offset
        return input

    def convert_ranges(self, inputs: list[tuple[int, int]]) -> list[tuple[int, int]]:
        converted = []
        for src_start, src_end, offset in self.maps:
            out_of_range = []
            while inputs:
                s, e = inputs.pop()
                if e <= src_start or s > src_end:
                    out_of_range.append((s, e))
                elif src_start <= s <= e <= src_end:
                    converted.append((s + offset, e + offset))
                elif s < src_start < e <= src_end:
                    out_of_range.append((s, src_start))
                    converted.append((src_start + offset, e + offset))
                elif src_start <= s < src_end <= e:
                    converted.append((s + offset, src_end + offset))
                    out_of_range.append((src_end, e))
                elif s <= src_start < src_end <= e:
                    out_of_range.append((s, src_start))
                    converted.append((src_start + offset, src_end + offset))
                    out_of_range.append((src_end, e))
            inputs = out_of_range
        return converted + out_of_range


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
print(f"Part 1: {lowest}")

lowest = float("inf")
seed_ranges = [[(seeds[i], seeds[i] + seeds[i + 1])] for i in range(0, len(seeds), 2)]
for ranges in seed_ranges:
    for map in maps:
        ranges = map.convert_ranges(ranges)
    lowest = min(lowest, min(ranges)[0])
print(f"Part 2: {lowest}")
