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
                       test: Callable[[int], bool], 
                       throw_to: Dict[bool, int]):
        self.items = deque(items) 
        self.operation = operation 
        self.test = test
        self.throw_to = throw_to
        self.num_inspected = 0

    # take the first item and modify its worry level
    def inspect(self) -> None:
        self.items[0] = self.operation(self.items[0]) // 3 
        self.num_inspected += 1

    # pop the first item off and return it & the monkey # it was thrown to
    def throw(self) -> Tuple[int, int]:
        item = self.items.popleft()
        test_result = self.test(item)
        return (item, self.throw_to[test_result])

    # catch an item and add it to the end of our item list
    def catch(self, item: int) -> None:
        self.items.append(item)


def parse_monkey(lines: List[str]) -> Monkey:
    print(lines)
    items = [int(x) for x in lines[1].split(':')[1].split(',')]
    op_operator = lines[2].split()[-2]
    op_term1 = lines[2].split()[-3]
    op_term2 = lines[2].split()[-1]
    test_divisor = int(lines[3].split()[-1])
    throw_to = {
        True: int(lines[4].split()[-1]),
        False: int(lines[5].split()[-1])
    }
    return Monkey(items=items,
                  operation=lambda x: ops[op_operator](x if op_term1 == 'old' else int(op_term1), x if op_term2 == 'old' else int(op_term2)),
                  test=lambda x: x % test_divisor == 0,
                  throw_to=throw_to
    )

monkeys: List[Monkey] = []
for i in range(0, len(lines), 7):
    monkeys.append(parse_monkey(lines[i:i + 7]))

for _ in range(20):
    for monkey in monkeys:
        while monkey.items:
            monkey.inspect()
            item, thrown_to = monkey.throw()
            monkeys[thrown_to].catch(item)
monkey_inspections = sorted((monkey.num_inspected for monkey in monkeys), reverse=True)
print(f"Level of Monkey Business: {monkey_inspections[0] * monkey_inspections[1]}")
