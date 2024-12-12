import time
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Set

from utils import BaseCoord as Coord
from utils import read_data


@dataclass
class Region:
    type: str
    area: Set[Coord]
    perimeter: Dict[Coord, int]

    def value(self):
        return len(self.area) * sum(self.perimeter.values())

    def discounted_value(self):
        pass


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
        seeds: Set[Coord] = {Coord(0, 0)}
        while seeds:
            region_start = seeds.pop()
            start_type = self.raw_map[region_start]
            region = Region(type=start_type, area=set(), perimeter=defaultdict(int))
            self.regions[start_type].append(region)
            to_check = {region_start}
            while to_check:
                curloc = to_check.pop()
                region.area.add(curloc)
                seeds.discard(curloc)
                for neighbor in (x for x in curloc.cardinal_neighbors() if x not in region.area):
                    neighbor_type = self.raw_map.get(neighbor)
                    if neighbor_type is None:  # out of bounds
                        region.perimeter[neighbor] += 1
                        continue
                    elif neighbor_type != region.type:
                        region.perimeter[neighbor] += 1
                        if neighbor not in set().union(*(r.area for r in self.regions[neighbor_type])):
                            seeds.add(neighbor)
                        continue
                    else:  # Part of the existing region
                        to_check.add(neighbor)


def main():
    farm = Farm(read_data())
    farm.find_regions()
    print(f"Part one: {sum(x.value() for x in farm.all_regions())}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
