from overrides import override
from aoc23_base import DayBase
from enum import Enum, StrEnum, auto
from dataclasses import dataclass

class GroundType(Enum):
    TRENCH = auto(),
    GROUND = auto(),

@dataclass(frozen=True)
class Coord:
    i: int
    j: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.i + other.i, self.j + other.j)

class Direction(StrEnum):
    U = auto(),
    R = auto(),
    D = auto(),
    L = auto(),

    @classmethod
    def move(cls, direction: 'Direction') -> Coord:
        match direction:
            case cls.U:
                return Coord(-1, 0)
            case cls.R:
                return Coord(0, 1)
            case cls.D:
                return Coord(1, 0)
            case cls.L:
                return Coord(0, -1)
            case _:
                raise RuntimeError(f"Direction {direction} is not recognised.")
        
@dataclass
class Instruction:
    direction: Direction
    length: int
    colour: str

class FillingState(Enum):
    INSIDE = auto(),
    OUTSIDE = auto(),

class Frame:

    def __init__(self):
        self.boundary_coords: dict[Coord, str] = {}

    def create_outline(self, instructions: list[Instruction]):
        coord = Coord(0, 0)
        for instruction in instructions:
            coord = self._apply_instruction(instruction, coord)

    def _apply_instruction(self, instruction: Instruction, coord: Coord) -> Coord:
        for _ in range(instruction.length):
            self.boundary_coords[coord] = instruction.colour
            coord = coord + Direction.move(instruction.direction)
        return coord
    
    # def calculate_area(self) -> int:
    #     fill_coords_including_outline: set[Coord] = set(self.boundary_coords.keys())
    #     min_j_for_each_i: dict[int, int] = {}
    #     max_j_for_each_i: dict[int, int] = {}
    #     for coord in self.boundary_coords:
    #         if coord.i in min_j_for_each_i:
    #             min_j_for_each_i[coord.i] = min(min_j_for_each_i[coord.i], coord.j)
    #         else:
    #             min_j_for_each_i[coord.i] = coord.j
    #         if coord.i in max_j_for_each_i:
    #             max_j_for_each_i[coord.i] = max(max_j_for_each_i[coord.i], coord.j)
    #         else:
    #             max_j_for_each_i[coord.i] = coord.j
        
    #     for i in min_j_for_each_i:
    #         j = min_j_for_each_i[i]
    #         while j != max_j_for_each_i[i]:
    #             j += 1
    #             if Coord(i - 1, j) in fill_coords_including_outline:
    #                 fill_coords_including_outline.add(Coord(i, j))

    #     return len(fill_coords_including_outline)
    
    # def calculate_area(self) -> int:
    #     fill_coords_including_outline: set[Coord] = set(self.boundary_coords.keys())
    #     min_j_for_each_i: dict[int, int] = {}
    #     max_j_for_each_i: dict[int, int] = {}

    #     for coord in self.boundary_coords:
    #         if coord.i in min_j_for_each_i:
    #             min_j_for_each_i[coord.i] = min(min_j_for_each_i[coord.i], coord.j)
    #         else:
    #             min_j_for_each_i[coord.i] = coord.j
    #         if coord.i in max_j_for_each_i:
    #             max_j_for_each_i[coord.i] = max(max_j_for_each_i[coord.i], coord.j)
    #         else:
    #             max_j_for_each_i[coord.i] = coord.j
        
    #     for i in sorted(min_j_for_each_i.keys()):
    #         print(i)
    #         j = min_j_for_each_i[i]
    #         while j != max_j_for_each_i[i]:
    #             j += 1
    #             if Coord(i, j) not in self.boundary_coords and Coord(i - 1, j) in fill_coords_including_outline:
    #                 fill_coords_including_outline.add(Coord(i, j))

    #     return len(fill_coords_including_outline)
    
    def calculate_area(self) -> int:
        fill_coords_including_outline: set[Coord] = set(self.boundary_coords.keys())
        min_j_for_each_i: dict[int, int] = {}
        max_j_for_each_i: dict[int, int] = {}

        for coord in self.boundary_coords:
            if coord.i in min_j_for_each_i:
                min_j_for_each_i[coord.i] = min(min_j_for_each_i[coord.i], coord.j)
            else:
                min_j_for_each_i[coord.i] = coord.j
            if coord.i in max_j_for_each_i:
                max_j_for_each_i[coord.i] = max(max_j_for_each_i[coord.i], coord.j)
            else:
                max_j_for_each_i[coord.i] = coord.j
        
        for i in sorted(min_j_for_each_i.keys()):
            boundary_count = 0
            j = min_j_for_each_i[i]
            while j != max_j_for_each_i[i]:
                curr_coord = Coord(i, j)
                next_coord = Coord(i, j + 1)
                prev_coord = Coord(i, j - 1)

                if curr_coord in self.boundary_coords and next_coord not in self.boundary_coords:
                    boundary_count += 1

                

                if boundary_count % 2:
                    fill_coords_including_outline.add(curr_coord)
                
                if curr_coord not in self.boundary_coords:
                    print(i, j, boundary_count % 2)

                j += 1
        return len(fill_coords_including_outline)

class Day18(DayBase):
    
    def __init__(self):
        super().__init__()
        self.instructions: list[Instruction] = self.parse()
        self.frame = Frame()

    def parse(self) -> list[Instruction]:
        instructions: list[Instruction] = []
        for line in self.input:
            split_line = line.split()
            instruction = Instruction(Direction[split_line[0]], int(split_line[1]), split_line[-1][2:-1])
            instructions.append(instruction)
        return instructions

    @override
    def part_1(self) -> int:
        self.frame.create_outline(self.instructions)
        # for coord in self.frame.coords:
        #     print(coord)
        return self.frame.calculate_area()

    @override
    def part_2(self) -> int:
        pass

if __name__ == "__main__":
    day18 = Day18()
    print(day18.part_1())
    print(day18.part_2())
