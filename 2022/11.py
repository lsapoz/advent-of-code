from pathlib import Path
from typing import Callable, Dict, List, Tuple
from collections import deque
import operator

here = Path(__file__).parent
lines = Path(here/"11.txt").read_text().splitlines()

ops = {
    '+' : operator.add,
    '*' : operator.mul,
}

class Monkey:
    def __init__(self, items: List[int], 
                       operation: Callable[[int], int], 
                       test_divisor: int, 
                       throw_to: Dict[bool, int]):
        self.items = deque(items) 
        self.operation = operation 
        self.test_divisor = test_divisor
        self.throw_to = throw_to
        self.num_inspected = 0

    # take the first item and modify its worry level
    def inspect(self) -> None:
        self.items[0] = self.operation(self.items[0])
        self.num_inspected += 1

    # calm down the worry level of the first item
    def calm_down(self, divisor: int = None, modulus: int = None):
        if divisor:
            self.items[0] //= divisor
        if modulus:
            self.items[0] %= modulus

    # pop the first item off and return it & the monkey # it was thrown to
    def throw(self) -> Tuple[int, int]:
        item = self.items.popleft()
        test_result = (item % self.test_divisor == 0)
        return (item, self.throw_to[test_result])

    # catch an item and add it to the end of our item list
    def catch(self, item: int) -> None:
        self.items.append(item)


def parse_monkey(data: List[str]) -> Monkey:
    items = [int(x) for x in data[1].split(':')[1].split(',')]
    op_operator = data[2].split()[-2]
    op_term1 = data[2].split()[-3]
    op_term2 = data[2].split()[-1]
    test_divisor = int(data[3].split()[-1])
    throw_to = {
        True: int(data[4].split()[-1]),
        False: int(data[5].split()[-1])
    }
    return Monkey(items=items,
                  operation=lambda x: ops[op_operator](x if op_term1 == 'old' else int(op_term1), x if op_term2 == 'old' else int(op_term2)),
                  test_divisor=test_divisor,
                  throw_to=throw_to
    )

def init_monkeys() -> List[Monkey]:
    monkeys: List[Monkey] = []
    for i in range(0, len(lines), 7):
        monkeys.append(parse_monkey(lines[i:i + 7]))
    return monkeys

def simulate_monkeys(monkeys: List[Monkey], num_rounds: int, calming_divisor: int = None) -> int:
    test_divisors = set([monkey.test_divisor for monkey in monkeys])
    calming_modulus = 1
    for divisor in test_divisors:
        calming_modulus *= divisor
    
    for _ in range(num_rounds):
        for monkey in monkeys:
            while monkey.items:
                monkey.inspect()
                monkey.calm_down(calming_divisor, calming_modulus)
                item, thrown_to = monkey.throw()
                monkeys[thrown_to].catch(item)
    monkey_inspections = sorted((monkey.num_inspected for monkey in monkeys), reverse=True)
    return monkey_inspections[0] * monkey_inspections[1]


print(f"Part 1: {simulate_monkeys(init_monkeys(), 20, 3)}")
print(f"Part 2: {simulate_monkeys(init_monkeys(), 10000)}")
