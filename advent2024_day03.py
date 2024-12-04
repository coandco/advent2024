import re
import time

from utils import read_data

MULS = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
# The crucial bit of MIDDLE_DONTS is the non-greedy matcher .*?, which makes sure
# we only grab one don't/do pair with each match
MIDDLE_DONTS = re.compile(r"don\'t\(\).*?do\(\)")
# Once we've removed all the middle pairs, remove from the final don't to the end of the line
END_DONT = re.compile(r"don\'t\(\).*$")


def main():
    # Newlines trip up the regexes
    data = read_data().replace("\n", "")
    # Simple regex to pull just x and y out of the mul(x,y), then multiply them and add them
    print(f"Part one: {sum(int(x[0]) * int(x[1]) for x in MULS.findall(data))}")
    # Do some cheeky raw-string replacements to remove don't/do pairs in the middle and don't at the end
    part_two_raw = END_DONT.sub("", MIDDLE_DONTS.sub("", data))
    # Now we have a string that just has valid mul()s, so process it the same way as part one
    print(f"Part two: {sum(int(x[0]) * int(x[1]) for x in MULS.findall(part_two_raw))}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
