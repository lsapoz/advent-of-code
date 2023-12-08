from pathlib import Path
import re

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

dirs = [1 if x == "R" else 0 for x in lines[0]]
nodes = {}
for line in lines[2:]:
    parsed = re.findall("\\w+", line)
    nodes[parsed[0]] = parsed[1:]

curr, dest, steps = "AAA", "ZZZ", 0
while curr != dest:
    curr = nodes[curr][dirs[steps % len(dirs)]]
    steps += 1
print(steps)
