from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

split_idx = lines.index("")
ranges = [(int(r[0]), int(r[1])) for r in (x.split("-") for x in lines[:split_idx])]
ingredients = [int(x) for x in lines[split_idx + 1 :]]


def is_fresh(ingredient: int):
    for a, b in ranges:
        if a <= ingredient <= b:
            return True
    return False


num_fresh = 0
for ingredient in ingredients:
    num_fresh += 1 if is_fresh(ingredient) else 0
print(f"Part 1: {num_fresh}")
