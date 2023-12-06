from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
times = [int(x) for x in lines[0][9:].split()]
distances = [int(x) for x in lines[1][9:].split()]

total = 1
for time, distance in zip(times, distances):
    ways = 0
    for i in range(1, time - 1):
        if i * (time - i) > distance:
            ways += 1
    total *= ways
print(total)
