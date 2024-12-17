import time
from functools import lru_cache
from typing import Optional, Set, Tuple

from utils import BaseCoord as Coord, read_grid
from utils import read_data

HEADINGS = {"N": Coord(y=-1, x=0), "E": Coord(y=0, x=1), "S": Coord(y=1, x=0), "W": Coord(y=0, x=-1)}
RIGHT_TURNS = {"N": "E", "E": "S", "S": "W", "W": "N"}


class Field:
    obstacles: Set[Coord]
    max_x: int
    max_y: int
    start: Coord

    def __init__(self, raw_field: str):
        self.obstacles = set()
        self.start = Coord(0, 0)
        pos = Coord(0, 0)
        for pos, char in read_grid(raw_field):
            if char == "#":
                self.obstacles.add(pos)
            elif char == "^":
                self.start = pos
        self.max_x, self.max_y = pos.x, pos.y


    def in_bounds(self, loc: Coord) -> bool:
        return 0 <= loc.x <= self.max_x and 0 <= loc.y <= self.max_y

    def traverse(self) -> Set[Coord]:
        heading = "N"
        curpos = self.start
        traversed_squares: Set[Coord] = set()
        while self.in_bounds(curpos):
            ahead = curpos + HEADINGS[heading]
            while ahead in self.obstacles:
                heading = RIGHT_TURNS[heading]
                ahead = curpos + HEADINGS[heading]
            traversed_squares.add(curpos)
            curpos = ahead
        return traversed_squares

    @lru_cache(maxsize=10000)
    def next_position(self, pos: Coord, heading: str, obstacle: Optional[Coord] = None) -> Optional[Coord]:
        obstacle = {obstacle} if obstacle else set()
        if heading == "N":
            obstacles_in_way = [x for x in (self.obstacles | obstacle) if x.x == pos.x and x.y < pos.y]
            if not obstacles_in_way:
                return None
            return max(obstacles_in_way, key=lambda x: x.y) + Coord(y=1, x=0)
        elif heading == "E":
            obstacles_in_way = [x for x in (self.obstacles | obstacle) if x.y == pos.y and x.x > pos.x]
            if not obstacles_in_way:
                return None
            return min(obstacles_in_way, key=lambda x: x.x) + Coord(y=0, x=-1)
        elif heading == "S":
            obstacles_in_way = [x for x in (self.obstacles | obstacle) if x.x == pos.x and x.y > pos.y]
            if not obstacles_in_way:
                return None
            return min(obstacles_in_way, key=lambda x: x.y) + Coord(y=-1, x=0)
        elif heading == "W":
            obstacles_in_way = [x for x in (self.obstacles | obstacle) if x.y == pos.y and x.x < pos.x]
            if not obstacles_in_way:
                return None
            return max(obstacles_in_way, key=lambda x: x.x) + Coord(y=0, x=1)

    def has_loop(self, extra_obstacle: Coord) -> bool:
        heading = "N"
        curpos = self.start
        seen: Set[Tuple[Coord, str]] = set()
        while True:
            if (curpos, heading) in seen:
                return True
            seen.add((curpos, heading))
            if curpos.x == extra_obstacle.x or curpos.y == extra_obstacle.y:
                # If we're in line with an obstacle, cache-bust it
                curpos = self.next_position(curpos, heading, extra_obstacle)
            else:
                # If we're not, we can pretend it doesn't exist for better cacheability
                curpos = self.next_position(curpos, heading)
            heading = RIGHT_TURNS[heading]
            if not curpos:
                return False

    def count_loop_obstacles(self, traversed_squares: Set[Coord]):
        valid_obstacle_locations = set()
        for new_obstacle in traversed_squares:
            if new_obstacle == self.start:
                continue
            if new_obstacle not in self.obstacles and self.has_loop(new_obstacle):
                valid_obstacle_locations.add(new_obstacle)
        return len(valid_obstacle_locations)


def main():
    field = Field(read_data())
    traversed_squares = field.traverse()
    print(f"Part one: {len(traversed_squares)}")
    print(f"Part two: {field.count_loop_obstacles(traversed_squares)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
