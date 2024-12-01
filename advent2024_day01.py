from collections import Counter

from utils import read_data
import time


def main():
    data = [line.split() for line in read_data().splitlines()]
    left, right = sorted([int(x[0]) for x in data]), sorted([int(x[1]) for x in data])
    print(f"Part one: {sum(abs(l - r) for l, r in zip(left, right))}")
    counts = Counter(right)
    print(f"Part two: {sum(item * counts[item] for item in left)}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
