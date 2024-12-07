import time
from itertools import product
from typing import List

from utils import read_data


class Equation:
    result: int
    operands: List[int]

    def __init__(self, line: str):
        result, raw_operands = line.split(":")
        self.result = int(result)
        self.operands = [int(x) for x in raw_operands.split()]

    def validate(self, operators: str = "+*") -> bool:
        for possibility in product(operators, repeat=len(self.operands) - 1):
            curval = self.operands[0]
            for i, op in enumerate(possibility, start=1):
                if op == "+":
                    curval = curval + self.operands[i]
                elif op == "*":
                    curval = curval * self.operands[i]
                elif op == "|":
                    curval = int(str(curval) + str(self.operands[i]))
                else:
                    raise Exception(f"Unknown operator {op}")
            if curval == self.result:
                return True
        return False


def main():
    equations = [Equation(x) for x in read_data().splitlines()]
    print(f"Part one: {sum(x.result for x in equations if x.validate())}")
    print(f"Part two: {sum(x.result for x in equations if x.validate(operators='+*|'))}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
