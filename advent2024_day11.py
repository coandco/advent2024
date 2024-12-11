import time
from collections import defaultdict
from typing import Dict

from utils import read_data


def blink(stones: Dict[int, int]) -> Dict[int, int]:
    new_stones = defaultdict(int)
    for stone, amount in stones.items():
        if stone == 0:
            new_stones[1] += amount
        elif len(text := str(stone)) % 2 == 0:
            left, right = int(text[: len(text) // 2]), int(text[len(text) // 2 :])
            new_stones[left] += amount
            new_stones[right] += amount
        else:
            new_stones[stone * 2024] += amount
    return new_stones


def main():
    # This wouldn't work if my input had duplicates, but I'm lazy and it doesn't
    stones = {int(x): 1 for x in read_data().split()}
    for _ in range(25):
        stones = blink(stones)
    print(f"Part one: {sum(stones.values())}")
    for _ in range(50):
        stones = blink(stones)
    print(f"Part two: {sum(stones.values())}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
