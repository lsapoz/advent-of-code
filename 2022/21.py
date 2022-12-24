from pathlib import Path
from dataclasses import dataclass
from collections import deque
from typing import Union
import operator

here = Path(__file__).parent
lines = Path(here/"21.txt").read_text().splitlines()

OPS = {
    '+' : operator.add,
    '*' : operator.mul,
    '-' : operator.sub,
    '/' : operator.floordiv,
}

@dataclass 
class Equation():
    term1: Union[str, int]
    op: str
    term2: Union[str, int]

    # return True if both terms of the equation have been resolved to numbers
    def is_resolved(self) -> True:
        return isinstance(self.term1, int) and isinstance(self.term2, int)

    def result(self):
        return OPS[self.op](self.term1, self.term2)


operator_monkeys: dict[str, Equation] = {}  # map of monkey name to equation
number_monkeys: dict[str, int] = {}  # map of monkey name to yelled number
for line in lines:
    name, job = line.split(': ')
    job = job.split(' ')
    if len(job) == 1:
        number_monkeys[name] = int(job[0])
    else:
        operator_monkeys[name] = Equation(*job)


while "root" not in number_monkeys:
    q = deque(["root"])
    while q:
        monkey = q.popleft()
        eq = operator_monkeys[monkey]

        if isinstance(eq.term1, str):
            if eq.term1 in number_monkeys:
                eq.term1 = number_monkeys[eq.term1]
            else:
                q.append(eq.term1)

        if isinstance(eq.term2, str): 
            if eq.term2 in number_monkeys:
                eq.term2 = number_monkeys[eq.term2]
            else:
                q.append(eq.term2)

        if (eq.is_resolved()):
            number_monkeys[monkey] = eq.result()

print(number_monkeys["root"])
