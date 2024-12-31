import math
from collections import defaultdict, deque
from functools import cache
from itertools import combinations_with_replacement
from typing import Dict, Tuple, Iterable, List

from utils import read_data, BaseCoord as Coord
import time

DIRS = {"^": Coord(x=0, y=-1), ">": Coord(x=1, y=0), "v": Coord(x=0, y=1), "<": Coord(x=-1, y=0)}
# precalculated SHORTEST_PATHS via A*, then froze the values into a dict
# fmt: off
SHORTEST_PATHS = {('0', '0'): ('A',), ('0', '1'): ('^<A',), ('0', '2'): ('^A',), ('0', '3'): ('^>A', '>^A'), ('0', '4'): ('^^<A', '^<^A'), ('0', '5'): ('^^A',), ('0', '6'): ('^^>A', '^>^A', '>^^A'), ('0', '7'): ('^^^<A', '^^<^A', '^<^^A'), ('0', '8'): ('^^^A',), ('0', '9'): ('^^^>A', '^^>^A', '^>^^A', '>^^^A'), ('0', 'A'): ('>A',), ('1', '0'): ('>vA',), ('1', '1'): ('A',), ('1', '2'): ('>A',), ('1', '3'): ('>>A',), ('1', '4'): ('^A',), ('1', '5'): ('^>A', '>^A'), ('1', '6'): ('^>>A', '>^>A', '>>^A'), ('1', '7'): ('^^A',), ('1', '8'): ('^^>A', '^>^A', '>^^A'), ('1', '9'): ('^^>>A', '^>^>A', '^>>^A', '>^^>A', '>^>^A', '>>^^A'), ('1', 'A'): ('>>vA', '>v>A'), ('2', '0'): ('vA',), ('2', '1'): ('<A',), ('2', '2'): ('A',), ('2', '3'): ('>A',), ('2', '4'): ('^<A', '<^A'), ('2', '5'): ('^A',), ('2', '6'): ('^>A', '>^A'), ('2', '7'): ('^^<A', '^<^A', '<^^A'), ('2', '8'): ('^^A',), ('2', '9'): ('^^>A', '^>^A', '>^^A'), ('2', 'A'): ('>vA', 'v>A'), ('3', '0'): ('v<A', '<vA'), ('3', '1'): ('<<A',), ('3', '2'): ('<A',), ('3', '3'): ('A',), ('3', '4'): ('^<<A', '<^<A', '<<^A'), ('3', '5'): ('^<A', '<^A'), ('3', '6'): ('^A',), ('3', '7'): ('^^<<A', '^<^<A', '^<<^A', '<^^<A', '<^<^A', '<<^^A'), ('3', '8'): ('^^<A', '^<^A', '<^^A'), ('3', '9'): ('^^A',), ('3', 'A'): ('vA',), ('4', '0'): ('>vvA', 'v>vA'), ('4', '1'): ('vA',), ('4', '2'): ('>vA', 'v>A'), ('4', '3'): ('>>vA', '>v>A', 'v>>A'), ('4', '4'): ('A',), ('4', '5'): ('>A',), ('4', '6'): ('>>A',), ('4', '7'): ('^A',), ('4', '8'): ('^>A', '>^A'), ('4', '9'): ('^>>A', '>^>A', '>>^A'), ('4', 'A'): ('>>vvA', '>v>vA', '>vv>A', 'v>>vA', 'v>v>A'), ('5', '0'): ('vvA',), ('5', '1'): ('v<A', '<vA'), ('5', '2'): ('vA',), ('5', '3'): ('>vA', 'v>A'), ('5', '4'): ('<A',), ('5', '5'): ('A',), ('5', '6'): ('>A',), ('5', '7'): ('^<A', '<^A'), ('5', '8'): ('^A',), ('5', '9'): ('^>A', '>^A'), ('5', 'A'): ('>vvA', 'v>vA', 'vv>A'), ('6', '0'): ('vv<A', 'v<vA', '<vvA'), ('6', '1'): ('v<<A', '<v<A', '<<vA'), ('6', '2'): ('v<A', '<vA'), ('6', '3'): ('vA',), ('6', '4'): ('<<A',), ('6', '5'): ('<A',), ('6', '6'): ('A',), ('6', '7'): ('^<<A', '<^<A', '<<^A'), ('6', '8'): ('^<A', '<^A'), ('6', '9'): ('^A',), ('6', 'A'): ('vvA',), ('7', '0'): ('>vvvA', 'v>vvA', 'vv>vA'), ('7', '1'): ('vvA',), ('7', '2'): ('>vvA', 'v>vA', 'vv>A'), ('7', '3'): ('>>vvA', '>v>vA', '>vv>A', 'v>>vA', 'v>v>A', 'vv>>A'), ('7', '4'): ('vA',), ('7', '5'): ('>vA', 'v>A'), ('7', '6'): ('>>vA', '>v>A', 'v>>A'), ('7', '7'): ('A',), ('7', '8'): ('>A',), ('7', '9'): ('>>A',), ('7', 'A'): ('>>vvvA', '>v>vvA', '>vv>vA', '>vvv>A', 'v>>vvA', 'v>v>vA', 'v>vv>A', 'vv>>vA', 'vv>v>A'), ('8', '0'): ('vvvA',), ('8', '1'): ('vv<A', 'v<vA', '<vvA'), ('8', '2'): ('vvA',), ('8', '3'): ('>vvA', 'v>vA', 'vv>A'), ('8', '4'): ('v<A', '<vA'), ('8', '5'): ('vA',), ('8', '6'): ('>vA', 'v>A'), ('8', '7'): ('<A',), ('8', '8'): ('A',), ('8', '9'): ('>A',), ('8', 'A'): ('>vvvA', 'v>vvA', 'vv>vA', 'vvv>A'), ('9', '0'): ('vvv<A', 'vv<vA', 'v<vvA', '<vvvA'), ('9', '1'): ('vv<<A', 'v<v<A', 'v<<vA', '<vv<A', '<v<vA', '<<vvA'), ('9', '2'): ('vv<A', 'v<vA', '<vvA'), ('9', '3'): ('vvA',), ('9', '4'): ('v<<A', '<v<A', '<<vA'), ('9', '5'): ('v<A', '<vA'), ('9', '6'): ('vA',), ('9', '7'): ('<<A',), ('9', '8'): ('<A',), ('9', '9'): ('A',), ('9', 'A'): ('vvvA',), ('<', '<'): ('A',), ('<', '>'): ('>>A',), ('<', 'A'): ('>^>A', '>>^A'), ('<', '^'): ('>^A',), ('<', 'v'): ('>A',), ('>', '<'): ('<<A',), ('>', '>'): ('A',), ('>', 'A'): ('^A',), ('>', '^'): ('^<A', '<^A'), ('>', 'v'): ('<A',), ('A', '0'): ('<A',), ('A', '1'): ('^<<A', '<^<A'), ('A', '2'): ('^<A', '<^A'), ('A', '3'): ('^A',), ('A', '4'): ('^^<<A', '^<^<A', '^<<^A', '<^^<A', '<^<^A'), ('A', '5'): ('^^<A', '^<^A', '<^^A'), ('A', '6'): ('^^A',), ('A', '7'): ('^^^<<A', '^^<^<A', '^^<<^A', '^<^^<A', '^<^<^A', '^<<^^A', '<^^^<A', '<^^<^A', '<^<^^A'), ('A', '8'): ('^^^<A', '^^<^A', '^<^^A', '<^^^A'), ('A', '9'): ('^^^A',), ('A', '<'): ('v<<A', '<v<A'), ('A', '>'): ('vA',), ('A', 'A'): ('A',), ('A', '^'): ('<A',), ('A', 'v'): ('v<A', '<vA'), ('^', '<'): ('v<A',), ('^', '>'): ('>vA', 'v>A'), ('^', 'A'): ('>A',), ('^', '^'): ('A',), ('^', 'v'): ('vA',), ('v', '<'): ('<A',), ('v', '>'): ('>A',), ('v', 'A'): ('^>A', '>^A'), ('v', '^'): ('^A',), ('v', 'v'): ('A',)}


