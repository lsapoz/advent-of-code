from pathlib import Path
from collections import deque

here = Path(__file__).parent
lines = Path(here/"20.txt").read_text().splitlines()

numbers = [int(x) for x in lines]
positions = deque([(i, number) for i, number in enumerate(numbers)])

for i, number in enumerate(numbers):
    idx = positions.index((i, number))  
    positions.remove((i, number))  
    positions.rotate(-number)  
    positions.insert(idx, (i, number)) 

final = [number for _, number in positions]
idx_0 = final.index(0)
print(sum(final[(idx_0 + x) % len(final)] for x in [1000, 2000, 3000]))
