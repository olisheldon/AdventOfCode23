from overrides import override
from aoc23_base import DayBase
from enum import Enum, Flag, auto
from dataclasses import dataclass


@dataclass(frozen=True)
class Coord:
    x: int
    y: int
    z: int

    @classmethod
    def get_extent(cls, coord1: 'Coord', coord2: 'Coord') -> list['Coord']:
        if coord1.x - coord2.x:
            assert coord1.y == coord2.y and coord1.z == coord2.z
            return [Coord(x, coord1.y, coord1.z) for x in range(max(coord1.x - coord2.x, coord2.x - coord1.x) + 1)]
        if coord1.y - coord2.y:
            assert coord1.x == coord2.x and coord1.z == coord2.z
            return [Coord(coord1.y, y, coord1.z) for y in range(max(coord1.y - coord2.y, coord2.y - coord1.y) + 1)]
        if coord1.z - coord2.z:
            assert coord1.x == coord2.x and coord1.y == coord2.y
            return [Coord(coord1.x, coord1.y, z) for z in range(max(coord1.z - coord2.z, coord2.z - coord1.z) + 1)]
        raise RuntimeError(f"{coord1} and {coord2} have no extent.")

    @classmethod
    def from_str(cls, brick_str: str) -> 'Coord':
        x, y, z = brick_str.split(',')
        return Coord(int(x), int(y), int(z))

    @classmethod
    def coord_below(cls, coord: 'Coord') -> 'Coord':
        return Coord(coord.x, coord.y, coord.z - 1)


class Brick:

    def __init__(self, brick_str: str):
        first_coord, second_coord = brick_str.split('~')
        self.initial_coords: list[Coord] = Coord.get_extent(
            Coord.from_str(first_coord), Coord.from_str(second_coord))


class BrickContainer:

    def __init__(self, bricks: list[str]):
        self.bricks: list[Brick] = [Brick(line) for line in bricks]
        self.occupied_coords: set[Coord] = set()
        self.brick_lookup: dict[tuple[Coord, ...], Brick] = {}
        for brick in self.bricks:
            self.brick_lookup[tuple(brick.initial_coords)] = brick
            self.occupied_coords.union(brick.initial_coords)

    def update_until_settled(self) -> None:
        old_occupied_coords = self.occupied_coords.copy()
        self._update_brick_positions()
        while self.occupied_coords != old_occupied_coords:
            old_occupied_coords = self.occupied_coords.copy()
            self._update_brick_positions()

    def _update_brick_positions(self):
        for brick_coords, brick in self.brick_lookup.items():
            if self._can_brick_move(brick_coords):
                coords_below = tuple(Coord.coord_below(brick_coord)
                                     for brick_coord in brick_coords)
                self.brick_lookup[coords_below] = brick
                self.brick_lookup.pop(brick_coords)
                self.occupied_coords = (
                    self.occupied_coords - set(brick_coords)).union(set(coords_below))
                break

    def _can_brick_move(self, brick_coords: tuple[Coord, ...]) -> bool:
        occupied_coords_except_current_brick: set[Coord] = self.occupied_coords - set(
            brick_coords)
        for new_coord in map(Coord.coord_below, brick_coords):
            if new_coord.z <= 0 or new_coord in occupied_coords_except_current_brick:
                return False
        return True


class Day22(DayBase):

    def __init__(self):
        super().__init__()
        self.brick_container = BrickContainer(self.input)

    def parse(self) -> list[str]:
        pass

    @override
    def part_1(self) -> int:
        self.brick_container.update_until_settled()

    @override
    def part_2(self) -> int:
        pass


if __name__ == "__main__":
    day22 = Day22()
    print(day22.part_1())
    print(day22.part_2())
