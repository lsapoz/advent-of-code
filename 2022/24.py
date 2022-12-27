from pathlib import Path
from collections import deque

here = Path(__file__).parent
lines = Path(here/"24.txt").read_text().splitlines()

grid = [[x for x in line] for line in lines]
M, N = len(grid), len(grid[0])
START = next((0, i) for i in range(N) if grid[0][i] == '.')
END = next((M - 1, i) for i in range(N) if grid[M - 1][i] == '.')
DIRS = {
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
    '^': (-1, 0)
}

walls = set()
blizzard_cache = [set()]
for i in range(M):
    for j in range(N):
        if grid[i][j] == '.':
            continue 
        elif grid[i][j] == '#':
            walls.add((i, j))
        else:
            blizzard_cache[0].add((i, j, grid[i][j]))

def spawn(x: int, y: int, dir: str) -> tuple[int, int]:
    match dir:
        case '>':
            return (x, 0) if (x, 0) not in walls else (x, 1)
        case 'v':
            return (0, y) if (0, y) not in walls else (1, y)
        case '<':
            return (x, N - 1) if (x, N - 1) not in walls else (x, N - 2)
        case '^':
            return (M - 1, y) if (M - 1, y) not in walls else (M - 2, y)

def get_blizzard(minute: int) -> tuple[int, int]:    
    if minute == len(blizzard_cache):
        blizzard_cache.append(set())
        for x, y, dir in blizzard_cache[minute - 1]:
            dx, dy = DIRS[dir]
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= M or ny < 0 or ny >= N or (nx, ny) in walls:
                blizzard_cache[-1].add((*spawn(x, y, dir), dir))
            else:
                blizzard_cache[-1].add((nx, ny, dir))
    return set((x, y) for x, y, _ in blizzard_cache[minute])

def shortest_path(start: tuple[int, int], end: tuple[int, int]) -> int:
    q = deque([(*start, 0)])
    visited = set()
    while q:
        x, y, minutes = q.popleft()

        if (x, y) == end:
            return minutes

        blizzard = get_blizzard(minutes + 1)

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < M and 0 <= ny < N and (nx, ny) not in walls and (nx, ny) not in blizzard and (nx, ny, minutes + 1) not in visited:
                visited.add((nx, ny, minutes + 1))
                q.append((nx, ny, minutes + 1))
        
print(shortest_path(START, END))
