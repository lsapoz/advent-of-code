from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

dirs = {"L": -1, "R": 1}

dial = 50
part1, part2 = 0, 0
for line in lines:
    direction, distance = line[0], int(line[1:])
    prev_dial = dial
    dial = dial + (dirs[direction] * distance)
    quotient, dial = divmod(dial, 100)
    part1 += 1 if dial == 0 else 0
    part2 += abs(quotient)

    # edge cases
    # turned left and landed on 0
    if direction == "L" and dial == 0:
        part2 += 1
    # started at 0 and turned left
    if direction == "L" and prev_dial == 0:
        part2 -= 1

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
