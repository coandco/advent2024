import time
from typing import Dict, List

from utils import ALL_NEIGHBORS_2D
from utils import BaseCoord as Coord
from utils import read_data


class Board:
    board: Dict[Coord, str]

    def __init__(self, board: Dict[Coord, str]):
        self.board = board

    @staticmethod
    def from_lines(lines: List[str]) -> "Board":
        board = {}
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                board[Coord(x=x, y=y)] = char
        return Board(board)

    def get_word(self, loc: Coord, heading: Coord, length: int = 4) -> str:
        word = []
        for _ in range(length):
            char = self.board.get(loc, None)
            if not char:
                return "".join(word)
            word.append(char)
            loc = loc + heading
        return "".join(word)

    def num_x_matches(self, loc: Coord) -> int:
        return sum(self.get_word(loc, heading) == "XMAS" for heading in ALL_NEIGHBORS_2D)

    def scan_xmas(self) -> int:
        return sum(self.num_x_matches(loc) for loc in self.board if self.board[loc] == "X")

    def check_a(self, loc: Coord) -> bool:
        NW, SE = self.board.get(loc + Coord(x=-1, y=-1)), self.board.get(loc + Coord(x=1, y=1))
        NE, SW = self.board.get(loc + Coord(x=1, y=-1)), self.board.get(loc + Coord(x=-1, y=1))
        for char1, char2 in ((NW, SE), (NE, SW)):
            if {char1, char2} != {"M", "S"}:
                return False
        return True

    def search_x(self) -> int:
        return sum(self.check_a(x) for x in self.board if self.board[x] == "A")


def main():
    board = Board.from_lines(read_data().splitlines())
    print(f"Part one: {board.scan_xmas()}")
    print(f"Part two: {board.search_x()}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
