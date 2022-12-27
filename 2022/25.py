from pathlib import Path
import functools

here = Path(__file__).parent
lines = Path(here/"25.txt").read_text().splitlines()

SYMBOL_TO_NUM = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}
NUM_TO_SYMBOL = {v: k for k, v in SYMBOL_TO_NUM.items()}

def to_decimal(snafu: str) -> int:
    return sum((5 ** i) * SYMBOL_TO_NUM[symbol] for i, symbol in enumerate(reversed(snafu)))

def add_snafu(a: str, b: str) -> str:
    a, b = list(a), list(b)
    ans, carry = [], 0
    while a or b:
        d1 = SYMBOL_TO_NUM[a.pop()] if a else 0
        d2 = SYMBOL_TO_NUM[b.pop()] if b else 0
        total, carry = carry + d1 + d2, 0
        while total >= 3:
            carry += 1
            total -= 5
        while total <= -3:
            carry -= 1
            total += 5
        ans += NUM_TO_SYMBOL[total]
    if carry:
        ans += NUM_TO_SYMBOL[carry]
    return ''.join(reversed(ans))

snafu_total = functools.reduce(lambda a, b: add_snafu(a, b), lines)
print(f"SNAFU: {snafu_total}")
print(f"Decimal: {to_decimal(snafu_total)}")
