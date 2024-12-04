import time
from typing import List

from utils import read_data


def is_safe(levels: List[int]) -> bool:
    # We calculate the deltas first so we can operate directly on them
    deltas = [y - x for x, y in zip(levels[:-1], levels[1:])]
    # Grab the sign of the first element so we can compare it later
    first_sign = (deltas[0] >= 0)
    # Apply the rules: the difference has to be between 1 and 3 and the sign has to be constant
    return all(1 <= abs(x) <= 3 and (x >= 0) == first_sign for x in deltas)


def is_safe_with_damper(levels: List[int]):
    # Generator that produces variations a list with one element removed
    variations = ([x for i, x in enumerate(levels) if i != to_drop] for to_drop in range(len(levels)))
    # Using any() shortcuts if it finds a single one that works
    return any(is_safe(x) for x in variations)


def main():
    # Boring parse stuff, get a list of ints per line
    data = [[int(x) for x in line.split()] for line in read_data().splitlines()]
    print(f"Part one: {sum(is_safe(x) for x in data)}")
    print(f"Part two: {sum(is_safe_with_damper(x) for x in data)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
