from pathlib import Path

steps = Path(__file__).resolve().with_suffix(".txt").read_text().replace("\n", "").split(",")


def HASH(s: str):
    val = 0
    for char in s:
        val += ord(char)
        val *= 17
        val %= 256
    return val


print(sum(HASH(step) for step in steps))
