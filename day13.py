from pathlib import Path
import argparse
from overrides import override
from enum import Enum, auto
from typing import Callable


class Covering(Enum):
    ASH = auto()
    ROCK = auto()

    def __repr__(self) -> str:
        return Covering.from_covering(self)

    @classmethod
    def from_str(cls, c: str) -> 'Covering':
        match c:
            case '.':
                return cls.ASH
            case '#':
                return cls.ROCK
            case _:
                raise RuntimeError(f"Covering {c} is not recognised.")

    @classmethod
    def from_covering(cls, s: 'Covering') -> str:
        match s:
            case cls.ASH:
                return '.'
            case cls.ROCK:
                return '#'
            case _:
                raise RuntimeError(f"Covering {s} is not recognised.")


class Pattern:

    def __init__(self, pattern_str: list[str]):
        self.pattern: list[list[Covering]] = []
        for line in pattern_str:
            self.pattern.append([Covering.from_str(elem) for elem in line])

    def find_reflection_indexes(self, smudge: bool = False) -> tuple[int, int]:
        if not smudge:
            return self._find_reflection_index(Pattern.submirror_equality, rowwise=True), self._find_reflection_index(Pattern.submirror_equality, rowwise=False)
        else:
            return self._find_reflection_index(Pattern.submirror_one_difference, rowwise=True), self._find_reflection_index(Pattern.submirror_one_difference, rowwise=False)

    def _find_reflection_index(self, predicate: Callable[[list[list[Covering]], list[list[Covering]]], bool], rowwise: bool = True) -> int:

        if rowwise:
            pattern = self.pattern
        else:
            # access pattern column-wise (transposed)
            pattern = list(zip(*self.pattern))

        for index in range(1, len(pattern)):
            above_partition = pattern[:index][::-1]
            below_partition = pattern[index:]

            above_partition = above_partition[:len(below_partition)]
            below_partition = below_partition[:len(above_partition)]

            if predicate(above_partition, below_partition):
                return index
        return 0

    @staticmethod
    def submirror_equality(pattern1: list[list[Covering]], pattern2: list[list[Covering]]) -> bool:
        return pattern1 == pattern2

    @staticmethod
    def submirror_one_difference(pattern1: list[list[Covering]], pattern2: list[list[Covering]]) -> bool:
        total_differences = 0
        for row1, row2 in zip(pattern1, pattern2):
            num_mismatches_in_row = sum(
                0 if elem1 == elem2 else 1 for elem1, elem2 in zip(row1, row2))
            total_differences += num_mismatches_in_row
        return total_differences == 1


class Day13:

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.patterns: list[Pattern] = [
            Pattern(pattern_str) for pattern_str in self.parse()]

    def parse_file(self) -> list[str]:
        with open(self.filepath, 'r', encoding="utf-8") as f:
            return f.read().splitlines()

    def parse(self) -> list[list[str]]:
        pattern_strs: list[list[str]] = [[]]
        for line in self.parse_file():
            if not line:
                pattern_strs.append([])
            else:
                pattern_strs[-1].append(line)
        return pattern_strs

    def part_1(self) -> int:
        def summarize(x): return 100 * x[0] + x[1]
        return sum(summarize(pattern.find_reflection_indexes()) for pattern in self.patterns)

    def part_2(self) -> int:
        def summarize(x): return 100 * x[0] + x[1]
        return sum(summarize(pattern.find_reflection_indexes(smudge=True)) for pattern in self.patterns)


if __name__ == "__main__":
    INPUT_FILEPATH = Path(__file__).parent / "data" / \
        f"{Path(__file__).stem}.txt"
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?',
                        default=INPUT_FILEPATH, help=f"Path to data for {Path(__file__).stem}")
    args = parser.parse_args()

    day13 = Day13(Path(args.input).absolute())
    print(day13.part_1())
    print(day13.part_2())
