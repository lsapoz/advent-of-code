from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
split = len(lines) - 1 - lines[::-1].index("")

shape_sizes = [0]
for line in lines[:split]:
    if line == "":
        shape_sizes.append(0)
        continue
    shape_sizes[-1] += line.count("#")

total = 0
for region in lines[split + 1 :]:
    width, length = [int(x) for x in region.split(":")[0].split("x")]
    quantities = [int(x) for x in region.split(":")[1].split()]

    shape_total = sum(
        shape_sizes[i] * quantity for i, quantity in enumerate(quantities)
    )
    total += 1 if shape_total <= (width * length) else 0
print(f"Part 1: {total}")
