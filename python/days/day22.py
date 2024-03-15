from overrides import override
from aoc23_base import DayBase
from enum import Enum, Flag, auto
from dataclasses import dataclass
from typing import Sequence


@dataclass()
class Coord:
    x: int
    y: int
    z: int

    @classmethod
    def from_csv(cls, brick_str: str) -> 'Coord':
        x, y, z = brick_str.split(',')
        return Coord(int(x), int(y), int(z))


class Brick:

    def __init__(self, brick_str: str):
        first_coord, second_coord = brick_str.split('~')
        self.coord1: Coord = Coord.from_csv(first_coord)
        self.coord2: Coord = Coord.from_csv(second_coord)

    def __repr__(self) -> str:
        return f"Brick(coord1={self.coord1}, coord2={self.coord2})"

    def overlaps(self, other: 'Brick') -> bool:
        return max(self.coord1.x, other.coord1.x) <= min(self.coord2.x, other.coord2.x) and max(self.coord1.y, other.coord1.y) <= min(self.coord2.y, other.coord2.y)


class BrickContainer:

    def __init__(self, bricks: list[str]):
        self.snapshot_bricks: tuple[Brick, ...] = tuple(
            Brick(line) for line in bricks)

    @staticmethod
    def _fall(bricks: list[Brick]) -> list[Brick]:
        bricks.sort(key=lambda brick: brick.coord1.z)
        for i, brick in enumerate(bricks):
            max_z = 1
            for other in bricks[:i]:
                if brick.overlaps(other):
                    max_z = max(max_z, other.coord2.z + 1)
            brick.coord2.z -= brick.coord1.z - max_z
            brick.coord1.z = max_z

        return bricks

    @staticmethod
    def _bidirectional_supports(bricks: Sequence[Brick]) -> tuple[dict[int, set[int]], dict[int, set[int]]]:

        bricks_supporting = {i: set() for i in range(len(bricks))}
        supporting_bricks = {i: set() for i in range(len(bricks))}

        for j, above in enumerate(bricks):
            for i, below in enumerate(bricks[:j]):
                if below.overlaps(above) and above.coord1.z == below.coord2.z + 1:
                    bricks_supporting[i].add(j)
                    supporting_bricks[j].add(i)

        return bricks_supporting, supporting_bricks

    def safe_disintegration_count(self) -> int:

        bricks = self._fall(list(self.snapshot_bricks))

        bricks_supporting, supports_bricks = self._bidirectional_supports(
            bricks)

        total = 0

        for i in range(len(bricks)):
            if all(len(supports_bricks[j]) >= 2 for j in bricks_supporting[i]):
                total += 1

        return total


class Day22(DayBase):

    def __init__(self):
        super().__init__()
        self.brick_container = BrickContainer(self.input)

    @override
    def part_1(self) -> int:
        return self.brick_container.safe_disintegration_count()

    @override
    def part_2(self) -> int:
        pass


if __name__ == "__main__":
    day22 = Day22()
    print(day22.part_1())
    print(day22.part_2())
