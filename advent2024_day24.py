import time
from collections import defaultdict
from functools import cache
from typing import Dict, FrozenSet, List, Tuple, Optional, Iterable, Set, Self

from utils import read_data

OPS = {"AND": lambda x, y: x & y, "OR": lambda x, y: x | y, "XOR": lambda x, y: x ^ y}


Knowns = Dict[str, int]
Unknowns = Dict[str, Tuple[str, str, str]]


def get_output(known: Knowns, in1: str, op: str, in2: str) -> int:
    return OPS[op](known[in1], known[in2])


class Wires:
    known: Dict[str, int]
    unknown: Dict[str, Tuple[str, str, str]]
    inputs: Dict[FrozenSet[str], List[str]]

    def __init__(self, known: Knowns, unknown: Unknowns):
        self.known = known
        self.unknown = unknown
        self.inputs = defaultdict(list)
        for out, (in1, op, in2) in unknown.items():
            self.inputs[frozenset([in1, in2])].append(out)

    @classmethod
    def from_raw(cls, raw: str) -> Self:
        raw_known, raw_unknown = raw.split("\n\n")
        known = {}
        for line in raw_known.splitlines():
            k, v = line.split(": ")
            known[k] = int(v)

        unknown = {}
        for line in raw_unknown.splitlines():
            in1, op, in2, _, out = line.split()
            unknown[out] = (in1, op, in2)
        return cls(known, unknown)

    def gates_with_input(self, in_gate: str) -> Iterable[str]:
        for inputs, outputs in self.inputs.items():
            if in_gate in inputs:
                yield from outputs

    def bad_gates(self) -> Iterable[str]:
        for out, (in1, op, in2) in self.unknown.items():
            if out[0] == "z" and op != "XOR" and out != "z45":
                yield out
                continue
            if op == "XOR" and all(x[0] not in ("x", "y", "z") for x in (out, in1, in2)):
                yield out
                continue
            if op == "AND" and "x00" not in (in1, in2):
                if any(self.unknown[x][1] == "XOR" for x in self.gates_with_input(out)):
                    yield out
                    continue
            if op == "XOR" and "x00" not in (in1, in2):
                if any(self.unknown[x][1] == "OR" for x in self.gates_with_input(out)):
                    yield out
                    continue


    def evaluate(self, set_x: Optional[int] = None, set_y: Optional[int] = None, bits: int = 45) -> Optional[int]:
        known, unknown, unknown_inputs = self.known.copy(), self.unknown.copy(), self.inputs.copy()
        if set_x is not None:
            for i in range(bits+1):
                known[f"x{i:02}"] = set_x & 1
                set_x = set_x >> 1
        if set_y is not None:
            for i in range(bits+1):
                known[f"y{i:02}"] = set_y & 1
                set_y = set_y >> 1

        z_attrs = [f"z{i:02}" for i in range(bits, -1, -1)]
        while not z_attrs[0] in known:
            knowable_unknowns = [(k, v) for k, v in unknown_inputs.items() if k.issubset(known)]
            if not knowable_unknowns:
                return None
            for inputs, outputs in knowable_unknowns:
                for output in outputs:
                    known[output] = get_output(known, *unknown[output])
                    del unknown[output]
                del unknown_inputs[inputs]
        return int("".join(str(known[x]) for x in z_attrs), 2)


def main():
    wires = Wires.from_raw(read_data())
    print(f"Part one: {wires.evaluate()}")
    print(f"Part two: {','.join(sorted(wires.bad_gates()))}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
