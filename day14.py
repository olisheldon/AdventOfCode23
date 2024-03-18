from pathlib import Path
import argparse
from enum import Enum, auto


class PlatformObject(Enum):
    ROUND_ROCK = auto()
    CUBE_ROCK = auto()
    EMPTY_SPACE = auto()

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
                    raise RuntimeError(
                        f"Platform object {other_platform_object} is not recognised.")
        return False

    @property
    def contributes_to_load(self) -> bool:
        return self.moveable

    @property
    def moveable(self) -> bool:
        return self is PlatformObject.ROUND_ROCK


class Direction(Enum):
    NORTH = auto()
    WEST = auto()
    SOUTH = auto()
    EAST = auto()


class ControlPlatform:

    def __init__(self, control_platform: tuple[tuple[PlatformObject, ...], ...]):
        self.control_platform: tuple[tuple[PlatformObject, ...], ...] = control_platform
        self.cache: dict[tuple[tuple[PlatformObject, ...], ...],
                         tuple[tuple[PlatformObject, ...], ...]] = {}

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "\n".join("".join([PlatformObject.from_platform_object(element) for element in row]) for row in self.control_platform) + "\n" + '&' * len(self.control_platform[0])

    @staticmethod
    def create_control_platform(control_platform: list[list[PlatformObject]]) -> 'ControlPlatform':
        return ControlPlatform(tuple(tuple(row) for row in control_platform))

    @property
    def score(self) -> int:
        score = 0
        for i, row in enumerate(self.control_platform):
            for element in row:
                if element.contributes_to_load:
                    score += len(self.control_platform) - i
        return score

    def tilt(self, direction: Direction = Direction.NORTH) -> None:

        match direction:
            case Direction.NORTH:
                self._tilt_north()
            case Direction.SOUTH:
                self._tilt_south()
            case Direction.EAST:
                self._tilt_east()
            case Direction.WEST:
                self._tilt_west()

    def _tilt_north(self) -> None:
        control_platform = list(list(control_platform)
                                for control_platform in self.control_platform)
        for i, row in enumerate(control_platform):
            for j, element in enumerate(row):
                new_i = i - 1
                if element.moveable:
                    while new_i >= 0 and element.can_move(control_platform[new_i][j]):
                        new_i -= 1
                new_i = new_i + 1
                if element.can_move(control_platform[new_i][j]):
                    control_platform[new_i][j] = control_platform[i][j]
                    control_platform[i][j] = PlatformObject.EMPTY_SPACE
        self.control_platform = tuple(tuple(row) for row in control_platform)

    def _tilt_south(self) -> None:
        control_platform = list(list(control_platform)
                                for control_platform in self.control_platform)
        for i, row in enumerate(control_platform[::-1]):
            i = len(control_platform) - 1 - i
            for j, element in enumerate(row):
                new_i = i + 1
                if element.moveable:
                    while new_i < len(control_platform) and element.can_move(control_platform[new_i][j]):
                        new_i += 1
                new_i = new_i - 1
                if element.can_move(control_platform[new_i][j]):
                    control_platform[new_i][j] = control_platform[i][j]
                    control_platform[i][j] = PlatformObject.EMPTY_SPACE
        self.control_platform = tuple(tuple(row) for row in control_platform)

    def _tilt_west(self) -> None:
        control_platform = list(list(control_platform)
                                for control_platform in self.control_platform)
        for i, row in enumerate(control_platform):
            for j, element in enumerate(row):
                new_j = j - 1
                if element.moveable:
                    while new_j >= 0 and element.can_move(control_platform[i][new_j]):
                        new_j -= 1
                new_j = new_j + 1
                if element.can_move(control_platform[i][new_j]):
                    control_platform[i][new_j] = control_platform[i][j]
                    control_platform[i][j] = PlatformObject.EMPTY_SPACE
        self.control_platform = tuple(tuple(row) for row in control_platform)

    def _tilt_east(self) -> None:
        control_platform = list(list(control_platform)
                                for control_platform in self.control_platform)
        for i, row in enumerate(control_platform):
            for j, element in enumerate(row[::-1]):
                j = len(row) - 1 - j
                new_j = j + 1
                if element.moveable:
                    while new_j < len(control_platform) and element.can_move(control_platform[i][new_j]):
                        new_j += 1
                new_j = new_j - 1
                if element.can_move(control_platform[i][new_j]):
                    control_platform[i][new_j] = control_platform[i][j]
                    control_platform[i][j] = PlatformObject.EMPTY_SPACE
        self.control_platform = tuple(tuple(row) for row in control_platform)

    def cycle(self, cycles: int = 1000000000) -> int:
        score = self.score
        for _ in range(cycles):
            cache_index = self.control_platform
            if cache_index in self.cache:
                self.control_platform = self.cache[cache_index]
            else:
                self.tilt(Direction.NORTH)
                self.tilt(Direction.WEST)
                self.tilt(Direction.SOUTH)
                self.tilt(Direction.EAST)
                self.cache[cache_index] = self.control_platform

            if score == self.score:
                return score
            score = self.score
        return score


class Day14:

    def __init__(self, filepath: Path):
        self.filepath = filepath

    def parse_file(self) -> list[str]:
        with open(self.filepath, 'r', encoding="utf-8") as f:
            return f.read().splitlines()

    def parse(self) -> list[str]:
        return self.parse_file()

    def part_1(self) -> int:
        control_platform = ControlPlatform.create_control_platform(
            [[PlatformObject.from_str(c) for c in s] for s in self.parse_file()])
        control_platform.tilt()
        return control_platform.score

    def part_2(self) -> int:
        control_platform = ControlPlatform.create_control_platform(
            [[PlatformObject.from_str(c) for c in s] for s in self.parse_file()])
        control_platform.cycle()
        return control_platform.score


if __name__ == "__main__":
    INPUT_FILEPATH = Path(__file__).parent / "data" / \
        f"{Path(__file__).stem}.txt"
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?',
                        default=INPUT_FILEPATH, help=f"Path to data for {Path(__file__).stem}")
    args = parser.parse_args()

    day14 = Day14(Path(args.input).absolute())
    print(day14.part_1())
    print(day14.part_2())
