from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
times = [int(x) for x in lines[0][9:].split()]
distances = [int(x) for x in lines[1][9:].split()]


def get_ways_to_win(t: int, d: int):
    ways = 0
    for i in range(1, time - 1):
        if i * (time - i) > distance:
            ways += 1
        elif ways > 0:
            break
    return ways


total = 1
for time, distance in zip(times, distances):
    total *= get_ways_to_win(time, distance)
print(f"Part 1: {total}")

time = int(lines[0][9:].replace(" ", ""))
distance = int(lines[1][9:].replace(" ", ""))
print(f"Part 2: {get_ways_to_win(time, distance)}")
