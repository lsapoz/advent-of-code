from pathlib import Path

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
devices = {line.split(":")[0]: line.split(":")[1].split() for line in lines}
START, END = "you", "out"


def dfs(device=START):
    paths = 0

    if device == END:
        return 1

    for output in devices[device]:
        paths += dfs(output)

    return paths


print(f"Part 1: {dfs()}")
