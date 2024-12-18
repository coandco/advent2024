from collections import deque, defaultdict
from typing import List, Dict, Deque, Tuple, Iterable

from utils import read_data, BaseCoord as Coord
import time

DIRS = {"N": Coord(x=0, y=-1), "E": Coord(x=1, y=0), "S": Coord(x=0, y=1), "W": Coord(x=-1, y=0)}


class Memory:
    walls: List[Coord]
    max_x: int = 70
    max_y: int = 70
    start: Coord = Coord(0, 0)
    end: Coord = Coord(70, 70)

    def __init__(self, raw: str):
        self.walls = []
        for line in raw.splitlines():
            raw_x, raw_y = line.split(",")
            self.walls.append(Coord(x=int(raw_x), y=int(raw_y)))

    def in_bounds(self, loc: Coord) -> bool:
        return 0 <= loc.x <= self.max_x and 0 <= loc.y <= self.max_y

    def navigate(self, num_fallen: int = 1024) -> int:
        walls = set(self.walls[:num_fallen])
        min_distances: Dict[Coord, int] = defaultdict(lambda: 9999999)
        stack: Deque[Tuple[Coord, int]] = deque([(self.start, 0)])
        while stack:
            loc, score = stack.popleft()
            if score >= min_distances[loc]:
                continue
            min_distances[loc] = score
            for heading in DIRS:
                new_loc = loc + DIRS[heading]
                if self.in_bounds(new_loc) and new_loc not in walls:
                    stack.append((new_loc, score+1))
        return min_distances[self.end]


def main():
    memory = Memory(read_data())
    print(f"Part one: {memory.navigate(1024)}")
    for i in range(1025, len(memory.walls)):
        if memory.navigate(i) > 5000:
            print(f"Part two: {memory.walls[i-1].x},{memory.walls[i-i].y}")
            break


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
