from collections import Counter

from utils import read_data
import time


def main():
    left, right = [], []
    for line in read_data().splitlines():
        first, second = line.split()
        left.append(int(first))
        right.append(int(second))
    left = sorted(left)
    right = sorted(right)
    distances = []
    for i in range(len(left)):
        distances.append(abs(left[i] - right[i]))
    print(f"Part one: {sum(distances)}")
    counts = Counter(right)
    similarities = []
    for item in left:
        similarities.append(item * counts[item])
    print(f"Part two: {sum(similarities)}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
