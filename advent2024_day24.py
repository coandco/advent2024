import time
from collections import defaultdict
from itertools import chain
from typing import Dict, FrozenSet, List, Tuple

from utils import read_data

OPS = {"AND": lambda x, y: x & y, "OR": lambda x, y: x | y, "XOR": lambda x, y: x ^ y}


def get_output(known: Dict[str, int], in1: str, op: str, in2: str) -> int:
    return OPS[op](known[in1], known[in2])


def ingest(raw: str) -> Tuple[Dict[str, int], Dict[str, Tuple[str, str, str]], Dict[FrozenSet[str], List[str]]]:
    raw_known, raw_unknown = raw.split("\n\n")
    known: Dict[str, int] = {}
    for line in raw_known.splitlines():
        k, v = line.split(": ")
        known[k] = int(v)

    unknown_outputs: Dict[str, Tuple[str, str, str]] = {}
    unknown_inputs: Dict[FrozenSet[str], List[str]] = defaultdict(list)
    for line in raw_unknown.splitlines():
        in1, op, in2, _, out = line.split()
        unknown_outputs[out] = (in1, op, in2)
        unknown_inputs[frozenset([in1, in2])].append(out)
    return known, unknown_outputs, unknown_inputs


def main():
    known, unknown_outputs, unknown_inputs = ingest(read_data())

    while [x for x in unknown_outputs if x.startswith("z")]:
        knowable_unknowns = [(k, v) for k, v in unknown_inputs.items() if k.issubset(known)]
        for inputs, outputs in knowable_unknowns:
            for output in outputs:
                known[output] = get_output(known, *unknown_outputs[output])
                del unknown_outputs[output]
            del unknown_inputs[inputs]
    z_attrs = sorted((x for x in known if x.startswith("z")), reverse=True)
    z_str = "".join(str(known[x]) for x in z_attrs)
    print(f"Part one: {int(z_str, 2)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
