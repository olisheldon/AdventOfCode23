from overrides import override
from aoc23_base import DayBase
from enum import Enum, auto

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
    
    def combinations(self) -> int:
        return self._combinations(self, 0, self.configuration, 0)
    
    def _combinations(self, springs: 'Row', l: int, counts: list[int], combos: int) -> int:
        if not counts and l == len(springs.springs) - 1:
            return 1
        if not counts and any(spring is SpringType.UNKNOWN for spring in self.springs):
            return 0

        while l < len(springs.springs):
            if springs.springs[l] is SpringType.UNKNOWN:
                springs_with_damaged_at_l = Row(springs.springs.copy(), self.configuration)
                springs_with_damaged_at_l.springs[l] = SpringType.DAMAGED
                springs_with_operational_at_l = Row(springs.springs.copy(), self.configuration)
                springs_with_operational_at_l.springs[l] = SpringType.OPERATIONAL
                combos += self._combinations(springs_with_damaged_at_l, l, counts, combos)
                combos += self._combinations(springs_with_operational_at_l, l, counts, combos)
            elif springs.springs[l] is SpringType.OPERATIONAL:
                combos += self._combinations(self, l + 1, counts, combos)
            elif springs.springs[l] is SpringType.DAMAGED:
                if springs.all_operational_in_range(l - counts[0], l + 1):
                    counts.pop(0)
                    combos += self._combinations(self, l + 1, counts, combos)
                else:
                    combos += self._combinations(self, l + 1, counts, combos)
        return combos
    
    def all_operational_in_range(self, l: int, r: int) -> bool:
        if l < 0 or r > len(self.springs):
            return False
        return all(spring is SpringType.OPERATIONAL for spring in self.springs[l: r])

class Field:

    def __init__(self, input: list[str]):
        self.rows: list[Row] = Field.create_field(input)

    @classmethod
    def create_field(cls, input: list[str]) -> list[Row]:
        res: list[Row] = []
        for line in input:
            springs, spring_lengths = line.split()
            res.append(Row([SpringType.from_str(spring) for spring in springs], [int(spring_length) for spring_length in spring_lengths.split(',')]))
        return res
            

class Day12(DayBase):
    
    def __init__(self):
        super().__init__()
        self.field = Field(self.input)

    def parse(self):
        pass

    @override
    def part_1(self) -> int:
        return self.field.rows[0].combinations()

    @override
    def part_2(self) -> int:
        pass

if __name__ == "__main__":
    day12 = Day12()
    print(day12.part_1())
    print(day12.part_2())
