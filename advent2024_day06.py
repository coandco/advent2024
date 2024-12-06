from collections import deque, defaultdict
from typing import Dict, Set, Optional, Tuple


from utils import read_data, BaseCoord as Coord
import time

HEADINGS = {"N": Coord(y=-1, x=0), "E": Coord(y=0, x=1), "S": Coord(y=1, x=0), "W": Coord(y=0, x=-1)}
RIGHT_TURNS = {"N": "E", "E": "S", "S": "W", "W": "N"}


class Field:
    obstacles: Set[Coord]
    max_x: int
    max_y: int
    start: Coord

    def __init__(self, raw_field: str):
        obstacles = set()
        self.start = None
        x = y = 0
        for y, line in enumerate(raw_field.splitlines()):
            for x, char in enumerate(line):
                if char == "#":
                    obstacles.add(Coord(x=x, y=y))
                elif char == "^":
                    self.start = Coord(x=x, y=y)
        self.obstacles = obstacles
        self.max_x, self.max_y = x, y

    def in_bounds(self, loc: Coord) -> bool:
        return 0 <= loc.x <= self.max_x and 0 <= loc.y <= self.max_y

    def traverse(self) -> Optional[int]:
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
        return len(traversed_squares)

    def next_position(self, obstacles: Set[Coord], pos: Coord, heading: str) -> Optional[Coord]:
        if heading == 'N':
            obstacles_in_way = [x for x in obstacles if x.x == pos.x and x.y < pos.y]
            if not obstacles_in_way:
                return None
            return max(obstacles_in_way, key=lambda x: x.y) + Coord(y=1, x=0)
        elif heading == 'E':
            obstacles_in_way = [x for x in obstacles if x.y == pos.y and x.x > pos.x]
            if not obstacles_in_way:
                return None
            return min(obstacles_in_way, key=lambda x: x.x) + Coord(y=0, x=-1)
        elif heading == 'S':
            obstacles_in_way = [x for x in obstacles if x.x == pos.x and x.y > pos.y]
            if not obstacles_in_way:
                return None
            return min(obstacles_in_way, key=lambda x: x.y) + Coord(y=-1, x=0)
        elif heading == 'W':
            obstacles_in_way = [x for x in obstacles if x.y == pos.y and x.x < pos.x]
            if not obstacles_in_way:
                return None
            return max(obstacles_in_way, key=lambda x: x.x) + Coord(y=0, x=1)

    def has_loop(self, extra_obstacle: Coord) -> bool:
        heading = "N"
        curpos = self.start
        history = deque(maxlen=1000)
        obstacles = self.obstacles | {extra_obstacle}
        seen: Set[Tuple[Coord, str]] = set()
        while True:
            history.append(curpos)
            if (curpos, heading) in seen:
                return True
            seen.add((curpos, heading))
            curpos = self.next_position(obstacles, curpos, heading)
            heading = RIGHT_TURNS[heading]
            if not curpos:
                return False


    def count_loop_obstacles(self):
        valid_obstacle_locations = set()
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                new_obstacle = Coord(x=x, y=y)
                if new_obstacle == self.start:
                    continue
                if new_obstacle not in self.obstacles and self.has_loop(new_obstacle):
                    valid_obstacle_locations.add(new_obstacle)
        return len(valid_obstacle_locations)


def main():
    field = Field(read_data())
    print(f"Part one: {field.traverse()}")
    print(f"Part two: {field.count_loop_obstacles()}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
