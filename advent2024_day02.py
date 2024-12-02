import time
from math import copysign
from typing import List

from utils import read_data


def is_safe(levels: List[int]) -> bool:
    deltas = [y - x for x, y in zip(levels[:-1], levels[1:])]
    first_sign = copysign(1, deltas[0])
    return all(1 <= abs(x) <= 3 and copysign(1, x) == first_sign for x in deltas)


def is_safe_with_damper(levels: List[int]):
    variations = [[x for i, x in enumerate(levels) if i != to_drop] for to_drop in range(len(levels))]
    return any(is_safe(x) for x in variations)


def main():
    data = [[int(x) for x in line.split()] for line in read_data().splitlines()]
    print(f"Part one: {sum(is_safe(x) for x in data)}")
    print(f"Part two: {sum(is_safe_with_damper(x) for x in data)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
