import time
from collections import defaultdict
from typing import Dict, List, Set

from utils import read_data


class Rules:
    before: Dict[int, Set[int]]

    def __init__(self, raw_rules: str):
        self.before = defaultdict(set)
        for line in raw_rules.splitlines():
            before, after = line.split("|", maxsplit=1)
            self.before[int(after)].add(int(before))

    def validate(self, update_list: List[int]) -> bool:
        pages_in_list = set(update_list)
        for i, pagenum in enumerate(update_list):
            # If there are any pages we haven't seen already that are listed as before this one
            if (self.before[pagenum] & pages_in_list) - set(update_list[:i]):
                return False
        return True

    def reorder(self, update_list: List[int]):
        pages_in_list = set(update_list)
        # Get just the subset of self.before that contains the pages in our list
        local_rules = {k: v & pages_in_list for k, v in self.before.items() if k in pages_in_list}
        order = []
        while local_rules:
            # Get a page that doesn't have anything before it
            valid_page = {k for k, v in local_rules.items() if not v}.pop()
            order.append(valid_page)
            # Delete the page and remove it from all sets
            del local_rules[valid_page]
            for before_set in local_rules.values():
                before_set.discard(valid_page)
        return order


def main():
    raw_rules, raw_pages = read_data().split("\n\n")
    rules = Rules(raw_rules)
    pages = [[int(x) for x in line.split(",")] for line in raw_pages.splitlines()]
    p1_pages = [x[len(x) // 2] for x in pages if rules.validate(x)]
    print(f"Part one: {sum(p1_pages)}")
    p2_pages = [rules.reorder(x)[len(x) // 2] for x in pages if not rules.validate(x)]
    print(f"Part two: {sum(p2_pages)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
