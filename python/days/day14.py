from overrides import override
from aoc23_base import DayBase
from enum import Enum, auto
import copy
from functools import reduce

class PlatformObject(Enum):
    ROUND_ROCK = auto(),
    CUBE_ROCK = auto(),
    EMPTY_SPACE = auto(),

    @classmethod
    def from_str(cls, c: str) -> 'PlatformObject':
        match c:
            case 'O':
                return cls.ROUND_ROCK
            case '#':
                return cls.CUBE_ROCK
            case '.':
                return cls.EMPTY_SPACE
            case _:
                raise RuntimeError(f"SpringType {c} is not recognised.")
                       
    @classmethod
    def from_platform_object(cls, s: 'PlatformObject') -> str:
        match s:
            case cls.ROUND_ROCK:
                return 'O'
            case cls.CUBE_ROCK:
                return '#'
            case cls.EMPTY_SPACE:
                return '.'
            case _:
                raise RuntimeError(f"PlatformObject {s} is not recognised.")
        
    def can_move(self, other_platform_object: 'PlatformObject') -> bool:
        if self is self.ROUND_ROCK:
            match other_platform_object:
                case self.ROUND_ROCK:
                    return False
                case self.CUBE_ROCK:
                    return False
                case self.EMPTY_SPACE:
                    return True
                case _:
                    raise RuntimeError(f"Platform object {other_platform_object} is not recognised.") 
        return False
    
    @property
    def contributes_to_load(self) -> bool:
        return self.moveable
    
    @property
    def moveable(self) -> bool:
        return self is self.ROUND_ROCK

    
class ControlPlatform:

    def __init__(self, control_platform: list[list[PlatformObject]]):
        self.control_platform: list[list[PlatformObject]] = control_platform

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "\n".join("".join([PlatformObject.from_platform_object(element) for element in row]) for row in self.control_platform) + "\n" + '&' * len(self.control_platform[0])
    
    def __eq__(self, other: 'ControlPlatform') -> bool:
        return self.control_platform.__repr__() == other.control_platform.__repr__()

    @property
    def score(self) -> int:
        score = 0
        for i, row in enumerate(self.control_platform):
            for element in row:
                if element.contributes_to_load:
                    score += len(self.control_platform) - i
        return score

    def tilt(self) -> None:
        no_movement = False
        while no_movement != True:
            no_movement = True
            for i, row in enumerate(self.control_platform):
                for j, element in enumerate(row):
                    new_i = i - 1
                    if element.moveable and new_i >= 0 and element.can_move(self.control_platform[new_i][j]):
                        no_movement = False
                        self.control_platform[new_i][j], self.control_platform[i][j] =  self.control_platform[i][j], self.control_platform[new_i][j]


class Day14(DayBase):
    
    def __init__(self):
        super().__init__()

        self.control_platform = ControlPlatform([[PlatformObject.from_str(c) for c in s] for s in self.input])

    def parse(self) -> list[str]:
        return self.input

    @override
    def part_1(self) -> int:
        self.control_platform.tilt()
        return self.control_platform.score

    @override
    def part_2(self) -> int:
        pass

if __name__ == "__main__":
    day14 = Day14()
    print(day14.part_1())
    print(day14.part_2())
