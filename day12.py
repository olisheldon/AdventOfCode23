from pathlib import Path
import argparse
from enum import Enum, auto
from functools import lru_cache


class SpringType(Enum):
    OPERATIONAL = auto()
    DAMAGED = auto()
    UNKNOWN = auto()

    def __repr__(self) -> str:
        return SpringType.from_spring(self)

    @classmethod
    def from_str(cls, c: str) -> 'SpringType':
        match c:
            case '.':
                return cls.OPERATIONAL
            case '#':
                return cls.DAMAGED
            case '?':
                return cls.UNKNOWN
            case _:
                raise RuntimeError(f"SpringType {c} is not recognised.")

    @classmethod
    def from_spring(cls, s: 'SpringType') -> str:
        match s:
            case cls.OPERATIONAL:
                return '.'
            case cls.DAMAGED:
                return '#'
            case cls.UNKNOWN:
                return '?'
            case _:
                raise RuntimeError(f"SpringType {s} is not recognised.")


class Row:

    def __init__(self, springs: list[SpringType], configuration: list[int]):
        self.springs: list[SpringType] = springs
        self.configuration: list[int] = configuration

    def __repr__(self) -> str:
        return f"{''.join(spring.__repr__() for spring in self.springs)} {self.configuration}"

    def combinations(self, folding_factor: int = 1) -> int:
        springs = self.springs.copy()
        for _ in range(folding_factor - 1):
            springs.extend([SpringType.UNKNOWN] + self.springs)
        return self._combinations(tuple(springs), tuple(self.configuration * folding_factor))

    @staticmethod
    @lru_cache
    def _combinations(springs: tuple[SpringType, ...], configuration: tuple[int, ...]) -> int:

        # Base cases
        if not springs:
            # can only be valid if we are not expecting any more operational springs
            return 1 if not configuration else 0
        if not configuration:
            # if we are not expecting more springs but there are still
            return 1 if SpringType.DAMAGED not in springs else 0
            # damaged springs this must not be valid

        result = 0

        # Decisions
        if springs[0] in (SpringType.OPERATIONAL, SpringType.UNKNOWN):
            # treat unknown spring as an operational spring
            result += Row._combinations(springs[1:], configuration)

        if springs[0] in (SpringType.DAMAGED, SpringType.UNKNOWN):
            # treat unknown as a damaged spring
            # this is the start of a block of damaged springs, but we need to determine: valid or invalid?
            if (configuration[0] <= len(springs) and  # number of possible springs we are considering must be less than number of springs left
               # block of damaged springs can't contain operational spring
                SpringType.OPERATIONAL not in springs[:configuration[0]] and
                (configuration[0] == len(springs) or  # not springs left, so number of springs left equals the configuration
                    springs[configuration[0]] != SpringType.DAMAGED)):  # OR if there are springs afterwards the next spring must not be damaged!
                result += Row._combinations(springs[configuration[0] + 1:],  # index springs by configuration[0] + 1 as we are looking for new damaged blocks
                                            configuration[1:])                # and we know springs[configuration[0] + 1] is unknown or operational!
                # We also found a damaged block, so remove the first config and recurse.
        return result


class Field:

    def __init__(self, field_str: list[str]):
        self.rows: list[Row] = Field.create_field(field_str)

    @classmethod
    def create_field(cls, field_str: list[str]) -> list[Row]:
        res: list[Row] = []
        for line in field_str:
            springs, spring_lengths = line.split()
            res.append(Row([SpringType.from_str(spring) for spring in springs], [
                       int(spring_length) for spring_length in spring_lengths.split(',')]))
        return res


class Day12:

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.field = Field(self.parse_file())

    def parse_file(self) -> list[str]:
        with open(self.filepath, 'r', encoding="utf-8") as f:
            return f.read().splitlines()

    def parse(self) -> list[str]:
        pass

    def part_1(self) -> int:
        return sum(row.combinations() for row in self.field.rows)

    def part_2(self) -> int:
        return sum(row.combinations(folding_factor=5) for row in self.field.rows)


if __name__ == "__main__":
    INPUT_FILEPATH = Path(__file__).parent / "data" / \
        f"{Path(__file__).stem}.txt"
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?',
                        default=INPUT_FILEPATH, help=f"Path to data for {Path(__file__).stem}")
    args = parser.parse_args()

    day12 = Day12(Path(args.input).absolute())
    print(day12.part_1())
    print(day12.part_2())
