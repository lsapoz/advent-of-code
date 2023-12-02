from pathlib import Path

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


ids_sum = 0
for idx, line in enumerate(lines):
    game_no, results = line.split(":")
    if is_game_possible(results.split(";")):
        ids_sum += idx + 1
print(ids_sum)
