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
    0: (0, 1),  # right
    1: (1, 0),  # down
    2: (0, -1), # left 
    3: (-1, 0)  # up
}


"""
 12
 3
45
6 
"""
FACE_SIZE = 50
# for each face, where does the upper left corner of the face start
FACE_OFFSETS = {
    1: (0, FACE_SIZE),
    2: (0, FACE_SIZE * 2),
    3: (FACE_SIZE, FACE_SIZE),
    4: (2 * FACE_SIZE, 0),
    5: (2 * FACE_SIZE, FACE_SIZE),
    6: (3 * FACE_SIZE, 0)
}
# when leaving X face going right/down/left/up,
# 1. which face do we end up on
# 2. how many times do we need to turn right to be facing the correct direction on the new face
TRANSITIONS = {
    1: [(2, 0), (3, 0), (4, 2), (6, 1)],  
    2: [(5, 2), (3, 1), (1, 0), (6, 0)],
    3: [(2, 3), (5, 0), (4, 3), (1, 0)],
    4: [(5, 0), (6, 0), (1, 2), (3, 1)],
    5: [(2, 2), (6, 1), (4, 0), (3, 0)],
    6: [(5, 3), (2, 0), (1, 3), (4, 0)]
}

def is_valid(x: int, y: int) -> bool:
    return 0 <= x < M and 0 <= y < N and grid[x][y] != ' '

def rotate(facing: int, turn: str) -> int:
    return (facing + (1 if turn == 'R' else -1)) % 4

def wrap(x: int, y: int, facing: int) -> tuple[int, int, int]:
    # march until we hit empty space
    dx, dy = DIRS[facing]
    while True:
        nx, ny = x - dx, y - dy
        if not is_valid(nx, ny):
            return (x, y, facing) 
        x, y = nx, ny

def which_face(x: int, y: int) -> int:
    for face, (ox, oy) in FACE_OFFSETS.items():
        if ox <= x < ox + FACE_SIZE and oy <= y < oy + FACE_SIZE:
            return face

def wrap3d(current_face: int, x: int, y: int, facing: int) -> tuple[int, int, int]:
    next_face, turns = TRANSITIONS[current_face][facing]

    # normalize the current coordinates relative to a single face
    x, y = x % 50, y % 50

    # rotate
    for _ in range(turns):
        x, y = y, FACE_SIZE - x  - 1
        facing = rotate(facing, 'R')

    # apply the offsets for the new face
    ox, oy = FACE_OFFSETS[next_face]
    x, y = x + ox, y + oy
    return x, y, facing
 
def move(x: int, y: int, facing: int, steps: int, is3d: bool) -> tuple[int, int, int]:
    for _ in range(steps):
        current_face = which_face(x, y)
        dx, dy = DIRS[facing]
        nx, ny, nf = x + dx, y + dy, facing
        # if we went off the board, wrap around
        if not is_valid(nx, ny):
            nx, ny, nf = wrap3d(current_face, nx, ny, nf) if is3d else wrap(nx, ny, nf)
        
        # if this is a wall, stop
        if (grid[nx][ny] == '#'):
            break

        # otherwise, move into position
        x, y, facing = nx, ny, nf
    
    return (x, y, facing)

def simulate(is3d: bool) -> int:
    x, y = START
    facing = 0
    for instruction in instructions:
        if instruction.isnumeric():
            x, y, facing = move(x, y, facing, int(instruction), is3d)
        else:
            facing = rotate(facing, instruction)
    return (1000 * (x + 1)) + (4 * (y + 1)) + facing

print(f"Part 1: {simulate(is3d=False)}")
print(f"Part 2: {simulate(is3d=True)}")
