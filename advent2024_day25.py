import time
from typing import FrozenSet, Iterable, List, Tuple

from utils import BaseCoord as Coord
from utils import read_data, read_grid

Grid = FrozenSet[Coord]


def parse(raw: str) -> Tuple[List[Grid], List[Grid]]:
    locks, keys = [], []
    for diagram in raw.split("\n\n"):
        cloud = set()
        for coord, char in read_grid(diagram):
            if char == "#":
                cloud.add(coord)
        if any(x.y == 0 for x in cloud):
            locks.append(frozenset(cloud))
        else:
            keys.append(frozenset(cloud))
    return locks, keys


def all_combinations(locks: List[Grid], keys: List[Grid]) -> Iterable[Tuple[Grid, Grid]]:
    for key in keys:
        for lock in locks:
            yield lock, key


def is_overlapping(lock: FrozenSet[Coord], key: FrozenSet[Coord]) -> bool:
    return len(lock & key) > 0


def main():
    locks, keys = parse(read_data())
    print(f"Part one: {sum(not is_overlapping(lock, key) for lock, key in all_combinations(locks, keys))}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
