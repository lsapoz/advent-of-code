from pathlib import Path
from dataclasses import dataclass
from functools import cache
from enum import Enum
from typing import Tuple
import re
import math

here = Path(__file__).parent
lines = Path(here/"19.txt").read_text().splitlines()

class Material(Enum):
    Ore = 0
    Clay = 1
    Obsidian = 2
    Geode = 3

# add two tuple of ints together by adding up their elements matched up by index
def add(a: Tuple[int], b: Tuple[int]):
    return tuple(map(lambda x, y: x + y, a, b))

# add two tuple of ints together by adding up their elements matched up by index
def subtract(a: Tuple[int], b: Tuple[int]):
    return add(a, (-x for x in b))

@dataclass
class Blueprint:
    id: int
    robot_ore_cost_ore: int
    robot_clay_cost_ore: int
    robot_obsidian_cost_ore: int 
    robot_obsidian_cost_clay: int
    robot_geode_cost_ore: int
    robot_geode_cost_obsidian: int

    # return how much of each material each robot costs
    def robot_cost(self, robot_type: Material) -> Tuple[int]:
        match robot_type:
            case Material.Ore:
                return (self.robot_ore_cost_ore, 0, 0, 0)
            case Material.Clay:
                return (self.robot_clay_cost_ore, 0, 0, 0)
            case Material.Obsidian:
                return (self.robot_obsidian_cost_ore, self.robot_obsidian_cost_clay, 0, 0)
            case Material.Geode:
                return (self.robot_geode_cost_ore, 0, self.robot_geode_cost_obsidian, 0)
        return (0, 0, 0, 0)

    # return the max we ever require of each element
    def max_required(self) -> Tuple[int]:
        return (
            max(self.robot_ore_cost_ore, self.robot_clay_cost_ore, self.robot_geode_cost_ore),
            self.robot_obsidian_cost_clay,
            self.robot_geode_cost_obsidian,
            float('inf')
        )
        
# given a set of materials and a cost to build, determine if we can build
def can_build(materials: Tuple[int], cost: Tuple[int]) -> bool:
    return all(x >= 0 for x in subtract(materials, cost))

# given a type of robot, the # of robots we already have, and the max amount we'll ever need of any material
# determine if we should bother trying to build this robot
def should_build(robot_type: Material, robots: Tuple[int], max_required: Tuple[int]):
    if robot_type is None:  # base case is to not build a robot
        return True
    return robots[robot_type.value] < max_required[robot_type.value]

@cache
def max_geodes_possible(minutes: int) -> int:
    # if there are X minutes left, the best we could do is 
    # make one geode robot per minute, each of which would produce X - 1 geodes, X - 2 geodes, and so on
    return sum(i - 1 for i in range(1, minutes + 1))

def get_max_geodes(blueprint: Blueprint, total_minutes: int) -> int:
    best = 0
    max_required = blueprint.max_required()  # store the max amount of every material we'll ever need during a turn

    @cache
    def simulate(materials: Tuple[int], robots: Tuple[int], minutes: int) -> int:
        nonlocal best  # update the best result we've found so far across all branches as we find them
        
        max_geodes = materials[Material.Geode.value]

        # if we're out of time, return how many geodes we have
        if minutes == 0:
            return max_geodes

        # with X minutes remaining, the max geodes we can build is:
        # the geodes we already have, 1 geode per minute for every geode robot we have
        # and a certain amount of geodges assuming we can build 1 more geode robot every minute
        # if that's less than the best result we've found so far, don't even bother
        if max_geodes + robots[Material.Geode.value] * minutes + max_geodes_possible(minutes) < best:
            return max_geodes
        
        # to get more cache hits, throw away any excess material we know we won't need
        # the max required of each resource * minutes remaining is how much we'd spend building the most expensive robot
        # the # of robots collecting each resource * minutes left to collect is how much we're already producing
        materials = tuple(min((max_required[i] * minutes) - (robots[i] * (minutes - 1)), x) for i, x in enumerate(materials))

        # figure out how much we're going to collect this minute after we begin our build phase
        collected = tuple(quantity for quantity in robots)

        # try to build each robot, starting with a geode robot and working our way down to building nothing
        for robot_type in list(reversed([*Material])) + [None]:
            cost = blueprint.robot_cost(robot_type)
            if can_build(materials, cost) and should_build(robot_type, robots, max_required):
                materials_after_build = subtract(materials, cost)
                materials_after_collection = add(materials_after_build, collected)
                robots_after_build = robots if robot_type is None else add(robots, tuple(1 if robot_type.value == i else 0 for i in range(len(Material))))

                max_geodes = max(max_geodes, simulate(materials_after_collection, robots_after_build, minutes - 1))
                best = max(best, max_geodes)
        return max_geodes    
    
    return simulate((0,0,0,0), (1,0,0,0), total_minutes)


blueprints = [Blueprint(*[int(x) for x in re.findall("\d{1,}", line)]) for line in lines]
print(f"Part 1: {sum(blueprint.id * get_max_geodes(blueprint, 24) for blueprint in blueprints)}")
print(f"Part 2: {math.prod(get_max_geodes(blueprints[i], 32) for i in range(min(len(blueprints), 3)))}")
