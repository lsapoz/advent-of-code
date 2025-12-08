from pathlib import Path
from heapq import heappop, heappush
from math import dist, prod
from collections import defaultdict, Counter

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
boxes = [tuple(int(x) for x in line.split(",")) for line in lines]

heap = []
for i in range(len(boxes)):
    for j in range(i + 1, len(boxes)):
        b1, b2 = boxes[i], boxes[j]
        heappush(heap, (dist(b1, b2), b1, b2))

box_to_circuit = {}
circuit_to_boxes = defaultdict(set)
circuit_num = 1
for _ in range(1000):
    _, b1, b2 = heappop(heap)
    c1, c2 = box_to_circuit.get(b1), box_to_circuit.get(b2)

    # if both boxes are already in circuits, merge them (or do nothing if it's the same circuit)
    if c1 and c2:
        if c1 != c2:
            c2_boxes = circuit_to_boxes.pop(c2)
            circuit_to_boxes[c1].update(c2_boxes)
            for box in c2_boxes:
                box_to_circuit[box] = c1

    # if one of the boxes in a circuit, add the other to that circuit
    elif c1 or c2:
        c = c1 or c2
        circuit_to_boxes[c].update([b1, b2])
        box_to_circuit[b1], box_to_circuit[b2] = c, c

    # if neither box is in a circuit, add both to a new circuit
    else:
        c = circuit_num
        circuit_to_boxes[c].update([b1, b2])
        box_to_circuit[b1], box_to_circuit[b2] = c, c
        circuit_num += 1

counter = Counter()
for key, value in circuit_to_boxes.items():
    counter[key] = len(value)
print(f"Part 1: {prod(x[1] for x in counter.most_common(3))}")
