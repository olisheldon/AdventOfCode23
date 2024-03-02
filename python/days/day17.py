from overrides import override
from aoc23_base import DayBase
from collections import deque
from enum import Enum, auto
from dataclasses import dataclass

@dataclass(frozen=True)
class Coord:
    i: int
    j: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.i + other.i, self.j + other.j)

class Direction(Enum):
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

@dataclass(frozen=True)
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

        initial_crucible_states: list[CrucibleState] = [CrucibleState(start, direction, 1) for direction in Direction]

        queue: deque[CrucibleState] = deque(initial_crucible_states)
        visit: set[CrucibleState] = set(initial_crucible_states)

        heat_loss: int = 0
        directions = [direction for direction in Direction]
        while queue:
            for _ in range(len(queue)):
                crucible_state = queue.popleft()

                if crucible_state.coord == end:
                    return heat_loss
                
                for next_direction in directions:
                    next_coord = crucible_state.coord + Direction.move(next_direction)
                    next_steps_in_direction = crucible_state.steps_in_direction + 1 if next_direction is crucible_state.direction else 1
                    next_crucible_state = CrucibleState(next_coord, next_direction, next_steps_in_direction)
                    if (not self._within_boundary(next_coord) or
                        (next_direction is crucible_state.direction and crucible_state.steps_in_direction > 2) or
                        (next_crucible_state in visit)):
                        continue
                    
                    queue.append(next_crucible_state)
                    visit.add(crucible_state)

    def _within_boundary(self, coord: Coord) -> bool:
        return 0 <= coord.i < len(self.grid) \
           and 0 <= coord.j < len(self.grid[0])

    def _too_many_steps(self, ) -> bool:
        return 

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
