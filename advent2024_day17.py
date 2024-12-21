import re
import time
from typing import Dict, Iterable, List, NamedTuple, Optional, Self, Tuple

from utils import read_data

DIGITS = re.compile(r"\d+")


OPCODES = [
    # adv
    lambda state, arg: {"a": state.a // pow(2, state.combo_val(arg)), "pc": state.pc + 2},
    # bxl
    lambda state, arg: {"b": state.b ^ arg, "pc": state.pc + 2},
    # bst
    lambda state, arg: {"b": state.combo_val(arg) % 8, "pc": state.pc + 2},
    # jnz
    lambda state, arg: {"pc": arg if state.a != 0 else state.pc + 2},
    # bxc
    lambda state, arg: {"b": state.b ^ state.c, "pc": state.pc + 2},
    # out
    lambda state, arg: {"pc": state.pc + 2},
    # bdv
    lambda state, arg: {"b": state.a // pow(2, state.combo_val(arg)), "pc": state.pc + 2},
    # cdv
    lambda state, arg: {"c": state.a // pow(2, state.combo_val(arg)), "pc": state.pc + 2},
]


class ProgramState(NamedTuple):
    a: int = 0
    b: int = 0
    c: int = 0
    pc: int = 0

    def combo_val(self, val: int) -> int:
        if val in (0, 1, 2, 3):
            return val
        if val in (4, 5, 6):
            return (self.a, self.b, self.c)[val - 4]
        raise Exception("Unknown combo val!")

    def changed_state(self, changed_vals: Dict[str, int]):
        return ProgramState(**(self._asdict() | changed_vals))

    def execute(self, program: List[int]) -> Tuple[Self, Optional[int]]:
        op, arg = program[self.pc : self.pc + 2]
        output = self.combo_val(arg) % 8 if op == 5 else None
        return self.changed_state(OPCODES[op](self, arg)), output


def run_program(state: ProgramState, program: List[int]) -> List[int]:
    all_output = []
    while 0 <= state.pc < len(program):
        state, output = state.execute(program)
        if output is not None:
            all_output.append(output)
    return all_output


def run_singleton(a: int, program: List[int]) -> int:
    state = ProgramState(a=a, b=0, c=0, pc=0)
    while 0 <= state.pc < len(program):
        state, output = state.execute(program)
        if output is not None:
            return output


def calc_a(prev_a: int, program: List[int], index: Optional[int] = -1) -> Iterable[int]:
    if index == -(len(program) + 1):
        yield prev_a
        return
    new_a = prev_a << 3
    for i in range(8):
        if run_singleton(new_a + i, program) == program[index]:
            yield from calc_a(new_a + i, program, index - 1)


def main():
    a, b, c, *program = DIGITS.findall(read_data())
    state = ProgramState(a=int(a), b=int(b), c=int(c), pc=0)
    program = [int(x) for x in program]
    print(f"Part one: {','.join(str(x) for x in run_program(state, program))}")
    print(f"Part two: {min(calc_a(0, program))}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
