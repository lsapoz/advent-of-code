from pathlib import Path
from math import prod

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

part1 = 0
for problem in zip(*[[x for x in line.split()] for line in lines]):
    op = problem[-1]
    numbers = [int(x) for x in problem[:-1]]
    part1 += sum(numbers) if op == "+" else prod(numbers)
print(f"Part 1: {part1}")


grid = [[x for x in line] for line in lines]
M, N = len(grid), len(grid[0])
part2 = 0
for j in range(N):
    # if there's an operator in the bottom row, we've started a new number
    if grid[M - 1][j] != " ":
        op = grid[M - 1][j]
        numbers = []

    number = ""
    for i in range(M - 1):
        number += grid[i][j] if grid[i][j] != " " else ""
    if number:
        numbers.append(int(number))

    # if we're in the final column
    # OR if there's an operator in the bottom row two columns from now,
    # we've reached the end of the current problem
    if j == N - 1 or (j + 2 < N and grid[M - 1][j + 2] != " "):
        part2 += sum(numbers) if op == "+" else prod(numbers)

print(f"Part 2: {part2}")
