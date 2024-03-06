from overrides import override
from aoc23_base import DayBase
from enum import Enum, Flag, auto
from dataclasses import dataclass


class TileType(Enum):
    START = auto()
    GARDEN_PLOT = auto()
    ROCK = auto()

    @classmethod
    def from_str(cls, c: str) -> 'TileType':
        match c:
            case 'S':
                return cls.START
            case '.':
                return cls.GARDEN_PLOT
            case '#':
                return cls.ROCK
            case _:
                raise RuntimeError(
                    f"{cls.__class__.__name__} {c} is not recognised.")

    @classmethod
    def from_tile(cls, c: 'TileType') -> str:
        match c:
            case cls.START:
                return 'S'
            case cls.GARDEN_PLOT:
                return '.'
            case cls.ROCK:
                return '#'
            case _:
                raise RuntimeError(
                    f"{cls.__class__.__name__} {c} is not recognised.")


class PositionType(Flag):
    REACHABLE = True
    UNREACHABLE = False

    @classmethod
    def from_position(cls, c: 'PositionType') -> str:
        match c:
            case cls.REACHABLE:
                return 'O'
            case cls.UNREACHABLE:
                return '.'
            case _:
                raise RuntimeError(
                    f"{cls.__class__.__name__} {c} is not recognised.")


class MapTile:

    def __init__(self, tile_type: TileType, position_type: PositionType):
        self.tile_type: TileType = tile_type
        self.position_type: PositionType = position_type

    @classmethod
    def from_tile(cls, tile: 'MapTile') -> str:
        if tile.position_type is PositionType.REACHABLE:
            return PositionType.from_position(tile.position_type)
        return TileType.from_tile(tile.tile_type)


@dataclass(frozen=True)
class Coord:
    i: int
    j: int


class Map:

    def __init__(self, map_str: list[list[str]]):
        self.map: list[list[MapTile]] = [[]]
        for row_index, row in enumerate(map_str):
            for column_index, element in enumerate(row):
                position = PositionType.UNREACHABLE
                map_tile_type = TileType.from_str(element)
                if map_tile_type is TileType.START:
                    position = PositionType.REACHABLE
                self.map[-1].append(MapTile(map_tile_type, position))
            self.map.append([])

    def __repr__(self) -> str:
        return "\n".join("".join([MapTile.from_tile(element) for element in column]) for column in self.map)

    def take_steps(self, iterations=64) -> int:
        for _ in range(iterations):
            self.update_map_with_reachable_positions()

        return self.reachable_garden_plots

    def update_map_with_reachable_positions(self) -> None:
        new_reachable_coords: set[Coord] = set()

        for row_index, row in enumerate(self.map):
            for column_index, map_tile in enumerate(row):
                if map_tile.position_type is PositionType.REACHABLE:
                    map_tile.position_type = PositionType.UNREACHABLE

                    for row_index_offset, column_index_offset in ((0, -1), (0, 1), (1, 0), (-1, 0)):
                        new_row_index = row_index + row_index_offset
                        new_column_index = column_index + column_index_offset
                        if new_row_index in self.row_limits and new_column_index in self.column_limits \
                                and self.map[new_row_index][new_column_index].tile_type is not TileType.ROCK:

                            new_reachable_coords.add(
                                Coord(new_row_index, new_column_index))

        for coord in new_reachable_coords:
            self.map[coord.i][coord.j].position_type = PositionType.REACHABLE

    @property
    def column_limits(self) -> range:
        return range(0, len(self.map[0]))

    @property
    def row_limits(self) -> range:
        return range(0, len(self.map))

    @property
    def reachable_garden_plots(self) -> int:
        reachable_count = 0
        for row_index, row in enumerate(self.map):
            for column_index, map_tile in enumerate(row):
                if map_tile.position_type is PositionType.REACHABLE:
                    reachable_count += 1

        return reachable_count


class Day21(DayBase):

    def __init__(self):
        super().__init__()
        self.map = Map(self.parse())

    def parse(self) -> list[list[str]]:
        return [list(s) for s in self.input]

    @override
    def part_1(self) -> int:
        return self.map.take_steps(64)

    @override
    def part_2(self) -> int:
        pass


if __name__ == "__main__":
    day21 = Day21()
    print(day21.part_1())
    print(day21.part_2())
