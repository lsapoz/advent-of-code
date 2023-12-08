from pathlib import Path
import math
import re

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

dirs = [1 if x == "R" else 0 for x in lines[0]]
nodes = {}  # {node: [left, right]}
starts = []  # all nodes that end in A
for line in lines[2:]:
    parsed = re.findall("\\w+", line)
    nodes[parsed[0]] = parsed[1:]
    if parsed[0][-1] == "A":
        starts.append(parsed[0])

curr, dest, steps = "AAA", "ZZZ", 0
while curr != dest:
    curr = nodes[curr][dirs[steps % len(dirs)]]
    steps += 1
print(f"Part 1: {steps}")

# through testing, it seems that each node's cycle begins repeating after landing on a Z node
# so we just need to track the # of steps it takes for each node to land on a Z node the first time
z_steps = []
for start in starts:
    curr, steps = start, 0
    while True:
        curr = nodes[curr][dirs[steps % len(dirs)]]
        steps += 1
        if curr[-1] == "Z":
            z_steps.append(steps)
            break
print(f"Part 2: {math.lcm(*z_steps)}")
