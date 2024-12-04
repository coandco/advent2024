import time
from collections import Counter

from utils import read_data


def main():
    # Step one: parse input into a list of paired strings
    data = [line.split() for line in read_data().splitlines()]
    # Step two: Parse each string to an int, put it in its proper column, then sort the columns
    left, right = sorted(int(x[0]) for x in data), sorted(int(x[1]) for x in data)
    # Step three: calculate the absolute distance between each left/right pair and add them up
    print(f"Part one: {sum(abs(l - r) for l, r in zip(left, right))}")
    # Step four: Count how many times each number appears in the right column
    counts = Counter(right)
    # Step five: Multiply each item in the left-hand list by its count on the right and add them up
    print(f"Part two: {sum(item * counts[item] for item in left)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
