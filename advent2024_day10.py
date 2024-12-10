import time
from collections import defaultdict, deque
from typing import Deque, Dict, Set, Tuple

from utils import BaseCoord as Coord
from utils import read_data


class Map:
    topo: Dict[Coord, int]
    trailheads: Set[Coord]

    def __init__(self, raw: str):
        self.topo = defaultdict(lambda: 99999)
        self.trailheads = set()
        for y, line in enumerate(raw.splitlines()):
            for x, char in enumerate(line):
                loc = Coord(x=x, y=y)
                self.topo[loc] = int(char)
                if char == "0":
                    self.trailheads.add(loc)

    def score_trails(self, trailhead: Coord) -> Tuple[int, int]:
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
        return len(set(x[-1] for x in found_trails)), len(found_trails)


def main():
    topo_map = Map(read_data())
    scores = [topo_map.score_trails(x) for x in topo_map.trailheads]
    print(f"Part one: {sum(x[0] for x in scores)}")
    print(f"Part two: {sum(x[1] for x in scores)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
