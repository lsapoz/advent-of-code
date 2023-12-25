from pathlib import Path
from random import choice
from itertools import pairwise
from collections import defaultdict, deque, Counter

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

edges = defaultdict(list)
connections = []
for line in lines:
    nodes = line.replace(":", "").split()
    node, adjacent = nodes[0], nodes[1:]
    for a in adjacent:
        edges[node].append(a)
        edges[a].append(node)
        connections.append(tuple(sorted([node, a])))


def explore(start: str, disconnected: tuple[tuple[str, str]]):
    q = deque([start])
    visited = set([start])
    while q:
        node = q.popleft()
        for adjacent in edges[node]:
            if adjacent not in visited and tuple(sorted([node, adjacent])) not in disconnected:
                visited.add(adjacent)
                q.append(adjacent)
    return len(visited)


def get_path(start: str, end: str):
    q = deque([[start]])
    visited = set([start])
    while q:
        path = q.popleft()
        node = path[-1]
        if node == end:
            return path
        for adjacent in edges[node]:
            if adjacent not in visited:
                visited.add(adjacent)
                q.append([*path, adjacent])


# find which edges we cross the most when pathfinding between two random nodes
counter = Counter()
nodes = list(edges.keys())
for i in range(1000):
    start, end = choice(nodes), choice(nodes)
    path = get_path(start, end)
    for adjacents in pairwise(path):
        counter[tuple(sorted(adjacents))] += 1

# disconnect the 3 most traveled paths, find the size of the groups
start_node = next(iter(edges))
total_nodes = len(edges)
group_size = explore(start_node, [k for k, _ in counter.most_common(3)])
print(group_size * (total_nodes - group_size))
