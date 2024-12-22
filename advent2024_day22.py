import time
from collections import defaultdict
from typing import Dict, List, Tuple

from utils import read_data


def step_one(secret: int) -> int:
    return (secret ^ (secret << 6)) % 16777216


def step_two(secret: int) -> int:
    return (secret ^ (secret >> 5)) % 16777216


def step_three(secret: int) -> int:
    return (secret ^ (secret << 11)) % 16777216


def evolve_secret(secret: int) -> int:
    return step_three(step_two(step_one(secret)))


def evolve_n_times(secret: int, times: int) -> List[int]:
    secret = [secret]
    for _ in range(times):
        secret.append(evolve_secret(secret[-1]))
    return secret


def measure_sequences(last_digits: List[List[int]], changes: List[List[int]]) -> Dict[Tuple[int, ...], int]:
    sequence_scores = defaultdict(int)
    for i in range(len(last_digits)):
        already_seen = set()
        for j in range(4, len(last_digits[i])):
            sequence = tuple(changes[i][j - 3 : j + 1])
            if not sequence in already_seen:
                sequence_scores[sequence] += last_digits[i][j]
                already_seen.add(sequence)
    return sequence_scores


def main():
    initials = [int(x) for x in read_data().splitlines()]
    all_secrets = [evolve_n_times(x, 2000) for x in initials]
    print(f"Part one: {sum(x[-1] for x in all_secrets)}")
    all_last_digits = [[x % 10 for x in buyer] for buyer in all_secrets]
    all_changes = [[None] + [x[0] - x[1] for x in zip(buyer[1:], buyer[:-1])] for buyer in all_last_digits]
    sequence_scores = measure_sequences(all_last_digits, all_changes)
    print(f"Part two: {max(sequence_scores.values())}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
