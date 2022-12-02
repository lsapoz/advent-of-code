from pathlib import Path

here = Path(__file__).parent
lines = Path(here/"02.txt").read_text().splitlines()

# 0 = draw, 1 = win, 2 = loss
outcome_points = {0: 3, 1: 6, 2: 0} 

my_total_score = 0
for line in lines:
    moves = line.split()
    elf_move = ord(moves[0]) - ord('A') + 1
    my_move = ord(moves[1]) - ord('X') + 1
    outcome = (my_move - elf_move) % 3
    my_total_score += my_move + outcome_points[outcome]
print(f"My Total Score: {my_total_score}")
