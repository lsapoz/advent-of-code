from pathlib import Path
from collections import deque

here = Path(__file__).parent
lines = Path(here/"12.txt").read_text().splitlines()

height_map = [[x for x in line] for line in lines]
M, N = len(height_map), len(height_map[0])

def shortest_descent(end: str, start: str):
    def valid_move(x, y, nx, ny) -> bool:
        if nx < 0 or nx >= M or ny < 0 or ny >= N or (nx, ny) in visited:
            return False
        a = height_map[x][y].replace('S', 'a').replace('E', 'z')
        b = height_map[nx][ny].replace('S', 'a').replace('E', 'z')
        return ord(a) - ord(b) <= 1
    
    q = deque([(i, j, 0) for i in range(M) for j in range(N) if height_map[i][j] == end])
    visited = set()
    while q:
        x, y, steps = q.popleft()

        if height_map[x][y] == start:
            return steps

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if valid_move(x, y, nx, ny):
                visited.add((nx, ny))
                q.append((nx, ny, steps + 1))

print(f"Part 1: {shortest_descent('E', 'S')}")
print(f"Part 2: {shortest_descent('E', 'a')}")
