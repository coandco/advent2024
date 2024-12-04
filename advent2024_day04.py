import time
from typing import Dict

from utils import ALL_NEIGHBORS_2D
from utils import BaseCoord as Coord
from utils import read_data

Board = Dict[Coord, str]

def get_word(board: Board, loc: Coord, heading: Coord) -> str:
    word = []
    for _ in range(4):
        char = board.get(loc, None)
        if not char:
            return "".join(word)
        word.append(char)
        loc = loc + heading
    return "".join(word)

def num_x_matches(board: Board, loc: Coord) -> int:
    return sum(get_word(board, loc, heading) == "XMAS" for heading in ALL_NEIGHBORS_2D)

def scan_xmas(board: Board) -> int:
    return sum(num_x_matches(board, loc) for loc in board if board[loc] == "X")

def check_a(board: Board, loc: Coord) -> bool:
    NW, SE = board.get(loc + Coord(x=-1, y=-1)), board.get(loc + Coord(x=1, y=1))
    NE, SW = board.get(loc + Coord(x=1, y=-1)), board.get(loc + Coord(x=-1, y=1))
    for char1, char2 in ((NW, SE), (NE, SW)):
        if {char1, char2} != {"M", "S"}:
            return False
    return True

def search_x(board: Board) -> int:
    return sum(check_a(board, x) for x in board if board[x] == "A")

def main():
    board = {}
    for y, line in enumerate(read_data().splitlines()):
        for x, char in enumerate(line):
            board[Coord(x=x, y=y)] = char

    print(f"Part one: {scan_xmas(board)}")
    print(f"Part two: {search_x(board)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
