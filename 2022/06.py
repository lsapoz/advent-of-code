from pathlib import Path
from collections import defaultdict

here = Path(__file__).parent
buffer = Path(here/"06.txt").read_text()

def get_marker_index(buffer, num_unique_chars):
    marker = defaultdict(int)
    for i in range(num_unique_chars):
        marker[buffer[i]] += 1
    if len(marker) == num_unique_chars:
        return num_unique_chars

    for i in range(num_unique_chars, len(buffer)):
        marker[buffer[i]] += 1
        marker[buffer[i-num_unique_chars]] -= 1
        if marker[buffer[i-num_unique_chars]] == 0:
            del marker[buffer[i-num_unique_chars]]
        if len(marker) == num_unique_chars:
            return i + 1

print(f"Part 1: {get_marker_index(buffer, 4)}")
print(f"Part 2: {get_marker_index(buffer, 14)}")
