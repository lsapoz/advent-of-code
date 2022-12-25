from pathlib import Path
from dataclasses import dataclass
from collections import deque

here = Path(__file__).parent
lines = Path(here/"21.txt").read_text().splitlines()

# return the result of a "result = x OP y" equation
OPERATIONS = {
    '+': lambda x, y: x + y,
    '*': lambda x, y: x * y,
    '-': lambda x, y: x - y,
    '/': lambda x, y: x // y
}

# return the x term of a "result = x OP y" equation
REVERSALS_X = {
    '+': lambda result, y: result - y,
    '*': lambda result, y: result // y,
    '-': lambda result, y: result + y,
    '/': lambda result, y: result * y,
}

# return the y term of a "result = x OP y" equation
REVERSALS_Y = {
    '+': lambda result, x: result - x,
    '*': lambda result, x: result // x,
    '-': lambda result, x: x - result,
    '/': lambda result, x: x // result
}

@dataclass 
class Equation():
    x: str
    op: str
    y: str

def parse_monkeys() -> tuple[dict[str, Equation], dict[str, int]]:
    equations: dict[str, Equation] = {}  # map of monkey name to equation
    numbers: dict[str, int] = {}  # map of monkey name to yelled number
    for line in lines:
        name, job = line.split(': ')
        job = job.split(' ')
        if len(job) == 1:
            numbers[name] = int(job[0])
        else:
            equations[name] = Equation(*job)
    return equations, numbers

def get_monkey_yell(equations: dict[str, Equation], numbers: dict[str, int]) -> int:
    def solve(eq: Equation):
        if numbers[eq.x] == None or numbers[eq.y] == None:
            return None 
        return OPERATIONS[eq.op](numbers[eq.x], numbers[eq.y])

    ROOT = 'root'
    while ROOT not in numbers:
        q = deque([ROOT])
        while q:
            monkey = q.popleft()
            eq = equations[monkey]
            if eq.x not in numbers:
                q.append(eq.x)
            if eq.y not in numbers:
                q.append(eq.y)
            if eq.x in numbers and eq.y in numbers:
                numbers[monkey] = solve(eq)
    return numbers[ROOT]

def get_human_yell(equations: dict[str, Equation], numbers: dict[str, int]):
    
    # given an equation and its result, and assuming one of the terms is known
    # return the unknown term and its value
    def reverse(eq: Equation, result: int):
        if numbers[eq.x] == None:
            return eq.x, REVERSALS_X[eq.op](result, numbers[eq.y])
        return eq.y, REVERSALS_Y[eq.op](result, numbers[eq.x])
    
    ROOT = 'root'
    HUMAN = 'humn'
    # set the value from the human "monkey" to None
    # find the root monkey yell - we'll resolve all the monkey numbers that we can
    # those terms that depend on 'humn' will be None as well
    numbers[HUMAN] = None
    get_monkey_yell(equations, numbers)

    # the root equation should now have one term with a value and one term without
    # find the term without, set the result of its equation to equal the other term's value, and work down to the human
    eq = equations[ROOT]
    monkey = eq.x if numbers[eq.x] == None else eq.y
    result = numbers[eq.x] if numbers[eq.x] != None else numbers[eq.y]
    while monkey != HUMAN:
        numbers[monkey] = result
        monkey, result = reverse(equations[monkey], result)
    return result


print(f"Part 1: {get_monkey_yell(*parse_monkeys())}")
print(f"Part 2: {get_human_yell(*parse_monkeys())}")
