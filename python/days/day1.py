import string
from overrides import override
from enum import Enum, auto
from aoc23_base import DayBase

class ParseType(Enum):
    DIGITS = auto()
    STRINGS = auto()
    DIGITS_AND_STRINGS = auto()

    @classmethod
    def get_string_interpret(cls, parse_type: 'ParseType') -> dict[str, int]:
        match parse_type:
            case cls.DIGITS:
                return {str(d) : int(d) for d in string.digits}
            case cls.STRINGS:
                return {
                    "one"   : 1,
                    "two"   : 2,
                    "three" : 3,
                    "four"  : 4,
                    "five"  : 5,
                    "six"   : 6,
                    "seven" : 7,
                    "eight" : 8,
                    "nine"  : 9,
                }
            case cls.DIGITS_AND_STRINGS:
                return cls.get_string_interpret(cls.DIGITS) | cls.get_string_interpret(cls.STRINGS)
            case _:
                raise RuntimeError(f"ParseType {parse_type} is not recognised.")

class CalibrationLine:

    def __init__(self, line: str):
        self.line = line
    
    def calibration_value(self, parse_type: ParseType = ParseType.DIGITS) -> int:
        left_edge_value, right_edge_value = self._parse_boundary(parse_type)
        return 10 * left_edge_value + right_edge_value

    def _parse_boundary(self, parse_type) -> tuple[int, int]:
        string_interpret: dict[str, int] = ParseType.get_string_interpret(parse_type)
        left_edge_value, right_edge_value = self._parse(self.line, string_interpret), self._parse(self.line[::-1], {k[::-1] : v for k, v in string_interpret.items()})
        assert left_edge_value > -1 and right_edge_value > -1
        return left_edge_value, right_edge_value

    @staticmethod
    def _parse(line: str, string_interpret: dict[str, int]) -> int:
        for l in range(1, len(line) + 1):
            for key, val in string_interpret.items():
                if key in line[ : l]:
                    return val
        return -1

class Day1(DayBase):
    
    def __init__(self):
        super().__init__()
        self.calibration_lines = self.parse()

    def parse(self) -> list[CalibrationLine]:
        return [CalibrationLine(line) for line in self.input]

    @override
    def part_1(self) -> int:
        return sum(calibration_line.calibration_value(parse_type=ParseType.DIGITS) for calibration_line in self.calibration_lines)

    @override
    def part_2(self) -> int:
        return sum(calibration_line.calibration_value(parse_type=ParseType.DIGITS_AND_STRINGS) for calibration_line in self.calibration_lines)

if __name__ == "__main__":
    day1 = Day1()
    print(day1.part_1())
    print(day1.part_2())
    