@cache
def gen_shortest(code: str, depth_left: int = 3) -> int:
    curpos = 'A'
    min_total = 0
    if depth_left == 0:
        return len(code)
    for char in code:
        min_total += min(gen_shortest(x, depth_left-1) for x in SHORTEST_PATHS[(curpos, char)])
        curpos = char
    return min_total


TEST = """029A
980A
179A
456A
379A"""


def main():
    print(f"Part one: {sum(int(x[:-1]) * gen_shortest(x, 3) for x in read_data().splitlines())}")
    print(f"Part two: {sum(int(x[:-1]) * gen_shortest(x, 25) for x in read_data().splitlines())}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")


# RAW_NUMPAD_LOCS = [Coord(x=x, y=y) for y in range(3) for x in range(3)] + [Coord(x=1, y=3), Coord(x=2, y=3)]
# RAW_DIRPAD_LOCS = [Coord(x=1, y=0), Coord(x=2, y=0)] + [Coord(x=x, y=1) for x in range(3)]
# NUMPAD = {k: v for k, v in zip("7894561230A", RAW_NUMPAD_LOCS)}
# DIRPAD = {k: v for k, v in zip("^A<v>", RAW_DIRPAD_LOCS)}
#
#
# def shortest_paths(locs: Dict[str, Coord]) -> Dict[Tuple[str, str], Tuple[str, ...]]:
#     def shortest_paths_for_pair(start_key, end_key) -> Iterable[str]:
#         stack = deque([(locs[start_key], '')])
#         min_lengths = defaultdict(lambda: 999999)
#
#         while stack:
#             curloc, path = stack.popleft()
#             min_lengths[curloc] = min(min_lengths[curloc], len(path))
#             if curloc == locs[end_key]:
#                 yield path + "A"
#                 continue
#             for heading in DIRS:
#                 neighbor = curloc + DIRS[heading]
#                 if neighbor not in locs.values() or min_lengths[neighbor] < len(path):
#                     continue
#                 stack.append((neighbor, path + heading))
#
#     paths = {}
#     for first in locs:
#         for second in locs:
#             paths[(first, second)] = tuple(shortest_paths_for_pair(first, second))
#     return paths
#
# SHORTEST_PATHS = shortest_paths(NUMPAD) | shortest_paths(DIRPAD)
# SHORTEST_PATHS = {k: v for k, v in sorted(SHORTEST_PATHS.items())}