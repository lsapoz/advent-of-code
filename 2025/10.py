from pathlib import Path
from dataclasses import dataclass
from collections import deque
import re
import z3

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()


@dataclass
class Machine:
    lights: tuple[bool, ...]
    buttons: list[set[int]]
    joltages: list[int]


machines: list[Machine] = []
for line in lines:
    lights = tuple(c == "#" for c in re.search(r"\[([.#]+)\]", line).group(1))

    button_groups = re.findall(r"\(([^)]*)\)", line)
    buttons = [set([int(x) for x in group.split(",")]) for group in button_groups]

    joltages = [int(x) for x in re.search(r"\{([^}]*)\}", line).group(1).split(",")]

    machines.append(Machine(lights, buttons, joltages))


def configure_lights(machine: Machine):
    initial_state = (False,) * len(machine.lights)
    initial_button_ids = set(range(len(machine.buttons)))

    q = deque([(0, initial_state, initial_button_ids, i) for i in initial_button_ids])
    while q:
        num_presses, current_state, button_ids, button_idx = q.popleft()
        button = machine.buttons[button_idx]
        new_state = tuple(
            x if i not in button else not x for i, x in enumerate(current_state)
        )
        if new_state == machine.lights:
            return num_presses + 1
        button_ids_left = button_ids - {button_idx}
        q.extend(
            (num_presses + 1, new_state, button_ids_left, i) for i in button_ids_left
        )


def configure_joltages(machine: Machine):
    optimizer = z3.Optimize()

    # variables p0, p1, ...pi represent how many times the ith button is pressed
    presses = [z3.Int(f"p{i}") for i in range(len(machine.buttons))]

    # the jth counter's joltage will equal the sum of all presses that increment it
    # e.g if buttons 0, 1, and 3 increment the jth counter
    # and the jth counter has a target joltage of 3
    # we expect p0 + p1 + p3 = 3
    for j, target in enumerate(machine.joltages):
        press_sum = sum(
            presses[i] for i, button in enumerate(machine.buttons) if j in button
        )
        optimizer.add(press_sum == target)

    # buttons can only be pressed a positive number of times
    # and we want to minimize the total number of presses
    optimizer.add(*[press >= 0 for press in presses])
    optimizer.minimize(sum(presses))

    optimizer.check()
    model = optimizer.model()
    return sum(model[press].as_long() for press in presses)


print(f"Part 1: {sum(configure_lights(machine) for machine in machines)}")
print(f"Part 2: {sum(configure_joltages(machine) for machine in machines)}")
