from collections import Counter

from utils import read_data
import time


def main():
    data = [[int(x) for x in line.split()] for line in read_data().splitlines()]
    left, right = sorted([x[0] for x in data]), sorted([x[1] for x in data])
    print(f"Part one: {sum(abs(left[i] - right[i]) for i in range(len(left)))}")
    counts = Counter(right)
    print(f"Part two: {sum((item * counts[item]) for item in left)}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
