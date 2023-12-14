from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

GRID = tuple(tuple(x for x in line) for line in lines)

def transpose(_grid: tuple[tuple[str]]):
    return tuple(zip(*_grid))

def slide(_grid: tuple[tuple[str]], dir: str):
    new_grid = []
    for row in _grid if dir in "EW" else transpose(_grid):
        new_row = []
        num_rocks = 0
        for idx, char in enumerate(row if dir in "NW" else row[::-1]):
            match char:
                case "O":
                    num_rocks += 1
                case "#":
                    new_row.extend(["O"] * num_rocks)
                    new_row.extend(["."] * (idx - len(new_row)))
                    num_rocks = 0
                    new_row.append("#")
        new_row.extend(["O"] * num_rocks)
        new_row.extend(["."] * (len(row) - len(new_row)))
        new_grid.append(tuple(new_row if dir in "NW" else new_row[::-1]))
    return tuple(new_grid) if dir in "EW" else transpose(tuple(new_grid))

def cycle(_grid: tuple[tuple[str]]):
    for dir in 'NWSE':
        _grid = slide(_grid, dir)    
    return _grid

def calc_load(_grid: tuple[tuple[str]]):
    return sum((len(_grid) - idx) * row.count("O") for idx, row in enumerate(_grid))

print(f"Part 1: {calc_load(slide(GRID, "N"))}")

seen = {}
num_cycles = 1000000000
g = GRID
for i in range(num_cycles):
    if g in seen:
        break
    seen[g] = i
    g = cycle(g)

cycle_length = i - seen[g]
remainder = (num_cycles - i) % cycle_length
for i in range(remainder):
    g = cycle(g)

print(f"Part 2: {calc_load(g)}")
