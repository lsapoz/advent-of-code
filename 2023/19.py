from pathlib import Path
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
print(total)
