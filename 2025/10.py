from pathlib import Path
from dataclasses import dataclass
from collections import deque
import re

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


print(f"Part 1: {sum(configure_lights(machine) for machine in machines)}")
