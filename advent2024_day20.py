import time
from typing import Dict, Iterable, List, Set

from utils import CARDINAL_NEIGHBORS_2D as NEIGHBORS
from utils import BaseCoord as Coord
from utils import read_data, read_grid


class Racetrack:
    walls: Set[Coord]
    start: Coord
    end: Coord
    path: List[Coord]
    steps: Dict[Coord, int]

    def __init__(self, raw: str):
        self.walls = set()
        for coord, char in read_grid(raw):
            if char == "#":
                self.walls.add(coord)
            elif char == "S":
                self.start = coord
            elif char == "E":
                self.end = coord
        self.steps = {}
        self.path = []
        self.calc_steps_and_path()

    def calc_steps_and_path(self):
        pos = self.start
        prev = None
        i = 0
        while pos != self.end:
            self.steps[pos] = i
            self.path.append(pos)
            # This only works because there's only one path to go
            nextpos = next(x for x in pos.cardinal_neighbors() if x != prev and x not in self.walls)
            prev = pos
            pos = nextpos
            i += 1
        # Make sure we hit the end space as well
        self.steps[pos] = i

    def find_savings_p1(self, pos: Coord) -> Iterable[int]:
        for heading in NEIGHBORS:
            one_out = pos + heading
            two_out = one_out + heading
            if one_out in self.walls and two_out in self.steps:
                savings = self.steps[two_out] - (self.steps[pos] + 2)
                if savings > 0:
                    yield savings

    def find_savings_p2(self, pos: Coord, cheat_range: int = 2) -> Iterable[int]:
        reachable = [x for x in self.steps if 2 <= x.distance(pos) <= cheat_range]
        for dest in reachable:
            savings = self.steps[dest] - (self.steps[pos] + dest.distance(pos))
            if savings > 0:
                yield savings

    def all_savings_p1(self) -> Iterable[int]:
        for pos in self.path:
            yield from self.find_savings_p1(pos)

    def all_savings_p2(self, cheat_range: int = 20) -> Iterable[int]:
        for pos in self.path:
            yield from self.find_savings_p2(pos, cheat_range)


def main():
    racetrack = Racetrack(read_data())
    print(f"Part one: {sum(1 for x in racetrack.all_savings_p1() if x >= 100)}")
    print(f"Part two: {sum(1 for x in racetrack.all_savings_p2() if x >= 100)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
