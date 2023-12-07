from pathlib import Path
from collections import Counter
import heapq

lines = Path(__file__).resolve().with_suffix(".txt").read_text().splitlines()


regular_map = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
joker_map = {**regular_map, **{"J": 1}}


def parse_hand(hand: str, joker=False):
    mapping = joker_map if joker else regular_map
    return tuple(int(mapping.get(x, x)) for x in hand)


def get_type(hand: tuple[int, ...], joker=False):
    if joker and joker_map["J"] in hand and len(set(hand)) > 1:
        most_common_non_joker = Counter(x for x in hand if x != joker_map["J"]).most_common(1)[0][0]
        hand = tuple(most_common_non_joker if x == joker_map["J"] else x for x in hand)

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


def get_winnings(hands: list):
    winnings = 0
    rank = 1
    while hands:
        winnings += rank * heapq.heappop(hands)[-1]
        rank += 1
    return winnings


regular_hands = []
joker_hands = []
for line in lines:
    hand, bid = line.split()

    regular_hand = parse_hand(hand)
    heapq.heappush(regular_hands, ((get_type(regular_hand), regular_hand, int(bid))))

    joker_hand = parse_hand(hand, True)
    heapq.heappush(joker_hands, ((get_type(joker_hand, True), joker_hand, int(bid))))

print(f"Part 1: {get_winnings(regular_hands)}")
print(f"Part 2: {get_winnings(joker_hands)}")
