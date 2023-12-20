from pathlib import Path
from collections import defaultdict, deque
import math

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()

types = {}  # name: type
outputs = {}  # name: [output module names]
inputs = defaultdict(list)  # name: [input module names]
flip_flops = {}  # name: on/off
conjunctions = {}  # name: {input: last received pulse}

to_track = []  # name of conjunctions to track
conjunction_cycles = {}  # cycle counts for when tracked conjunction turns low

for line in lines:
    module, destinations = line.split(" -> ")
    mod_type, name = (module[0], module[1:]) if module != "broadcaster" else (module, module)
    types[name] = mod_type
    outputs[name] = destinations.split(", ")
    for output in outputs[name]:
        inputs[output].append(name)

for name, mod_type in types.items():
    match mod_type:
        case "%":
            flip_flops[name] = False
        case "&":
            conjunctions[name] = {input: False for input in inputs[name]}


def process_pulse(origin: str, target: str, is_high: bool, push_num: int):
    match types.get(target, None):
        case "broadcaster":
            return [(target, output, is_high, push_num) for output in outputs[target]]
        case "%":
            if not is_high:
                flip_flops[target] = not flip_flops[target]
                return [(target, output, flip_flops[target], push_num) for output in outputs[target]]
        case "&":
            conjunctions[target][origin] = is_high
            all_high = all(conjunctions[target].values())
            if target in to_track and not all_high:
                conjunction_cycles[target] = push_num

            return [(target, output, not all_high, push_num) for output in outputs[target]]
    return []


def push_button(push_num: int):
    num_pulses = defaultdict(int)
    pulses = deque([("button", "broadcaster", False, push_num)])
    while pulses:
        origin, target, is_high, push_num = pulses.popleft()
        num_pulses[is_high] += 1
        pulses.extend(process_pulse(origin, target, is_high, push_num))
    return num_pulses


num_high, num_low = 0, 0
for i in range(1, 1001):
    num_pulses = push_button(i)
    num_high += num_pulses[True]
    num_low += num_pulses[False]
print(f"Part 1: {num_high * num_low}")

pushes = 1000
# rx is fed by conjunction module, which is fed by four more conjunctions
# track when those conjunctions all turn low
to_track = inputs[inputs["rx"][0]]
while True:
    pushes += 1
    push_button(pushes)
    if len(conjunction_cycles) == len(to_track):
        print(f"Part 2: {math.lcm(*conjunction_cycles.values())}")
        break
