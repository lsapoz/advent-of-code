from pathlib import Path
from functools import cache

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
devices = {line.split(":")[0]: line.split(":")[1].split() for line in lines}


@cache
def dfs(
    device: str,
    end: str,
    required: frozenset[str] = frozenset(),
):
    paths = 0

    if device == end:
        return 1 if not required else 0

    for output in devices[device]:
        paths += dfs(output, end, required - {device})

    return paths


print(f"Part 1: {dfs("you", "out")}")
print(f"Part 2: {dfs("svr", "out", frozenset(["dac", "fft"]))}")
