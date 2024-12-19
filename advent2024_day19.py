import time
from collections import Counter, defaultdict
from typing import Dict, List

from utils import read_data


def combinations(components: Dict[str, List[str]], desired: str) -> int:
    ways_to_reach = [0] * (len(desired) + 1)
    ways_to_reach[0] = 1
    for i in range(len(desired)):
        if ways_to_reach[i] == 0:
            continue
        for increment, how_many in Counter(len(x) for x in components[desired[i]] if desired[i:].startswith(x)).items():
            ways_to_reach[i + increment] += ways_to_reach[i] * how_many
    return ways_to_reach[-1]


def main():
    raw_components, raw_desires = read_data().split("\n\n")
    components = sorted(raw_components.split(", "))
    sorted_components = defaultdict(list)
    for component in components:
        sorted_components[component[0]].append(component)
    combos = [combinations(sorted_components, x) for x in raw_desires.splitlines()]
    print(f"Part one: {len([x for x in combos if x])}")
    print(f"Part two: {sum(combos)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
