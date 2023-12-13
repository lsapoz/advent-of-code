from pathlib import Path
from functools import cache

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()


@cache
def get_valid_arrangements(springs: str, sizes: tuple[int, ...], curr_group_size=0):
    if len(springs) == 0:
        if len(sizes) == 1 and curr_group_size == sizes[0]:
            return 1
        if len(sizes) == 0 and curr_group_size == 0:
            return 1
        return 0

    current_spring = springs[0]
    remaining = springs[1:]
    match current_spring:
        case "?":
            if_working = get_valid_arrangements("#" + remaining, sizes, curr_group_size)
            if_broken = get_valid_arrangements("." + remaining, sizes, curr_group_size)
            return if_working + if_broken
        case "#":
            if len(sizes) > 0 and curr_group_size < sizes[0]:
                return get_valid_arrangements(remaining, sizes, curr_group_size + 1)
        case ".":
            if curr_group_size == 0:
                return get_valid_arrangements(remaining, sizes, 0)
            if curr_group_size == sizes[0]:
                return get_valid_arrangements(remaining, sizes[1:], 0)
    return 0


part1 = 0
part2 = 0
for line in lines:
    springs, group_sizes = line.split()
    sizes = tuple(map(int, group_sizes.split(",")))
    part1 += get_valid_arrangements(springs, tuple(map(int, group_sizes.split(","))))
    part2 += get_valid_arrangements("?".join([springs] * 5), tuple(map(int, (",".join([group_sizes] * 5)).split(","))))
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
