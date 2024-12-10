import time
from collections import deque
from copy import copy
from dataclasses import dataclass
from itertools import islice
from typing import Iterable, List, Set

from utils import read_data


@dataclass
class File:
    length: int
    blocknum: int
    gap_after: int


class Diskmap:
    raw: List[int]
    files: List[File]
    filled: List[int]
    empty: List[int]

    def __init__(self, raw: str):
        self.raw = [int(x) for x in raw]
        self.filled = [x for i, x in enumerate(self.raw) if i % 2 == 0]
        self.empty = [x for i, x in enumerate(self.raw) if i % 2 != 0]
        self.files = []
        for i in range(len(self.filled)):
            gap = 0 if i >= len(self.empty) else self.empty[i]
            self.files.append(File(length=self.filled[i], blocknum=i, gap_after=gap))

    def vals_from_end(self):
        pos = len(self.filled) - 1
        while pos > 0:
            for _ in range(self.filled[pos]):
                yield pos
            pos -= 1

    def refragged_vals(self):
        amount_left = sum(self.filled)
        from_end = self.vals_from_end()

        for file in self.files[:-1]:
            yield from [file.blocknum] * min(file.length, amount_left)
            amount_left -= min(file.length, amount_left)
            yield from islice(from_end, min(file.gap_after, amount_left))
            amount_left -= min(file.gap_after, amount_left)

    def reshuffled_vals(self):
        files = deque(copy(x) for x in self.files)
        already_done: Set[int] = set()
        curindex = len(files) - 1
        while curindex:
            candidate = files[curindex]
            if candidate.blocknum in already_done:
                curindex -= 1
                continue
            for i in range(curindex):
                if candidate.length <= files[i].gap_after:
                    files[curindex - 1].gap_after += candidate.length + candidate.gap_after
                    del files[curindex]
                    files.insert(i + 1, candidate)
                    candidate.gap_after = files[i].gap_after - candidate.length
                    files[i].gap_after = 0
                    break
            else:
                curindex -= 1
            already_done.add(candidate.blocknum)
        for file in files:
            yield from [file.blocknum] * file.length
            yield from [-1] * file.gap_after

    def checksum(self, method: Iterable[int]) -> int:
        total = 0
        for i, val in enumerate(method):
            if val == -1:
                continue
            total += i * val
        return total


def main():
    diskmap = Diskmap(read_data())
    print(f"Part one: {diskmap.checksum(diskmap.refragged_vals())}")
    print(f"Part two: {diskmap.checksum(diskmap.reshuffled_vals())}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
