import string

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
    
    def __init__(self, coord: tuple[int, int]):
        self.coord = coord

class Day3:

    def __init__(self):
        self.input: list[str] = Day3.get_input()

    @staticmethod
    def get_input() -> list[str]:
        with open("input.txt", 'r') as f:
            lines = f.read().splitlines()
        return lines
    
    def part1(self) -> int:
        numbers, symbols = self.parse()

        symbols_coords = [symbol.coord for symbol in symbols]
        i = 0
        for number in numbers:
            for symbol_coord in symbols_coords:
                if number.within_boundary(symbol_coord):
                    i += number.num
                    break
        return i
        

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
                    symbols.append(Symbol((line_num, i)))
                    i += 1
                else:
                    i += 1
        return numbers, symbols
                

    
if __name__ == "__main__":
    day3 = Day3()
    print(day3.part1())
