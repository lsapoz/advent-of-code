from pathlib import Path

here = Path(__file__).parent
lines = Path(here/"04.txt").read_text().splitlines()

# is range b fully contained by range a
def is_fully_contained(a, b):
    a1, a2 = [int(x) for x in a.split('-')]
    b1, b2 = [int(x) for x in b.split('-')]
    return b1 >= a1 and b2 <= a2


num_fully_contained = 0
for line in lines:
    range1, range2 = line.split(',')
    if is_fully_contained(range1, range2) or is_fully_contained(range2, range1):
        num_fully_contained += 1
print(f"Num fully contained: {num_fully_contained}")
