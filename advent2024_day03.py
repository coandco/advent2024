from utils import read_data
import time
import re

MULS = re.compile(r'mul\((\d+),(\d+)\)')
MIDDLE_DONTS = re.compile(r'don\'t\(\).*?do\(\)')
END_DONT = re.compile(r'don\'t\(\).*$')


def main():
    # Newlines trip up the regexes
    data = read_data().replace("\n", "")
    print(f"Part one: {sum(int(x[0]) * int(x[1]) for x in MULS.findall(data))}")
    part_two_raw = END_DONT.sub('', MIDDLE_DONTS.sub('', data))
    print(f"Part two: {sum(int(x[0]) * int(x[1]) for x in MULS.findall(part_two_raw))}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
