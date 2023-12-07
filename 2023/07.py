from pathlib import Path
from collections import Counter
import heapq

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()


mapping = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}


def get_type(hand: tuple[int, ...]):
    counts = tuple(count for _, count in Counter(hand).most_common())
    match counts:
        case (5,):
            return 6  # five of a kind
        case (4, 1):
            return 5  # four of a kind
        case (3, 2):
            return 4  # full house
        case (3, 1, 1):
            return 3  # three of a kind
        case (2, 2, 1):
            return 2  # two pair
        case (2, 1, 1, 1):
            return 1  # one pair
    return 0  # high card


ranked = []
for line in lines:
    hand, bid = line.split()
    hand = tuple(int(mapping.get(x, x)) for x in hand)
    heapq.heappush(ranked, ((get_type(hand), hand, int(bid))))  # (type, hand, bid)

winnings = 0
rank = 1
while ranked:
    winnings += rank * heapq.heappop(ranked)[-1]
    rank += 1
print(winnings)
