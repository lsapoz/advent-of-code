from pathlib import Path
import re

here = Path(__file__).parent
lines = Path(here/"22.txt").read_text().splitlines()

board, instructions = lines[:lines.index('')], re.findall("\d+|\w", lines[-1])

M, N = len(board), max(len(line) for line in board)
grid = [[' ' for _ in range(N)] for _ in range(M)]
for i, row in enumerate(board):
    for j, cell in enumerate(row):
        grid[i][j] = cell

START = next((0, i) for i in range(N) if grid[0][i] == '.')
DIRS = {
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0)
}

def is_valid(x: int, y: int) -> bool:
    return 0 <= x < M and 0 <= y < N and grid[x][y] != ' '

def rotate(facing: int, turn: str) -> int:
    return (facing + (1 if turn == 'R' else -1)) % 4

def wrap(x: int, y: int, facing: int) -> tuple[int, int]:
    # march until we hit empty space
    dx, dy = DIRS[facing]
    while True:
        nx, ny = x - dx, y - dy
        if not is_valid(nx, ny):
            return (x, y) 
        x, y = nx, ny

def move(position: tuple[int, int], facing: int, steps: int) -> tuple[int, int]:
    x, y = position
    dx, dy = DIRS[facing]
    for _ in range(steps):
        nx, ny = x + dx, y + dy
        # if we went off the board, wrap around
        if not is_valid(nx, ny):
            nx, ny = wrap(nx, ny, facing)
        
        # if this is a wall, stop
        if (grid[nx][ny] == '#'):
            break

        # otherwise, move into position
        x, y = nx, ny
    
    return (x, y)

def simulate() -> int:
    position = START
    facing = 0
    for instruction in instructions:
        if instruction.isnumeric():
            position = move(position, facing, int(instruction))
        else:
            facing = rotate(facing, instruction)
    return (1000 * (position[0] + 1)) + (4 * (position[1] + 1)) + facing

print(f"Part 1: {simulate()}")
