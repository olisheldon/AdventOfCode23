from pathlib import Path
import argparse
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
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

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


class MirrorQueryResponse(Enum):
    SPLIT_LASERS = auto()
    NEW_POSITION = auto()
    NO_ACTION = auto()

    @classmethod
    def query(cls, mirror_tyle: 'MirrorTyle') -> 'MirrorQueryResponse':
        match mirror_tyle:
            case MirrorTyle.EMPTY_SPACE:
                return cls.NO_ACTION
            case MirrorTyle.FORWARD_MIRROR | MirrorTyle.BACKWARD_MIRROR:
                return cls.NEW_POSITION
            case MirrorTyle.VERTICAL_SPLITTER | MirrorTyle.HORIZONTAL_SPLITTER:
                return cls.SPLIT_LASERS
            case _:
                raise RuntimeError(
                    f"MirrorTyle {mirror_tyle} is not recognised.")


@dataclass(frozen=True)
class Laser:
    coord: Coord
    direction: Direction

    def move(self) -> 'Laser':
        coord_offset: Coord = Direction.move(self.direction)
        return Laser(self.coord + coord_offset, self.direction)


class MirrorTyle(Enum):
    EMPTY_SPACE = auto()
    FORWARD_MIRROR = auto()
    BACKWARD_MIRROR = auto()
    VERTICAL_SPLITTER = auto()
    HORIZONTAL_SPLITTER = auto()

    @classmethod
    def from_str(cls, c: str) -> 'MirrorTyle':
        match c:
            case '.':
                return cls.EMPTY_SPACE
            case '/':
                return cls.FORWARD_MIRROR
            case '\\':
                return cls.BACKWARD_MIRROR
            case '|':
                return cls.VERTICAL_SPLITTER
            case '-':
                return cls.HORIZONTAL_SPLITTER
            case _:
                raise RuntimeError(f"MirrorTyle {c} is not recognised.")

    @classmethod
    def from_mirror_tyle(cls, s: 'MirrorTyle') -> str:
        match s:
            case cls.EMPTY_SPACE:
                return '.'
            case cls.FORWARD_MIRROR:
                return '/'
            case cls.BACKWARD_MIRROR:
                return '\\'
            case cls.VERTICAL_SPLITTER:
                return '|'
            case cls.HORIZONTAL_SPLITTER:
                return '-'
            case _:
                raise RuntimeError(f"MirrorTyle {s} is not recognised.")

    @classmethod
    def query(cls, mirror_tyle: 'MirrorTyle', direction: Direction) -> list[Direction]:
        directions = []
        match mirror_tyle:
            case cls.EMPTY_SPACE:
                directions = [direction]
            case cls.FORWARD_MIRROR:
                match direction:
                    case Direction.NORTH:
                        directions = [Direction.EAST]
                    case Direction.EAST:
                        directions = [Direction.NORTH]
                    case Direction.SOUTH:
                        directions = [Direction.WEST]
                    case Direction.WEST:
                        directions = [Direction.SOUTH]
            case cls.BACKWARD_MIRROR:
                match direction:
                    case Direction.NORTH:
                        directions = [Direction.WEST]
                    case Direction.EAST:
                        directions = [Direction.SOUTH]
                    case Direction.SOUTH:
                        directions = [Direction.EAST]
                    case Direction.WEST:
                        directions = [Direction.NORTH]
            case cls.HORIZONTAL_SPLITTER:
                match direction:
                    case Direction.NORTH | Direction.SOUTH:
                        directions = [Direction.WEST, Direction.EAST]
                    case Direction.EAST:
                        directions = [Direction.EAST]
                    case Direction.WEST:
                        directions = [Direction.WEST]
            case cls.VERTICAL_SPLITTER:
                match direction:
                    case Direction.EAST | Direction.WEST:
                        directions = [Direction.NORTH, Direction.SOUTH]
                    case Direction.SOUTH:
                        directions = [Direction.SOUTH]
                    case Direction.NORTH:
                        directions = [Direction.NORTH]
            case _:
                raise RuntimeError(
                    f"MirrorTyle {mirror_tyle} should not use {__class__}.")
        return directions


class Mirror:

    def __init__(self, mirror: list[list[str]], lasers: list[Laser] = [Laser(Coord(0, 0), Direction.EAST)]):
        self.mirror: list[list[MirrorTyle]] = list(
            list(MirrorTyle.from_str(tyle) for tyle in row) for row in mirror)
        self.lasers: list[Laser] = lasers

    def _valid_coord(self, coord: Coord) -> bool:
        return 0 <= coord.i < len(self.mirror) and 0 <= coord.j < len(self.mirror[0])

    def shoot_laser(self) -> int:
        laser_states: set[Laser] = set()

        while self.lasers:
            laser = self.lasers.pop()
            if laser not in laser_states:
                laser_states.add(laser)
                directions = MirrorTyle.query(
                    self.mirror[laser.coord.i][laser.coord.j], laser.direction)
                for direction in directions:
                    new_laser = Laser(
                        laser.coord + Direction.move(direction), direction)
                    if self._valid_coord(new_laser.coord):
                        self.lasers.append(new_laser)

        return len(set(laser_state.coord for laser_state in laser_states))


class Day16:

    def __init__(self, filepath: Path):
        self.filepath = filepath

    def parse_file(self) -> list[str]:
        with open(self.filepath, 'r', encoding="utf-8") as f:
            return f.read().splitlines()

    def part_1(self) -> int:
        mirror = Mirror([[c for c in line] for line in self.parse_file()])
        return mirror.shoot_laser()

    def part_2(self) -> int:
        min_i, max_i = 0, len(self.parse_file()) - 1
        min_j, max_j = 0, len(self.parse_file()[0]) - 1
        lasers_going_north = [
            Laser(Coord(max_i, j), Direction.NORTH) for j in range(max_j + 1)]
        lasers_going_east = [Laser(Coord(i, min_j), Direction.EAST)
                             for i in range(max_i + 1)]
        lasers_going_south = [
            Laser(Coord(min_i, j), Direction.SOUTH) for j in range(max_j + 1)]
        lasers_going_west = [Laser(Coord(i, max_j), Direction.WEST)
                             for i in range(max_i + 1)]
        return max(Mirror([[c for c in line] for line in self.parse_file()], [laser]).shoot_laser() for laser in lasers_going_north +
                   lasers_going_east +
                   lasers_going_south +
                   lasers_going_west
                   )


if __name__ == "__main__":
    INPUT_FILEPATH = Path(__file__).parent / "data" / \
        f"{Path(__file__).stem}.txt"
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?',
                        default=INPUT_FILEPATH, help=f"Path to data for {Path(__file__).stem}")
    args = parser.parse_args()

    day16 = Day16(Path(args.input).absolute())
    print(day16.part_1())
    print(day16.part_2())
