from pathlib import Path

here = Path(__file__).parent
lines = Path(here/"02.txt").read_text().splitlines()

# 0 = draw, 1 = win, 2 = loss
outcome_points = {0: 3, 1: 6, 2: 0} 

# Part 1
# A = X = Rock = 1 point
# B = Y = Paper = 2 points
# C = Z = Scissors = 3 points
my_total_score = 0
for line in lines:
    moves = line.split()
    elf_move = ord(moves[0]) - ord('A') + 1
    my_move = ord(moves[1]) - ord('X') + 1
    outcome = (my_move - elf_move) % 3
    my_total_score += my_move + outcome_points[outcome]
print(f"Part 1 Score: {my_total_score}")

# Part 2
# X = Lose
# Y = Draw
# Z = Win

# Map letters to the numbers we originally associated with each outcome
outcome_map = {'X': 2, 'Y': 0, 'Z': 1}

my_total_score = 0
for line in lines:
    split_line = line.split()
    elf_move = ord(split_line[0]) - ord('A') + 1
    outcome = outcome_map[split_line[1]]
    my_move = elf_move + outcome 
    my_move = my_move % 3 if my_move > 3 else my_move
    my_total_score += my_move + outcome_points[outcome]
print(f"Part 2 Score: {my_total_score}")
