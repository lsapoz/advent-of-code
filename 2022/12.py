from pathlib import Path
from collections import deque

here = Path(__file__).parent
lines = Path(here/"12.txt").read_text().splitlines()

height_map = [[x for x in line] for line in lines]
M, N = len(height_map), len(height_map[0])

S, E = None, None
for i in range(M):
    for j in range(N):
        if height_map[i][j] == 'S':
            S = (i, j)
            height_map[i][j] = 'a'
        elif height_map[i][j] == 'E':
            E = (i, j)
            height_map[i][j] = 'z'
        height_map[i][j] = ord(height_map[i][j]) - ord('a')

def get_shortest_path():
    q = deque([(S[0], S[1], 0)])
    visited = set()
    while q:
        x, y, steps = q.popleft()

        if (x, y) == E:
            return steps

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if nx >= 0 and nx < M and ny >= 0 and ny < N and (nx, ny) not in visited and height_map[nx][ny] - height_map[x][y] <= 1:
                visited.add((nx, ny))
                q.append((nx, ny, steps + 1))

print(f"Part 1: {get_shortest_path()}")
