from pathlib import Path
import math
import re

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()
workflow_lines, rating_lines = lines[: lines.index("")], lines[lines.index("") + 1 :]

workflows: dict[str, dict[str, str]] = {}
for wf in workflow_lines:
    name, rule_defs = wf[:-1].split("{")
    workflows[name] = {}
    for rd in rule_defs.split(","):
        rd = rd.split(":")
        if len(rd) == 2:
            condition, dest = rd
        else:
            condition, dest = "True", rd[0]
        workflows[name][condition] = dest

ratings = [tuple(int(x) for x in re.findall("\d+", rt)) for rt in rating_lines]

q = [("in", r) for r in ratings]
total = 0
while q:
    workflow_name, rating = q.pop()
    workflow = workflows[workflow_name]
    x, m, a, s = rating
    for condition, dest in workflow.items():
        if eval(condition):
            match dest:
                case "A":
                    total += sum([x, m, a, s])
                case "R":
                    pass
                case _:
                    q.append((dest, rating))
            break
print(f"Part 1: {total}")


def split_range(rating: tuple[range, range, range, range], condition: str):
    if condition == "True":
        return (rating, None)

    category = condition[0]
    expr = condition[1]
    val = int(condition[2:])
    if expr == ">":
        val += 1

    left, right = list(rating), list(rating)
    idx = "xmas".index(category)
    left[idx] = range(left[idx][0], val)
    right[idx] = range(val, right[idx][-1] + 1)

    l, r = tuple(left), tuple(right)
    return (l, r) if expr == "<" else (r, l)


total = 0
q = [("in", tuple(range(1, 4001) for _ in range(4)))]
while q:
    workflow_name, rating = q.pop()
    workflow = workflows[workflow_name]
    for condition, dest in workflow.items():
        passing, failing = split_range(rating, condition)
        match dest:
            case "A":
                total += math.prod(len(r) for r in passing)
            case "R":
                pass
            case _:
                q.append((dest, passing))
        rating = failing
print(f"Part 2: {total}")
