import time
from collections import defaultdict
from typing import Dict, List, Set

from utils import read_data

BeforeMapType = Dict[int, Set[int]]


def validate(update_list: List[int], before: BeforeMapType) -> bool:
    pages_in_list = set(update_list)
    for i, pagenum in enumerate(update_list):
        # If there are any pages we haven't seen already that are listed as before this one
        if (before[pagenum] & pages_in_list) - set(update_list[:i]):
            return False
    return True


def reorder(update_list: List[int], before: BeforeMapType):
    pages_in_list = set(update_list)
    # Get just the subset of the before map that contains the pages in our list
    local_rules = {k: v & pages_in_list for k, v in before.items() if k in pages_in_list}
    order = []
    while local_rules:
        # Get a page that doesn't have anything before it
        valid_page = {k for k, v in local_rules.items() if not v}.pop()
        # Add it to our output
        order.append(valid_page)
        # Delete the page from the local rules and remove it from all sets
        del local_rules[valid_page]
        for before_set in local_rules.values():
            before_set.discard(valid_page)
    return order


def main():
    raw_rules, raw_updates = read_data().split("\n\n")
    before_map = defaultdict(set)
    for line in raw_rules.splitlines():
        before, after = line.split("|", maxsplit=1)
        before_map[int(after)].add(int(before))
    updates = [[int(x) for x in line.split(",")] for line in raw_updates.splitlines()]
    p1_pages = [x[len(x) // 2] for x in updates if validate(x, before_map)]
    print(f"Part one: {sum(p1_pages)}")
    p2_pages = [reorder(x, before_map)[len(x) // 2] for x in updates if not validate(x, before_map)]
    print(f"Part two: {sum(p2_pages)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
