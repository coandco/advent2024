import time
from collections import deque, defaultdict
from typing import Set, Dict, Tuple, Deque

from utils import read_data, read_grid, BaseCoord as Coord


DIRS = {"N": Coord(x=0, y=-1), "E": Coord(x=1, y=0), "S": Coord(x=0, y=1), "W": Coord(x=-1, y=0)}
RIGHT_TURNS = {"N": "E", "E": "S", "S": "W", "W": "N"}
LEFT_TURNS = {"N": "W", "E": "N", "S": "E", "W": "S"}


class Maze:
    walls: Set[Coord]
    start: Coord
    end: Coord

    def __init__(self, raw: str):
        self.walls = set()
        for pos, char in read_grid(raw, Coord):
            if char == "#":
                self.walls.add(pos)
            elif char == "S":
                self.start = pos
            elif char == "E":
                self.end = pos

    def score(self) -> Tuple[int, int]:
        # If we want to make sure we hit all min-value paths instead of just a single min-value path,
        # we can only cache by position/heading combo, rather than just position
        min_scores: Dict[Coord, Dict[str, int]] = defaultdict(lambda: defaultdict(lambda: 99999999))
        # We keep track of all squares that are on paths to the end we find and index them by score
        # so we can pull just the lowest-score ones for part 2
        paths_by_score: Dict[int, Set[Coord]] = defaultdict(set)
        stack: Deque[Tuple[int, Tuple[Coord, ...], str]] = deque([(0, (self.start,), 'E')])
        while stack:
            score, path, heading = stack.popleft()
            min_end_score = min(min_scores[self.end].values()) if min_scores[self.end] else 99999999
            if score > min_end_score or score > min_scores[path[-1]][heading]:
                continue
            min_scores[path[-1]][heading] = min(min_scores[path[-1]][heading], score)
            if path[-1] == self.end:
                paths_by_score[score].update(path)
            if (new_loc := path[-1] + DIRS[LEFT_TURNS[heading]]) not in self.walls:
                stack.append((score + 1001, path + (new_loc,), LEFT_TURNS[heading]))
            if (new_loc := path[-1] + DIRS[RIGHT_TURNS[heading]]) not in self.walls:
                stack.append((score + 1001, path + (new_loc,), RIGHT_TURNS[heading]))
            if (new_loc := path[-1] + DIRS[heading]) not in self.walls:
                stack.append((score + 1, path + (new_loc,), heading))
        min_end_score = min(min_scores[self.end].values())
        return min_end_score, len(paths_by_score[min_end_score])


def main():
    maze = Maze(read_data())
    min_score, num_squares_in_min_paths = maze.score()
    print(f"Part one: {min_score}")
    print(f"Part two: {num_squares_in_min_paths}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
