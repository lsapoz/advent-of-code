from pathlib import Path
import math

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

max_cubes = {"red": 12, "green": 13, "blue": 14}


def is_game_possible(game_sets: list[str]):
    for s in game_sets:
        cubes = s.split(",")
        for cube in cubes:
            num, color = cube.strip().split(" ")
            if int(num) > max_cubes[color]:
                return False
    return True


def get_game_power(game_sets: list[str]):
    min_cubes = {"red": 0, "green": 0, "blue": 0}
    for s in game_sets:
        cubes = s.split(",")
        for cube in cubes:
            num, color = cube.strip().split(" ")
            min_cubes[color] = max(min_cubes[color], int(num))
    return math.prod(min_cubes.values())


ids_sum = 0
powers_sum = 0
for idx, line in enumerate(lines):
    game_no, results = line.split(":")
    sets = results.split(";")
    if is_game_possible(sets):
        ids_sum += idx + 1
    powers_sum += get_game_power(sets)
print(f"Part 1: {ids_sum}")
print(f"Part 2: {powers_sum}")
