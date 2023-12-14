from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

GRID = [[x for x in line] for line in lines]


def transpose(_grid: list[list[str]]):
    return list(zip(*_grid))


def slide_left(_grid: list[list[str]]):
    new_grid = []
    for row in _grid:
        new_row = []
        num_rocks = 0
        for idx, char in enumerate(row):
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
        new_grid.append(new_row)
    return new_grid


def calc_load(_grid: list[list[str]]):
    return sum((len(_grid) - idx) * row.count("O") for idx, row in enumerate(_grid))


transposed = transpose(GRID)
tilted = slide_left(transposed)
transposed_back = transpose(tilted)
print(calc_load(transposed_back))
