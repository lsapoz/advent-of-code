from pathlib import Path

here = Path(__file__).parent
lines = Path(here/"23.txt").read_text().splitlines()

DIRS = {
    0: [(-1, 0), (-1, 1), (-1, -1)],  # N, NE, NW
    1: [(1, 0), (1, 1), (1, -1)],  # S, SE, SW
    2: [(0, -1), (-1, -1), (1, -1)],  # W, NW, SW
    3: [(0, 1), (-1, 1), (1, 1)]  # E, NE, SE
}
ADJACENT = set(point for points in DIRS.values() for point in points)

def parse_elves() -> list[tuple[int, int]]:
    elves = []
    for i, line in enumerate(lines):
        for j, cell in enumerate(line):
            if cell == '#':
                elves.append((i, j))
    return elves


def get_num_empty_tiles(elves: list[tuple[int, int]]) -> int:
    # after the rounds are complete, draw the bounding box and figure out how many empty tiles there are
    x_coords, y_coords = zip(*elves)
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    all_points = set()
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
                all_points.add((x, y))
    return len(all_points - set(elves))


def simulate(elves: list[tuple[int, int]], rounds: int = None) -> tuple[list[tuple[int, int]], int]:
    round = -1
    while round < rounds if rounds is not None else True:
        round += 1
        proposals: dict[tuple[int, int]: int] = {}  # map each proposed direction to the index of the elf proposing it
        moves = elves.copy()  # start off each elf assuming it doesn't move
        occupied = set(elves)

        for elf_idx, (x, y) in enumerate(elves):
            # if no other Elves are in the adjacent positions, do nothing during this round.
            if all((x + dx, y + dy) not in occupied for (dx, dy) in ADJACENT):
                continue

            # otherwise looks in each of four directions and propose moving in the first valid direction
            for dir_idx in range(round, round + len(DIRS)):
                dir_idx = dir_idx % len(DIRS)
                if all((x + dx, y + dy) not in occupied for (dx, dy) in DIRS[dir_idx]):
                    nx, ny = next((x + dx, y + dy) for (dx, dy) in DIRS[dir_idx])

                    # if no other elf has claimed this position, claim it ourselves
                    if (nx, ny) not in proposals:
                        proposals[(nx, ny)] = elf_idx
                        moves[elf_idx] = (nx, ny)
                    # otherwise, do nothing and void the other elf's move
                    else:
                        elf_idx_to_void = proposals[(nx, ny)]
                        moves[elf_idx_to_void] = elves[elf_idx_to_void]

                    # we've made our proposal, so we can skip checking the other directions
                    break

        if elves == moves:
            break
        elves = moves
    return elves, round + 1

elves, _ = simulate(parse_elves(), 10)
print(f"Part 1: {get_num_empty_tiles(elves)}")

_, num_rounds = simulate(parse_elves())
print(f"Part 2: {num_rounds}")
