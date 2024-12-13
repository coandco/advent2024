import re
import time
from typing import Iterable, NamedTuple, Optional, Tuple

from utils import BaseCoord as Coord
from utils import read_data

DIGITS = re.compile(r"[+-]?\d+")


class Machine(NamedTuple):
    a: Coord
    b: Coord
    prize: Coord

    @staticmethod
    def from_raw(data: str, offset: int = 0) -> "Machine":
        raw_ints = [[int(x) for x in DIGITS.findall(line)] for line in data.splitlines()]
        a = Coord(x=raw_ints[0][0], y=raw_ints[0][1])
        b = Coord(x=raw_ints[1][0], y=raw_ints[1][1])
        prize = Coord(x=raw_ints[2][0] + offset, y=raw_ints[2][1] + offset)
        return Machine(a=a, b=b, prize=prize)

    def linear_solve(self) -> Optional[int]:
        determinant = (self.a.x * self.b.y) - (self.a.y * self.b.x)
        if determinant == 0:
            # The machine isn't solvable, so we can't spend tokens on it
            return 0

        num_a = ((self.prize.x * self.b.y) - (self.prize.y * self.b.x)) / determinant
        num_b = ((self.prize.y * self.a.x) - (self.prize.x * self.a.y)) / determinant

        if not all(x.is_integer() for x in (num_a, num_b)):
            # The machine isn't solvable, so we can't spend tokens on it
            return 0
        return 3 * int(num_a) + int(num_b)


def main():
    machines = [Machine.from_raw(x) for x in read_data().split("\n\n")]
    print(f"Part one: {sum(x.linear_solve() for x in machines)}")
    p2_machines = [Machine.from_raw(x, offset=10000000000000) for x in read_data().split("\n\n")]
    print(f"Part two: {sum(x.linear_solve() for x in p2_machines)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
