from pathlib import Path

here = Path(__file__).parent
lines = Path(here/"08.txt").read_text().splitlines()

trees = [[int(x) for x in line] for line in lines]
M, N = len(trees), len(trees[0])
visible = set()

def traverse_row(from_left):
    for x in range(M):
        tallest = -1
        for y in (range(N) if from_left else reversed(range(N))):
            if trees[x][y] > tallest:
                visible.add((x,y))
                tallest = trees[x][y]

def traverse_column(from_top):
    for y in range(N):
        tallest = -1
        for x in (range(M) if from_top else reversed(range(M))):
            if trees[x][y] > tallest:
                visible.add((x,y))
                tallest = trees[x][y]

traverse_row(from_left=True)
traverse_row(from_left=False)
traverse_column(from_top=True)
traverse_column(from_top=False)

print(f"Trees Visible: {len(visible)}")

dirs = [(0,1), (0,-1), (1,0), (-1,0)]
def get_scenic_score(x, y):   
    scenic_score = 1
    for dx, dy in dirs:
        viewing_distance = 0
        nx, ny = x, y
        while True:
            nx += dx
            ny += dy
            if nx < 0 or nx >= M or ny < 0 or ny >= N:
                break
            viewing_distance += 1
            if trees[nx][ny] >= trees[x][y]:
                break
        scenic_score *= viewing_distance
    return scenic_score

max_scenic_score = 0
for x in range(M):
    for y in range(N):
        max_scenic_score = max(max_scenic_score, get_scenic_score(x, y))
print(f"Highest Scenic Score: {max_scenic_score}")
