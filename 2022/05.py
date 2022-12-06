from pathlib import Path
import re

here = Path(__file__).parent
lines = Path(here/"05.txt").read_text().splitlines()


# split data file into initial stack arrangement + movements
stack_data = []
movement_data = []
for i, line in enumerate(lines):
    if line:
        stack_data.append(line)
    else:
        movement_data = lines[i+1:]
        break

num_stacks = int(stack_data.pop().split()[-1])
initial_stacks = [[] for _ in range(num_stacks)]
while stack_data:
    line = stack_data.pop()
    line_idx = 1  # first character on a stack line is a '[', so skip it
    for i in range(num_stacks):
        letter = line[line_idx]
        if letter.strip():
            initial_stacks[i].append(letter)
        line_idx += 4  # after every letter we have '] [', skip straight to the next letter

# Part 1 - CrateMover 9000 - one crate moved at a time
stacks = [x[:] for x in initial_stacks]
for line in movement_data:
    num_crates, start, end = [int(x) for x in re.sub('\D', ' ', line).split()]
    for _ in range(num_crates):
        crate = stacks[start-1].pop()
        stacks[end-1].append(crate)
print(f"Part 1 - {''.join(stack[-1] for stack in stacks)}")

# Part 2 - CrateMover 9001 - multiple crates moved at a time
stacks = [x[:] for x in initial_stacks]
for line in movement_data:
    num_crates, start, end = [int(x) for x in re.sub('\D', ' ', line).split()]
    start_stack = stacks[start-1]
    split_point = len(start_stack) - num_crates
    stacks[start-1], crates_to_move = start_stack[:split_point], start_stack[split_point:]
    stacks[end-1].extend(crates_to_move)
print(f"Part 2 - {''.join(stack[-1] for stack in stacks)}")
