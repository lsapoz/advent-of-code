from pathlib import Path
import heapq

here = Path(__file__).parent
lines = Path(here/"01.txt").read_text().splitlines()

heap = []
current_elf_calories = 0
for line in lines:
    if not line:
        heapq.heappush(heap, -current_elf_calories)
        current_elf_calories = 0
    else:
        current_elf_calories += int(line)

max_calories = -heap[0]
print(f"Max Calories: {max_calories}")

top_elf_calories = sum(-heapq.heappop(heap) for _ in range(3))
print(f"Top 3 Elf Calories: {top_elf_calories}")
        