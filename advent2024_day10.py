import time
from collections import defaultdict, deque
from typing import Deque, Dict, Set, Tuple

from utils import BaseCoord as Coord, read_grid
from utils import read_data


class Map:
    topo: Dict[Coord, int]
    trailheads: Set[Coord]

    def __init__(self, raw: str):
        self.topo = defaultdict(lambda: 99999)
        self.trailheads = set()
        for loc, char in read_grid(raw):
            self.topo[loc] = int(char)
            if char == "0":
                self.trailheads.add(loc)

    def find_trails(self, trailhead: Coord) -> Set[Tuple[Coord, ...]]:
        found_trails = set()
        stack: Deque[Tuple[Coord, ...]] = deque([(trailhead,)])
        while stack:
            trail = stack.pop()
            if self.topo[trail[-1]] == 9:
                found_trails.add(trail)
                continue
            for step in trail[-1].cardinal_neighbors():
                if self.topo[step] == self.topo[trail[-1]] + 1:
                    stack.append(trail + (step,))
        return found_trails


def main():
    topo_map = Map(read_data())
    trails = [topo_map.find_trails(x) for x in topo_map.trailheads]
    # Deduplicate peaks for part one
    print(f"Part one: {sum(len(set(route[-1] for route in trail)) for trail in trails)}")
    print(f"Part two: {sum(len(x) for x in trails)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
