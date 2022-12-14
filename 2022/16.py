from pathlib import Path
from typing import Dict, List, Set
from dataclasses import dataclass
from collections import defaultdict, deque
import itertools
import re

here = Path(__file__).parent
lines = Path(here/"16.txt").read_text().splitlines()

START_VALVE = 'AA'

@dataclass
class Valve:
    name: str
    flow_rate: int
    tunnels: List[str]


# get mapping of valve name to valve dataclass for all valves
def parse() -> Dict[str, Valve]:
    valve_map: Dict[str, Valve] = {}  
    for line in lines:
        name, flow_rate, *tunnels = re.findall("[A-Z]{2}|\d{1,}", line)
        valve_map[name] = Valve(name, int(flow_rate), tunnels)
    return valve_map


# assemble a mapping of the shortest distance from every valve to every other valve
# ignore any valves with a flow_rate of 0 (except the start)
def map_valve_distances(valve_map: Dict[str, Valve]) -> Dict[str, Dict[str, int]]:
    def shortest_path(a: str, b: str) -> int:
        q = deque([(a, 0)])
        visited = set([a])
        while q:
            name, distance = q.popleft()
            if name == b:
                return distance

            for next_valve_name in valve_map[name].tunnels:
                if next_valve_name not in visited:
                    visited.add(next_valve_name)
                    q.append((next_valve_name, distance + 1))
    
    valve_distances: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for a in valve_map:
        if valve_map[a].flow_rate == 0 and a != START_VALVE:
            continue

        for b in valve_map:
            if (valve_map[b].flow_rate == 0 and b != START_VALVE) or b == a:
                continue
            if b in valve_distances and a in valve_distances[b]:
                valve_distances[a][b] = valve_distances[b][a]
            valve_distances[a][b] = shortest_path(a, b)

    return valve_distances


# for a set of valves and distances between those valves, determine the max steam that can be released
def get_max_steam(valve_map: Dict[str, Valve], valve_distances: Dict[str, Dict[str, int]], minutes: int, with_elephant: bool) -> int:
    
    # depth-first traversal of the tunnels
    # starting from the current_valve, with minutes remaining, steam already released, and some already open_valves
    def traverse(current_valve: str, minutes: int, steam: int, open_valves: Set[str]) -> int:
        # if all valves are open, we're done
        if len(open_valves) == len(valve_distances):
            return steam

        # otherwise, see how much more steam we can release by opening more valves
        max_steam = steam
        for nv, distance in valve_distances[current_valve].items():
            minutes_left = minutes - distance - 1  
            if nv not in open_valves and minutes_left > 0:
                open_valves.add(nv)

                total_steam = steam + (valve_map[nv].flow_rate * minutes_left)
                max_steam = max(max_steam, traverse(nv, minutes_left, total_steam, open_valves))

                open_valves.remove(nv)
        return max_steam

    if not with_elephant:
        return traverse(START_VALVE, minutes, 0, set([START_VALVE]))
    
    # if we have an elephant helping us, split the valves into every possible pair of two exclusive sets
    # figure out the max steam released if we each take the optimal path for every pair of exclusive sets
    max_steam = 0
    valves_to_open = set([v for v in valve_distances.keys() if v != START_VALVE])
    for r in range((len(valves_to_open) // 2 + 1)):
        for combination in itertools.combinations(valves_to_open, r):
            my_set = set(combination)
            elephant_set = valves_to_open - my_set
            max_steam = max(max_steam, traverse(START_VALVE, 26, 0, my_set) + traverse(START_VALVE, 26, 0, elephant_set))
    return max_steam


valve_map = parse()
valve_distances = map_valve_distances(valve_map)
print(f"Part 1: {get_max_steam(valve_map, valve_distances, 30, False)}")
print(f"Part 2: {get_max_steam(valve_map, valve_distances, 26, True)}")
