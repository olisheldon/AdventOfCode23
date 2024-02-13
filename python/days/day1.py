import string
from overrides import override
from enum import Enum, auto
from aoc23_base import DayBase

class ParseType(Enum):
    DIGITS = auto()
    DIGITS_AND_STRINGS = auto()

class CalibrationLine:

    STRING_TO_DIGIT: dict[str, int] = {
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

    def __init__(self, line: str):
        self.line = line

    def parse_edge_digits(self, parse_type: ParseType) -> tuple[int, int]:
        match parse_type:
            case ParseType.DIGITS:
                return self._parse_edge_digits_only()
            case ParseType.DIGITS_AND_STRINGS:
                return self._parse_edge_digits_and_strings()
            case _:
                raise RuntimeError(f"ParseType {parse_type} is not recognised.")
    
    def _parse_edge_digits_only(self) -> tuple[int, int]:
        left_edge_value, right_edge_value = -1, -1

        for l in range(len(self.line)):
            if self.line[l] in string.digits:
                left_edge_value = int(self.line[l])
                break

        for r in range(len(self.line) - 1, -1, -1):
            if self.line[r] in string.digits:
                right_edge_value = int(self.line[r])
                break

        assert left_edge_value > 0 and right_edge_value > 0
        return left_edge_value, right_edge_value
    
    def _parse_edge_digits_and_strings(self) -> tuple[int, int]:
        left_edge_value, right_edge_value = -1, -1

        for l in range(len(self.line)):
            if self.line[l] in string.digits:
                left_edge_value = int(self.line[l])
            for key, val in CalibrationLine.STRING_TO_DIGIT.items():
                if key in self.line[ : l]:
                    left_edge_value = val
            
            if left_edge_value >= 0:
                break

        for r in range(len(self.line) - 1, -1, -1):
            if self.line[r] in string.digits:
                right_edge_value = int(self.line[r])
            for key, val in CalibrationLine.STRING_TO_DIGIT.items():
                if key in self.line[r : ]:
                    right_edge_value = val
            
            if right_edge_value >= 0:
                break

        assert left_edge_value > 0 and right_edge_value > 0
        return left_edge_value, right_edge_value
    
    def calibration_value(self, parse_type: ParseType = ParseType.DIGITS) -> int:
        left_edge_value, right_edge_value = self.parse_edge_digits(parse_type)
        return 10 * left_edge_value + right_edge_value

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
    