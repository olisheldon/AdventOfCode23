import string
import sys


class Day1:

    char_string_map = {"one"   : 1,
                       "two"   : 2,
                       "three" : 3,
                       "four"  : 4,
                       "five"  : 5,
                       "six"   : 6,
                       "seven" : 7,
                       "eight" : 8,
                       "nine"  : 9,
                       }
    min_char_string_length = min([len(key) for key in char_string_map])
    max_char_string_length = max([len(key) for key in char_string_map])

    inverse_char_string_map = {k[::-1] : v for k, v in char_string_map.items()}

    def __init__(self):
        self.input = Day1.get_input()

    def part_1(self) -> int:
        lines = Day1.preprocess_strings(self.input, Day1.string_preprocessing_part_1)
        return Day1.handle_boundary_integers(lines)
    
    def part_2(self) -> int:
        lines = Day1.preprocess_strings(self.input, Day1.string_preprocessing_part_2)
        return Day1.handle_boundary_integers(lines)

    @staticmethod
    def handle_boundary_integers(lines: list[list[int]]) -> int:
        assert len(lines) >= 1 and all(all((type(item) == int) for item in line) for line in lines)
        value = 0
        for line in lines:
            value += 10 * line[0] + line[-1]
        return value
    
    @staticmethod
    def preprocess_strings(lines: list[str], method) -> list[list[int]]:
        new_lines = []
        for line in lines:
            new_lines.append(method(line))
        return new_lines
    
    @staticmethod
    def string_preprocessing_part_1(line: str) -> list[list[int]]:
        new_line = []
        for c in line:
            if c.isdigit():
                new_line.append(int(c))
        return new_line
    
    @staticmethod
    def string_preprocessing_part_2(line: str) -> list[int]:
        new_line = []
        l = 0
        while l < len(line):
            if line[l] in string.digits:
                new_line.append(int(line[l]))
            else:
                answer = Day1.isStringRangeValid(line, l)
                if answer:
                    new_line.append(answer)
            l += 1
        return new_line
    
    @staticmethod
    def isStringRangeValid(line, l):
        r = l + Day1.min_char_string_length
        while r - l <= Day1.max_char_string_length and r < len(line) + 1:
            if line[l:r] in Day1.char_string_map:
                return Day1.char_string_map[line[l:r]]
            r += 1
        return 0

    @staticmethod
    def get_input() -> list[str]:
        with open("input.txt", 'r') as f:
            lines = f.read().splitlines()
        return lines

if __name__ == "__main__":

    day1 = Day1()

    print("Python Solution:")
    print(f"\tPart 1: {day1.part_1()}")
    print(f"\tPart 2: {day1.part_2()}")
    