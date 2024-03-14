from overrides import override
from aoc23_base import DayBase
from enum import StrEnum, auto
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Coord:
    i: int
    j: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.i + other.i, self.j + other.j)

    def __mul__(self, other) -> 'Coord':

        if isinstance(other, int):
            return self.__class__(other * self.i, other * self.j)

        raise RuntimeError(
            f"{self.__class__.__name__} does not support multiplication by {type(other)}")

    def __rmul__(self, other) -> 'Coord':

        return self.__mul__(other)


class Direction(StrEnum):
    U = auto()
    R = auto()
    D = auto()
    L = auto()

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
class ColourMixin:
    colour: str


@dataclass
class Instruction:
    direction: Direction
    steps: int


@dataclass
class DigPlan(ColourMixin, Instruction):
    pass


@dataclass
class ColourCorrection(ColourMixin, Instruction):

    def __post_init__(self):
        self.steps = int(self.colour[:-1], base=16)
        ending_colour = self.colour[-1]
        match ending_colour:
            case '0':
                direction = Direction.R
            case '1':
                direction = Direction.D
            case '2':
                direction = Direction.L
            case '3':
                direction = Direction.U
            case _:
                raise RuntimeError(
                    f"{self.__class__.__name__} ending digit {ending_colour} is not recognised.")
        self.direction = direction


class Frame:

    def __init__(self, instructions: Sequence[Instruction]):
        self.instructions = instructions

    def _create_vertex_coords(self) -> list[Coord]:
        coord = Coord(0, 0)
        vertex_coords: list[Coord] = [coord]
        for instr in self.instructions:
            coord = coord + instr.steps * Direction.move(instr.direction)
            vertex_coords.append(coord)
        return vertex_coords

    def _polygon_area(self) -> int:
        vertex_coords = self._create_vertex_coords()
        polygon_area = 0
        for i, curr_vertex in enumerate(vertex_coords):
            prev_vertex = vertex_coords[i - 1]
            next_vertex = vertex_coords[(i + 1) % len(vertex_coords)]
            polygon_area += curr_vertex.i * (prev_vertex.j - next_vertex.j)
        return abs(polygon_area) // 2

    def calculate_area(self) -> int:
        '''
        Using Pick's theorem to calculate area from vertex coordinates
        '''
        polygon_area = self._polygon_area()
        boundary_area = sum(instr.steps for instr in self.instructions)
        interior_area = polygon_area - boundary_area // 2 + 1
        return interior_area + boundary_area


class Day18(DayBase):

    def __init__(self):
        super().__init__()
        self.dig_plans: list[DigPlan] = self.parse()

    def parse(self) -> list[DigPlan]:
        dig_plans: list[DigPlan] = []
        for line in self.input:
            split_line = line.split()
            dig_plan = DigPlan(Direction[split_line[0]], int(
                split_line[1]), split_line[-1][2:-1])
            dig_plans.append(dig_plan)
        return dig_plans

    @override
    def part_1(self) -> int:
        frame = Frame(self.dig_plans)
        return frame.calculate_area()

    @override
    def part_2(self) -> int:
        instructions = [ColourCorrection(dig_plan.direction, dig_plan.steps,
                                         dig_plan.colour) for dig_plan in self.dig_plans]
        frame = Frame(instructions)
        return frame.calculate_area()


if __name__ == "__main__":
    day18 = Day18()
    print(day18.part_1())
    print(day18.part_2())
