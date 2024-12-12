import time
from collections import defaultdict
from copy import deepcopy
from typing import Dict, Iterable, List, NamedTuple, Set

from utils import BaseCoord as Coord
from utils import read_data

DIRECTIONS = {"N": Coord(x=0, y=-1), "E": Coord(x=1, y=0), "S": Coord(x=0, y=1), "W": Coord(x=-1, y=0)}


class Region(NamedTuple):
    type: str
    area: Set[Coord]
    perimeter: Dict[str, Set[Coord]]

    def value(self):
        return len(self.area) * sum(len(x) for x in self.perimeter.values())

    @staticmethod
    def walls_in_dir(wallset: Set[Coord], startloc: Coord, heading: Coord) -> Set[Coord]:
        curloc = startloc
        contiguous = set()
        while curloc in wallset:
            contiguous.add(curloc)
            curloc = curloc + heading
        return contiguous

    def discounted_value(self):
        sections = deepcopy(self.perimeter)
        walls = defaultdict(list)
        for curdir in sections:
            while sections[curdir]:
                # Pick a point from the set at random
                startloc = next(iter(sections[curdir]))
                full_wall = set()
                # Extend out on both sides to find the extent of the wall
                if curdir in ("N", "S"):
                    full_wall |= self.walls_in_dir(sections[curdir], startloc, DIRECTIONS["W"])
                    full_wall |= self.walls_in_dir(sections[curdir], startloc, DIRECTIONS["E"])
                elif curdir in ("W", "E"):
                    full_wall |= self.walls_in_dir(sections[curdir], startloc, DIRECTIONS["N"])
                    full_wall |= self.walls_in_dir(sections[curdir], startloc, DIRECTIONS["S"])
                # Add it to our list of walls
                walls[curdir].append(full_wall)
                # Remove the points of the wall from the set
                sections[curdir] -= full_wall
        num_walls = sum(len(x) for x in walls.values())
        return len(self.area) * num_walls


class Farm:
    raw_map: Dict[Coord, str]
    regions: Dict[str, List[Region]]
    max_x: int
    max_y: int

    def __init__(self, raw: str):
        self.regions = defaultdict(list)
        self.raw_map = {}
        x = y = 0
        for y, line in enumerate(raw.splitlines()):
            for x, char in enumerate(line):
                self.raw_map[Coord(x=x, y=y)] = char
        self.max_x, self.max_y = x, y
        self.find_regions()

    def all_regions(self) -> Iterable[Region]:
        for region_list in self.regions.values():
            yield from region_list

    def find_regions(self):
        # Possible starts of regions we haven't explored yet
        seeds: Set[Coord] = {Coord(0, 0)}
        while seeds:
            region_start = seeds.pop()
            start_type = self.raw_map[region_start]
            region = Region(type=start_type, area=set(), perimeter=defaultdict(set))
            self.regions[start_type].append(region)
            to_check = {region_start}
            while to_check:
                curloc = to_check.pop()
                region.area.add(curloc)
                # It's probable we have multiple seeds in a single region,
                # so this makes sure we don't double-count regions
                seeds.discard(curloc)
                for curdir in DIRECTIONS:
                    neighbor = curloc + DIRECTIONS[curdir]
                    if neighbor in region.area:
                        continue
                    neighbor_type = self.raw_map.get(neighbor)
                    if neighbor_type is None:  # out of bounds
                        # Add the point to the set of (e.g.) "coords with north walls"
                        region.perimeter[curdir].add(curloc)
                        continue
                    elif neighbor_type != region.type:
                        region.perimeter[curdir].add(curloc)
                        # Only add a point to our seeds if it's not already part of a region of that type
                        if neighbor not in set().union(*(r.area for r in self.regions[neighbor_type])):
                            seeds.add(neighbor)
                        continue
                    else:  # Part of the existing region
                        to_check.add(neighbor)


def main():
    farm = Farm(read_data())
    print(f"Part one: {sum(x.value() for x in farm.all_regions())}")
    print(f"Part two: {sum(x.discounted_value() for x in farm.all_regions())}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
