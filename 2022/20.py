from pathlib import Path
from collections import deque

here = Path(__file__).parent
lines = Path(here/"20.txt").read_text().splitlines()
numbers = [int(x) for x in lines]

def get_coords(rounds: int, decryption_key: int) -> int:
    positions = deque([(i, number) for i, number in enumerate(numbers)])
    for _ in range(rounds):
        for i, number in enumerate(numbers):
            idx = positions.index((i, number))  
            positions.remove((i, number))  
            positions.rotate(-(number * decryption_key))  
            positions.insert(idx, (i, number)) 

    final = [number for _, number in positions]
    idx_0 = final.index(0)
    return sum(final[(idx_0 + x) % len(final)] * decryption_key for x in [1000, 2000, 3000])

print(f"Part 1: {get_coords(1, 1)}")
print(f"Part 2: {get_coords(10, 811589153)}")
