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
stacks = [[] for _ in range(num_stacks)]
while stack_data:
    line = stack_data.pop()
    line_idx = 1  # first character on a stack line is a '[', so skip it
    for i in range(num_stacks):
        letter = line[line_idx]
        if letter.strip():
            stacks[i].append(letter)
        line_idx += 4  # after every letter we have '] [', skip straight to the next letter

for line in movement_data:
    num_crates, start, end = [int(x) for x in re.sub('\D', ' ', line).split()]
    for _ in range(num_crates):
        crate = stacks[start-1].pop()
        stacks[end-1].append(crate)

top_seqeuence = ''
for stack in stacks:
    top_seqeuence += stack[-1]
print(top_seqeuence)
