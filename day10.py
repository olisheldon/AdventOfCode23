from pathlib import Path
import argparse
from overrides import override
from enum import Enum, auto
from dataclasses import dataclass


@dataclass(frozen=True)
class Coord:
    i: int
    j: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.i + other.i, self.j + other.j)


class Segment(Enum):
    INSIDE = auto()
    OUTSIDE = auto()
    LOOP = auto()

    UNDETERMINED = auto()

    @classmethod
    def crossings_to_segment(cls, crossings: int) -> 'Segment':
        if crossings % 2 == 0:
            return cls.OUTSIDE
        return cls.INSIDE


class Move(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

    INVALID = auto()

    @classmethod
    def move_to_coord_offset(cls, move: 'Move') -> Coord:
        match move:
            case cls.NORTH:
                return Coord(-1, 0)
            case cls.EAST:
                return Coord(0, 1)
            case cls.SOUTH:
                return Coord(1, 0)
            case cls.WEST:
                return Coord(0, -1)
            case _:
                return Coord(0, 0)


class TileType(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()
    BENDNE = auto()
    BENDNW = auto()
    BENDSW = auto()
    BENDSE = auto()
    GROUND = auto()
    START = auto()

    @classmethod
    def from_str(cls, s: str) -> 'TileType':
        match s:
            case "|":
                return cls.VERTICAL
            case "-":
                return cls.HORIZONTAL
            case "L":
                return cls.BENDNE
            case "J":
                return cls.BENDNW
            case "7":
                return cls.BENDSW
            case "F":
                return cls.BENDSE
            case ".":
                return cls.GROUND
            case "S":
                return cls.START
            case _:
                raise RuntimeError(f"Tile type {s} is not recognised.")

    @classmethod
    def tile_type_from_moves(cls, moves: list[Move]) -> 'TileType':
        set_moves: set[Move] = set(moves)

        if set_moves == set([Move.NORTH, Move.SOUTH]):
            return cls.VERTICAL
        if set_moves == set([Move.EAST, Move.WEST]):
            return cls.HORIZONTAL
        if set_moves == set([Move.NORTH, Move.EAST]):
            return cls.BENDNE
        if set_moves == set([Move.NORTH, Move.WEST]):
            return cls.BENDNW
        if set_moves == set([Move.SOUTH, Move.WEST]):
            return cls.BENDSW
        if set_moves == set([Move.SOUTH, Move.EAST]):
            return cls.BENDSE

        raise RuntimeError(f"Can not handle moves={moves}")


class Tile:

    def __init__(self, tile_char: str, segment: Segment = Segment.UNDETERMINED):
        self.tile_type: TileType = TileType.from_str(tile_char)
        self.tile_char: str = tile_char
        self.segment: Segment = segment

    def __repr__(self) -> str:
        return self.tile_char

    def move(self, move_in: Move) -> Move:
        match self.tile_type:
            case TileType.START:
                return Move.INVALID
            case TileType.VERTICAL:
                match move_in:
                    case Move.SOUTH:
                        return Move.SOUTH
                    case Move.NORTH:
                        return Move.NORTH
                    case _:
                        return Move.INVALID
            case TileType.HORIZONTAL:
                match move_in:
                    case Move.EAST:
                        return Move.EAST
                    case Move.WEST:
                        return Move.WEST
                    case _:
                        return Move.INVALID
            case TileType.BENDNE:
                match move_in:
                    case Move.SOUTH:
                        return Move.EAST
                    case Move.WEST:
                        return Move.NORTH
                    case _:
                        return Move.INVALID
            case TileType.BENDNW:
                match move_in:
                    case Move.SOUTH:
                        return Move.WEST
                    case Move.EAST:
                        return Move.NORTH
                    case _:
                        return Move.INVALID
            case TileType.BENDSW:
                match move_in:
                    case Move.NORTH:
                        return Move.WEST
                    case Move.EAST:
                        return Move.SOUTH
                    case _:
                        return Move.INVALID
            case TileType.BENDSE:
                match move_in:
                    case Move.NORTH:
                        return Move.EAST
                    case Move.WEST:
                        return Move.SOUTH
                    case _:
                        return Move.INVALID
            case TileType.GROUND:
                raise RuntimeError(
                    f"Tile type {move_in} should not be called with {self.__class__.__name__}.")
            case _:
                raise RuntimeError(f"Tile type {move_in} not recognised.")


class Maze:

    def __init__(self, tiles: list[str]):
        self.tiles: list[list[Tile]] = []
        self.start: Coord = Coord(0, 0)
        for i in range(len(tiles)):
            self.tiles.append([])
            for j in range(len(tiles[0])):
                self.tiles[i].append(Tile(tiles[i][j]))
                if self.tiles[i][j].tile_type == TileType.START:
                    self.start = Coord(i, j)

    def __repr__(self, segment: Segment = Segment.LOOP) -> str:
        s = ""
        for row in self.tiles:
            for elem in row:
                if elem.segment is segment:
                    s += '#'
                else:
                    s += str(elem)
            s += "\n"
        return s

    def show_segment(self, segment: Segment = Segment.LOOP) -> str:
        return self.__repr__(segment)

    def get_beginning_moves(self) -> list[Move]:
        return list(move for move in Move if self.tiles[(self.start + Move.move_to_coord_offset(move)).i][(self.start + Move.move_to_coord_offset(move)).j].move(move) != Move.INVALID)

    def traverse_pipes(self) -> int:
        beginning_moves: list[Move] = self.get_beginning_moves()
        start_tile_type: TileType = TileType.tile_type_from_moves(
            beginning_moves)
        self.tiles[self.start.i][self.start.j].tile_type = start_tile_type
        self.tiles[self.start.i][self.start.j].segment = Segment.LOOP
        move = beginning_moves[0]  # pick random valid direction
        move_count = 1
        coord = self.start + Move.move_to_coord_offset(move)

        while coord != self.start:
            move = self.tiles[coord.i][coord.j].move(move)
            coord += Move.move_to_coord_offset(move)
            move_count += 1

            self.tiles[coord.i][coord.j].segment = Segment.LOOP
        return move_count

    def furthest_point(self) -> int:
        move_count = self.traverse_pipes()
        return move_count // 2 + 1 if move_count % 2 else move_count // 2

    def partition(self) -> None:
        height: int = len(self.tiles)
        width: int = len(self.tiles[0])

        for i in range(height):
            inside: bool = False
            prev_bend: TileType = TileType.GROUND
            for j in range(width):
                coord = Coord(i, j)
                tile = self.tiles[coord.i][coord.j]

                if tile.segment is Segment.LOOP:
                    if tile.tile_type is TileType.VERTICAL:
                        inside = not inside
                    elif tile.tile_type is TileType.HORIZONTAL:
                        pass
                    elif tile.tile_type in (TileType.BENDNE, TileType.BENDSE):
                        prev_bend = tile.tile_type
                    elif tile.tile_type is TileType.BENDNW:
                        if prev_bend is TileType.BENDSE:
                            inside = not inside
                    elif tile.tile_type is TileType.BENDSW:
                        if prev_bend is TileType.BENDNE:
                            inside = not inside
                    else:
                        raise RuntimeError()

                if tile.segment is not Segment.LOOP:
                    tile.segment = Segment.INSIDE if inside else Segment.OUTSIDE

    def count_segments(self, segment: Segment) -> int:
        return sum(tile.segment is segment for row in self.tiles for tile in row)


class Day10:

    def __init__(self, filepath: Path):
        self.filepath = filepath

    def parse_file(self) -> list[str]:
        with open(self.filepath, 'r', encoding="utf-8") as f:
            return f.read().splitlines()

    def parse(self) -> list[str]:
        return self.parse_file()

    def part_1(self) -> int:
        maze = Maze(self.parse_file())
        return maze.furthest_point()

    def part_2(self) -> int:
        maze = Maze(self.parse_file())
        maze.traverse_pipes()
        maze.partition()
        print([(segment, maze.count_segments(segment)) for segment in Segment])
        counts = maze.count_segments(Segment.INSIDE)

        print(maze.show_segment(Segment.INSIDE))
        print(maze.tiles[maze.start.i][maze.start.j].tile_type)
        return counts


if __name__ == "__main__":
    INPUT_FILEPATH = Path(__file__).parent / "data" / \
        f"{Path(__file__).stem}.txt"
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?',
                        default=INPUT_FILEPATH, help=f"Path to data for {Path(__file__).stem}")
    args = parser.parse_args()

    day10 = Day10(Path(args.input).absolute())
    print(day10.part_1())
    print(day10.part_2())
