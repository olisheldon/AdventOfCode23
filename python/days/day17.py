from overrides import override
from aoc23_base import DayBase
from enum import StrEnum, auto
from dataclasses import dataclass, field
from heapq import heappush, heappop

@dataclass(frozen=True, order=True)
class Coord:
    i: int
    j: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.i + other.i, self.j + other.j)

class Direction(StrEnum):
    NORTH = auto()
    WEST = auto()
    SOUTH = auto()
    EAST = auto()

    @classmethod
    def move(cls, direction: 'Direction') -> Coord:
        match direction:
            case cls.NORTH:
                return Coord(-1, 0)
            case cls.EAST:
                return Coord(0, 1)
            case cls.SOUTH:
                return Coord(1, 0)
            case cls.WEST:
                return Coord(0, -1)
            case _:
                raise RuntimeError(f"Direction {direction} is not recognised.")

    @classmethod
    def reverse(cls, direction: 'Direction') -> 'Direction':
        match direction:
            case cls.NORTH:
                return cls.SOUTH
            case cls.EAST:
                return cls.WEST
            case cls.SOUTH:
                return cls.NORTH
            case cls.WEST:
                return cls.EAST
            case _:
                raise RuntimeError(f"Direction {direction} is not recognised.")

@dataclass(frozen=True, order=True)
class CrucibleState:
    coord: Coord
    direction: Direction
    steps_in_direction: int

class City:

    def __init__(self, heat_losses: list[list[int]]):
        self.grid = heat_losses
    
    def minimum_heat_loss(self, start: Coord = Coord(0, 0), end: Coord | None = None) -> int:
        
        if end is None:
            end = Coord(len(self.grid) - 1, len(self.grid[0]) - 1)

        initial_crucible_states: list[tuple[int, CrucibleState]] = [(0, CrucibleState(start, direction, 0)) for direction in Direction]

        priority_queue: list[tuple[int, CrucibleState]] = initial_crucible_states
        visit: set[CrucibleState] = set()

        while priority_queue:
            for _ in range(len(priority_queue)):

                heat_loss_accum, crucible_state = heappop(priority_queue)

                if crucible_state.coord == end:
                    return heat_loss_accum

                if crucible_state in visit:
                    continue
                
                visit.add(crucible_state)

                directions = [direction for direction in Direction]
                for next_direction in directions:

                    if next_direction is Direction.reverse(crucible_state.direction):
                        continue

                    next_coord = crucible_state.coord + Direction.move(next_direction)
                    if not self._within_boundary(next_coord):
                        continue

                    if next_direction is crucible_state.direction and crucible_state.steps_in_direction >= 3:
                        continue

                    next_steps_in_direction = crucible_state.steps_in_direction + 1 if next_direction is crucible_state.direction else 1
                    next_heat_loss_accum = self.grid[next_coord.i][next_coord.j] + heat_loss_accum
                    next_crucible_state = (next_heat_loss_accum, CrucibleState(next_coord, next_direction, next_steps_in_direction))
                    
                    heappush(priority_queue, next_crucible_state)
        return -1

    def _within_boundary(self, coord: Coord) -> bool:
        return (0 <= coord.i < len(self.grid)
           and 0 <= coord.j < len(self.grid[0]))

class Day17(DayBase):
    
    def __init__(self):
        super().__init__()
        self.city: City = City(self.parse())

    def parse(self) -> list[list[int]]:
        return [[int(heat_loss) for heat_loss in line] for line in self.input]

    @override
    def part_1(self) -> int:
        return self.city.minimum_heat_loss()

    @override
    def part_2(self) -> int:
        pass

if __name__ == "__main__":
    day17 = Day17()
    print(day17.part_1())
    print(day17.part_2())
