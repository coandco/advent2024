import time
from collections import defaultdict
from itertools import combinations
from typing import Dict, Set, Tuple

from utils import BaseCoord as Coord, read_grid
from utils import read_data


class City:
    all_antennae: Dict[Coord, str]
    per_freq: Dict[str, Set[Coord]]
    antinodes: Dict[str, Set[Coord]]
    harmonics: Dict[str, Set[Coord]]
    max_x: int
    max_y: int

    def __init__(self, raw_map: str):
        self.all_antennae = {}
        self.per_freq = defaultdict(set)
        pos = Coord(0, 0)
        for pos, char in read_grid(raw_map):
            if char.isalnum():
                self.all_antennae[pos] = char
                self.per_freq[char].add(pos)
        self.max_x, self.max_y = pos.x, pos.y

        self.antinodes = defaultdict(set)
        self.harmonics = defaultdict(set)
        for freq, locs in self.per_freq.items():
            for pair in combinations(locs, 2):
                self.antinodes[freq] |= self._antinodes(pair)
                self.harmonics[freq] |= self._harmonics(pair)

    def in_bounds(self, loc: Coord) -> bool:
        return 0 <= loc.x <= self.max_x and 0 <= loc.y <= self.max_y

    def _antinodes(self, pair: Tuple[Coord, Coord]) -> Set[Coord]:
        first, second = pair
        slope = first - second
        return {x for x in (first + slope, second - slope) if self.in_bounds(x)}

    def _harmonics(self, pair: Tuple[Coord, Coord]) -> Set[Coord]:
        first, second = pair
        slope = first - second
        harmonics = set()
        curloc = first
        while self.in_bounds(curloc):
            harmonics.add(curloc)
            curloc = curloc + slope
        curloc = second
        while self.in_bounds(curloc):
            harmonics.add(curloc)
            curloc = curloc - slope
        return harmonics


def main():
    city = City(read_data())
    print(f"Part one: {len(set().union(*city.antinodes.values()))}")
    print(f"Part two: {len(set().union(*city.harmonics.values()))}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
