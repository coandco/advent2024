import time
from collections import defaultdict
from itertools import combinations
from typing import Dict, FrozenSet, Iterable, List, Set

from utils import read_data


def load_connections(raw: str) -> Dict[str, Set[str]]:
    connections = defaultdict(set)
    for line in raw.splitlines():
        first, second = line.split("-")
        connections[first].add(second)
        connections[second].add(first)
    return connections


def find_triplets(connections: Dict[str, Set[str]], starts_with: str) -> Set[FrozenSet[str]]:
    triplets: Set[FrozenSet[str]] = set()
    for comp in [x for x in connections if x.startswith(starts_with)]:
        for first, second in combinations(connections[comp], 2):
            if first in connections[second]:
                triplets.add(frozenset([comp, first, second]))
    return triplets


def find_set(connections: Dict[str, Set[str]], first: str) -> Set[str]:
    in_set = {first}
    to_check = connections[first].copy()
    invalid = set()
    while to_check:
        other_comp = to_check.pop()
        if in_set.issubset(connections[other_comp]):
            in_set.add(other_comp)
            to_check.update(connections[other_comp] - in_set - invalid)
        else:
            invalid.add(other_comp)
    return in_set


def find_all_sets(connections: Dict[str, Set[str]]) -> Iterable[List[str]]:
    remaining = set(connections.keys())
    while remaining:
        node = remaining.pop()
        node_set = find_set(connections, node)
        yield sorted(node_set)
        remaining -= node_set


def main():
    connections = load_connections(read_data())
    print(f"Part one: {len(find_triplets(connections, 't'))}")
    print(f"Part two: {','.join(max(find_all_sets(connections), key=lambda x: len(x)))}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
