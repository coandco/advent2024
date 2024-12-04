import time
from typing import Dict, List

from utils import ALL_NEIGHBORS_2D
from utils import BaseCoord as Coord
from utils import read_data


class Board:
    board: Dict[Coord, str]
    max_x: int
    max_y: int

    def __init__(self, board: Dict[Coord, str], max_x: int, max_y: int):
        self.board = board
        self.max_x = max_x
        self.max_y = max_y

    @staticmethod
    def from_lines(lines: List[str]) -> "Board":
        board = {}
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                board[Coord(x=x, y=y)] = char
        return Board(board, max_x=x, max_y=y)

    def in_bounds(self, loc: Coord) -> bool:
        return 0 <= loc.x <= self.max_x and 0 <= loc.y <= self.max_y

    def get_word(self, loc: Coord, heading: Coord, length: int = 4) -> str:
        word = []
        for _ in range(length):
            if not self.in_bounds(loc):
                return "".join(word)
            word.append(self.board[loc])
            loc = loc + heading
        return "".join(word)

    def scan_xmas(self) -> int:
        seen = 0
        for loc in self.board:
            for heading in ALL_NEIGHBORS_2D:
                if self.board[loc] == "X" and self.get_word(loc, heading) == "XMAS":
                    seen += 1
        return seen

    def check_a(self, loc: Coord) -> bool:
        NW = loc + Coord(x=-1, y=-1)
        SE = loc + Coord(x=1, y=1)
        NE = loc + Coord(x=1, y=-1)
        SW = loc + Coord(x=-1, y=1)
        for one, two in ((NW, SE), (NE, SW)):
            if not self.in_bounds(one) or not self.in_bounds(two):
                return False
            if self.board[one] not in ("M", "S"):
                return False
            if self.board[two] not in ("M", "S") or self.board[one] == self.board[two]:
                return False
        return True

    def search_x(self) -> int:
        seen = 0
        for loc in self.board:
            if self.board[loc] == "A" and self.check_a(loc):
                seen += 1
        return seen


def main():
    board = Board.from_lines(read_data().splitlines())
    print(f"Part one: {board.scan_xmas()}")
    print(f"Part two: {board.search_x()}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
