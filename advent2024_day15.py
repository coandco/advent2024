import time
from typing import Optional, Set, Tuple

from utils import BaseCoord as Coord
from utils import read_data

DIRS = {"^": Coord(x=0, y=-1), ">": Coord(x=1, y=0), "v": Coord(x=0, y=1), "<": Coord(x=-1, y=0)}


class Warehouse:
    walls: Set[Coord]
    boxes: Set[Coord]
    start: Coord

    def __init__(self, raw_map: str):
        self.walls = set()
        self.boxes = set()
        self.load_map(raw_map)

    def load_map(self, raw_map: str):
        for y, line in enumerate(raw_map.splitlines()):
            for x, char in enumerate(line):
                pos = Coord(x=x, y=y)
                if char == "#":
                    self.walls.add(pos)
                elif char == "O":
                    self.boxes.add(pos)
                elif char == "@":
                    self.start = pos

    def boxes_in_way(self, pos: Coord, heading: str) -> Tuple[Set[Coord], int]:
        boxes_in_way = set()
        nextpos = pos + DIRS[heading]
        while nextpos in self.boxes:
            boxes_in_way.add(nextpos)
            nextpos = nextpos + DIRS[heading]
        if nextpos in self.walls:
            return boxes_in_way, True
        return boxes_in_way, False

    def move(self, curpos: Coord, heading: str) -> Coord:
        boxes_in_way, blocked = self.boxes_in_way(curpos, heading)
        if blocked:
            return curpos
        self.boxes -= boxes_in_way
        self.boxes |= {x + DIRS[heading] for x in boxes_in_way}
        return curpos + DIRS[heading]

    def print(self, curpos: Optional[Coord] = None):
        max_x, max_y = max(x.x for x in self.walls), max(x.y for x in self.walls)
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                pos = Coord(x=x, y=y)
                if pos == curpos:
                    print("@", end="")
                elif pos in self.walls:
                    print("#", end="")
                elif pos in self.boxes:
                    print("O", end="")
                else:
                    print(".", end="")
            print("")

    def handle_movement(self, moveset: str, debug: bool = False) -> int:
        curpos = self.start
        for move in moveset:
            curpos = self.move(curpos, move)
            if debug:
                self.print(curpos)
        return sum(x.x + (100 * x.y) for x in self.boxes)


class FatWarehouse(Warehouse):
    def load_map(self, raw_map: str):
        for y, line in enumerate(raw_map.splitlines()):
            for x, char in enumerate(line):
                pos = Coord(x=2 * x, y=y)
                doubled_pos = Coord(x=2 * x + 1, y=y)
                if char == "#":
                    self.walls.update({pos, doubled_pos})
                elif char == "O":
                    self.boxes.add(pos)
                elif char == "@":
                    self.start = pos

    def print(self, curpos: Optional[Coord] = None):
        max_x, max_y = max(x.x for x in self.walls), max(x.y for x in self.walls)
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                pos = Coord(x=x, y=y)
                if pos == curpos:
                    print("@", end="")
                elif pos in self.walls:
                    print("#", end="")
                elif pos in self.boxes:
                    print("[", end="")
                elif pos + DIRS["<"] in self.boxes:
                    print("]", end="")
                else:
                    print(".", end="")
            print("")

    def boxes_in_way(self, pos: Coord, heading: str) -> Tuple[Set[Coord], int]:
        boxes_in_way = set()
        blocked = False
        nextpos = pos + DIRS[heading]
        if heading == "<":
            nextpos = nextpos + DIRS[heading]
            while nextpos in self.boxes:
                boxes_in_way.add(nextpos)
                nextpos = nextpos + (DIRS[heading] * 2)
            nextpos = nextpos - DIRS[heading]
            if nextpos in self.walls:
                blocked = True
        elif heading == ">":
            while nextpos in self.boxes:
                boxes_in_way.add(nextpos)
                nextpos = nextpos + (DIRS[heading] * 2)
            if nextpos in self.walls:
                blocked = True
        elif heading in ("^", "v"):
            positions_to_check = [nextpos, nextpos + DIRS["<"]]
            while positions_to_check:
                to_check = positions_to_check.pop()
                if to_check in self.boxes:
                    boxes_in_way.add(to_check)
                    next_in_dir = to_check + DIRS[heading]
                    positions_to_check.extend([next_in_dir + DIRS["<"], next_in_dir, next_in_dir + DIRS[">"]])
            # Now that we have a set of boxes in the way, we need to check for blockage
            for box in boxes_in_way:
                if any(x + DIRS[heading] in self.walls for x in (box, box + DIRS[">"])):
                    blocked = True
        if nextpos in self.walls:
            blocked = True
        return boxes_in_way, blocked


def main():
    layout, moveset = read_data().split("\n\n")
    warehouse = Warehouse(layout)
    moveset = moveset.replace("\n", "")
    print(f"Part one: {warehouse.handle_movement(moveset)}")
    fat_warehouse = FatWarehouse(layout)
    print(f"Part two: {fat_warehouse.handle_movement(moveset)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
