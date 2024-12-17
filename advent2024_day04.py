import time
from typing import Dict

from utils import ALL_NEIGHBORS_2D, read_grid
from utils import BaseCoord as Coord
from utils import read_data

Board = Dict[Coord, str]


def is_xmas(board: Board, loc: Coord, heading: Coord) -> bool:
    word = "XMAS"
    for i in range(4):
        if board.get(loc) != word[i]:
            return False
        loc = loc + heading
    return True


def scan_xmas(board: Board) -> int:
    def num_x_matches(loc: Coord) -> int:
        return sum(is_xmas(board, loc, heading) for heading in ALL_NEIGHBORS_2D)

    return sum(num_x_matches(loc) for loc in board if board[loc] == "X")


def check_a(board: Board, loc: Coord) -> bool:
    nw, se = board.get(loc + Coord(x=-1, y=-1)), board.get(loc + Coord(x=1, y=1))
    ne, sw = board.get(loc + Coord(x=1, y=-1)), board.get(loc + Coord(x=-1, y=1))
    for char1, char2 in ((nw, se), (ne, sw)):
        if {char1, char2} != {"M", "S"}:
            return False
    return True


def scan_x_mas(board: Board) -> int:
    return sum(check_a(board, x) for x in board if board[x] == "A")


def main():
    board = {}
    for pos, char in read_grid(read_data()):
        board[pos] = char

    print(f"Part one: {scan_xmas(board)}")
    print(f"Part two: {scan_x_mas(board)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
