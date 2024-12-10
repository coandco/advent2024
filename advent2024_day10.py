import time
from collections import defaultdict, deque
from typing import Deque, Dict, Set, Tuple

from utils import BaseCoord as Coord
from utils import read_data


class Map:
    topo: Dict[Coord, int]
    trailheads: Set[Coord]
    peaks: Set[Coord]
    max_x: int
    max_y: int

    def __init__(self, raw: str):
        self.topo = defaultdict(lambda: 99999)
        self.trailheads = set()
        self.peaks = set()
        x = y = 0
        for y, line in enumerate(raw.splitlines()):
            for x, char in enumerate(line):
                loc = Coord(x=x, y=y)
                self.topo[loc] = int(char)
                if char == "0":
                    self.trailheads.add(loc)
                elif char == "9":
                    self.peaks.add(loc)
        self.max_x, self.max_y = x, y

    def score_trailhead(self, trailhead: Coord) -> int:
        found_peaks = set()
        stack: Deque[Coord] = deque([trailhead])
        while stack:
            cur = stack.pop()
            if self.topo[cur] == 9:
                found_peaks.add(cur)
                continue
            for step in cur.cardinal_neighbors():
                if self.topo[step] == self.topo[cur] + 1:
                    stack.append(step)
        return len(found_peaks)

    def score_trails(self, trailhead: Coord) -> int:
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
        return len(found_trails)


def main():
    topo_map = Map(read_data())
    print(f"Part one: {sum(topo_map.score_trailhead(x) for x in topo_map.trailheads)}")
    print(f"Part two: {sum(topo_map.score_trails(x) for x in topo_map.trailheads)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
