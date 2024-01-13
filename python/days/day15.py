from overrides import override

from aoc23_base import DayBase
from enum import Enum, auto
from dataclasses import dataclass

class Hasher:

    @staticmethod
    def hash(s: str) -> int:
        # Determine the ASCII code for the current character of the string.
        # Increase the current value by the ASCII code you just determined.
        # Set the current value to itself multiplied by 17.
        # Set the current value to the remainder of dividing itself by 256.
        current_value = 0
        for c in s:
            ascii_value = ord(c)
            current_value += ascii_value
            current_value *= 17
            current_value %= 256
        return current_value





class Day15(DayBase):
    
    def __init__(self):
        super().__init__()

    def parse(self) -> list[str]:
        return self.input[0].split(',')

    @override
    def part_1(self) -> int:
        return sum(Hasher.hash(s) for s in self.parse())
        

    @override
    def part_2(self) -> int:
        pass


if __name__ == "__main__":
    day15 = Day15()
    print(day15.part_1())
    print(day15.part_2())
