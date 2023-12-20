from pathlib import Path
from collections import defaultdict, deque

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

types = {}  # name: type
outputs = {}  # name: [output module names]
inputs = defaultdict(list)  # name: [input module names]
flip_flops = {}  # name: on/off
conjunctions = {}  # name: {input: last received pulse}

for line in lines:
    module, destinations = line.split(" -> ")
    type, name = (module[0], module[1:]) if module != "broadcaster" else (module, module)
    types[name] = type
    outputs[name] = destinations.split(", ")
    for output in outputs[name]:
        inputs[output].append(name)

for name, type in types.items():
    match type:
        case "%":
            flip_flops[name] = False
        case "&":
            conjunctions[name] = {input: False for input in inputs[name]}


def process_pulse(origin: str, target: str, is_high: bool):
    match types.get(target, None):
        case "broadcaster":
            return [(target, output, is_high) for output in outputs[target]]
        case "%":
            if not is_high:
                flip_flops[target] = not flip_flops[target]
                return [(target, output, flip_flops[target]) for output in outputs[target]]
        case "&":
            conjunctions[target][origin] = is_high
            return [(target, output, not all(conjunctions[target].values())) for output in outputs[target]]
    return []


def push_button():
    num_pulses = defaultdict(int)
    pulses = deque([("button", "broadcaster", False)])
    while pulses:
        origin, target, is_high = pulses.popleft()
        num_pulses[is_high] += 1
        pulses.extend(process_pulse(origin, target, is_high))
    return num_pulses


num_high, num_low = 0, 0
for _ in range(1000):
    num_pulses = push_button()
    num_high += num_pulses[True]
    num_low += num_pulses[False]
print(f"Part 1: {num_high * num_low}")
