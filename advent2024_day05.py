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

    def validate(self, pagelist: List[int]) -> bool:
        all_pages = set(pagelist)
        for i, pagenum in enumerate(pagelist):
            if (self.before[pagenum] & all_pages) - set(pagelist[:i]):
                return False
        return True

    def reorder(self, pagelist: List[int]):
        all_pages = set(pagelist)
        # Get just the subset of self.before that contains the pages in our list
        page_ordering = {k: v & all_pages for k, v in self.before.items() if k in all_pages}
        order = []
        while page_ordering:
            # Get a page that doesn't have anything before it
            valid_page = {k for k, v in page_ordering.items() if not v}.pop()
            order.append(valid_page)
            # Delete the page and remove it from all sets
            del page_ordering[valid_page]
            for k, v in page_ordering.items():
                v.discard(valid_page)
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
