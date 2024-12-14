from collections import Counter
from math import prod
from typing import NamedTuple, Set, Tuple, List, FrozenSet, Dict

from utils import read_data, BaseCoord as Coord
import time
import re

DIGITS = re.compile(r'[+-]?\d+')


class Robot(NamedTuple):
    pos: Coord
    vel: Coord

    def pos_at(self, max_x: int, max_y: int, t: int) -> Coord:
        new_pos = self.pos + (self.vel * t)
        return Coord(x=new_pos.x % max_x, y=new_pos.y % max_y)

    @staticmethod
    def from_raw(raw: str) -> 'Robot':
        px, py, vx, vy = DIGITS.findall(raw)
        return Robot(pos=Coord(x=int(px), y=int(py)), vel=Coord(x=int(vx), y=int(vy)))


def sort_quadrants(field: List[Coord], max_x: int, max_y: int) -> Tuple[List[Coord], ...]:
    mid_x, mid_y = max_x//2, max_y//2
    nw = [x for x in field if 0 <= x.x < mid_x and 0 <= x.y < mid_y]
    ne = [x for x in field if mid_x < x.x <= max_x and 0 <= x.y < mid_y]
    sw = [x for x in field if 0 <= x.x < mid_x and mid_y < x.y <= max_y]
    se = [x for x in field if mid_x < x.x <= max_x and mid_y < x.y <= max_y]
    return nw, ne, sw, se

def has_tree(field: FrozenSet[Coord]) -> bool:
    by_column = Counter(x.x for x in field)
    biggest = [x[1] for x in by_column.most_common(3)]
    # Looking for symmetrical order and assuming that a tree will have vertical columns
    if biggest[0] == biggest[1] and biggest[0] - biggest[2] > 8:
        return True
    return False


def print_field(field: FrozenSet[Coord], max_x: int, max_y: int):
    for y in range(max_y):
        for x in range(max_x):
            loc = Coord(x=x, y=y)
            if loc in field:
                print("#", end='')
            else:
                print(".", end='')
        print('')


def main():
    robots = [Robot.from_raw(x) for x in read_data().splitlines()]
    at_100 = [x.pos_at(max_x=101, max_y=103, t=100) for x in robots]
    print(f"Part one: {prod(len(x) for x in sort_quadrants(at_100, max_x=101, max_y=103))}")
    t = 0
    while True:
        t += 1
        positions = frozenset(x.pos_at(max_x=101, max_y=103, t=t) for x in robots)
        if has_tree(positions):
            print_field(positions, max_x=101, max_y=103)
            print(f"Part two: {t}")
            break


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
