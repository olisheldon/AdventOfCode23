from overrides import override
from aoc23_base import DayBase
from enum import Enum, auto

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

    def find_reflection_indexes(self) -> tuple[int, int]:
        return self._find_reflection_index(rowwise=True), self._find_reflection_index(rowwise=False)

    def _find_reflection_index(self, rowwise: bool = True) -> int:

        if rowwise:
            pattern = self.pattern
        else:
            pattern = list(zip(*self.pattern))


        for index in range(1, len(pattern)):
            above_partition = pattern[:index][::-1]
            below_partition = pattern[index:]
            
            above_partition = above_partition[:len(below_partition)]
            below_partition = below_partition[:len(above_partition)]

            if above_partition == below_partition:
                return index
        return 0

class Day13(DayBase):
    
    def __init__(self):
        super().__init__()
        self.patterns: list[Pattern] = [Pattern(pattern_str) for pattern_str in self.parse()]

    def parse(self) -> list[list[str]]:
        pattern_strs: list[list[str]] = [[]]
        for line in self.input:
            if not line:
                pattern_strs.append([])
            else:
                pattern_strs[-1].append(line)
        return pattern_strs

    @override
    def part_1(self) -> int:
        summarize = lambda x : 100 * x[0] + x[1]
        return sum(summarize(pattern.find_reflection_indexes()) for pattern in self.patterns)

    @override
    def part_2(self) -> int:
        pass

if __name__ == "__main__":
    day13 = Day13()
    print(day13.part_1())
    print(day13.part_2())
