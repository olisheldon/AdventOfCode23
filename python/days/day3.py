import string
from functools import reduce

class Number:
    
    def __init__(self, num: int, boundary_right: int, line_num: int):
        self.num = num
        self.boundary_coordinates: set = self.create_boundary(boundary_right - len(str(num)) - 1, boundary_right, line_num)

    def create_boundary(self, boundary_left: int, boundary_right: int, line_num: int) -> set[tuple[int, int]]:
        boundary = set()
        for i in range(line_num - 1, line_num + 2):
            for j in range(boundary_left, boundary_right + 1):

                boundary.add((i, j))
        return boundary
    
    def within_boundary(self, coord: tuple[int, int]) -> bool:
        return coord in self.boundary_coordinates

class Symbol:
    
    def __init__(self, coord: tuple[int, int], symbol: str):
        self.coord = coord
        self.symbol = symbol

    @property
    def is_gear(self) -> bool:
        return self.symbol == '*'

class Day3:

    def __init__(self):
        self.input: list[str] = Day3.get_input()
        self.numbers, self.symbols = self.parse()

    @staticmethod
    def get_input() -> list[str]:
        with open("input.txt", 'r') as f:
            lines = f.read().splitlines()
        return lines
    
    def part1(self) -> int:
        i = 0
        for number in self.numbers:
            for symbol in self.symbols:
                if number.within_boundary(symbol.coord):
                    i += number.num
                    break
        return i
    
    def part2(self) -> int:
        result = 0
        for symbol in self.symbols:
            if symbol.is_gear:
                number_count = 0
                number_vals = []
                for number in self.numbers:
                    if number.within_boundary(symbol.coord):
                        number_count += 1
                        number_vals.append(number.num)
                if number_count == 2:
                    result += reduce((lambda x, y: x * y), number_vals)
        return result

    def parse(self) -> tuple[list[Number], list[Symbol]]:
        numbers = []
        symbols = []
        for line_num, line in enumerate(self.input):
            i = 0
            while i < len(line):
                if line[i] in string.digits:
                    num_str = ""
                    while i < len(line) and line[i] in string.digits:
                        num_str += line[i]
                        i += 1
                    numbers.append(Number(int(num_str), i, line_num))
                elif line[i] != '.':
                    symbols.append(Symbol((line_num, i), line[i]))
                    i += 1
                else:
                    i += 1
        return numbers, symbols
                

    
if __name__ == "__main__":
    day3 = Day3()
    print(day3.part1())
    print(day3.part2())
