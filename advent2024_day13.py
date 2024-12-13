from typing import NamedTuple, Iterable, Tuple

from utils import read_data, BaseCoord as Coord
import time
import re

DIGITS = re.compile(r'[+-]?\d+')


class Machine(NamedTuple):
    a: Coord
    b: Coord
    prize: Coord

    @staticmethod
    def from_raw(data: str) -> 'Machine':
        raw_ints = [[int(x) for x in DIGITS.findall(line)] for line in data.splitlines()]
        a = Coord(x=raw_ints[0][0], y=raw_ints[0][1])
        b = Coord(x=raw_ints[1][0], y=raw_ints[1][1])
        prize = Coord(x=raw_ints[2][0], y=raw_ints[2][1])
        return Machine(a=a, b=b, prize=prize)


    def btns_to_reach_prize(self, limit: int = 100) -> Iterable[Tuple[int, int]]:
        for a_times in range(limit+1):
            for b_times in range(limit+1):
                if (self.a * a_times) + (self.b * b_times) == self.prize:
                    yield a_times, b_times


def main():
    machines = [Machine.from_raw(x) for x in read_data().split("\n\n")]
    combinations = [list(x.btns_to_reach_prize()) for x in machines]
    combinations = [x for x in combinations if x]
    print(f"Part one: {sum(min((3*a)+b for a, b in combination) for combination in combinations)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
