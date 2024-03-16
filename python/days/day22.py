from overrides import override
from aoc23_base import DayBase
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
        self.end1: Coord = Coord.from_csv(first_coord)
        self.end2: Coord = Coord.from_csv(second_coord)

    def __repr__(self) -> str:
        return f"Brick(end1={self.end1}, end2={self.end2})"

    def overlaps(self, other: 'Brick', plane: tuple[str, str] = ('x', 'y')) -> bool:
        '''
        plane argument generalises overlaps to be in any pair of planes
        '''
        axis_0, axis_1 = plane
        return max(getattr(self.end1, axis_0), getattr(other.end1, axis_0)) <= min(getattr(self.end2, axis_0), getattr(other.end2, axis_0)) and max(getattr(self.end1, axis_1), getattr(other.end1, axis_1)) <= min(getattr(self.end2, axis_1), getattr(other.end2, axis_1))


class BrickContainer:

    def __init__(self, bricks: list[str]):
        self.snapshot_bricks: tuple[Brick, ...] = tuple(
            Brick(line) for line in bricks)

    @staticmethod
    def _fall(bricks: list[Brick]) -> list[Brick]:
        bricks.sort(key=lambda brick: brick.end1.z)
        for i, brick in enumerate(bricks):
            max_z = 1
            for other in bricks[:i]:
                if brick.overlaps(other):
                    max_z = max(max_z, other.end2.z + 1)
            brick.end2.z -= brick.end1.z - max_z
            brick.end1.z = max_z

        return bricks

    @staticmethod
    def _bidirectional_supports(bricks: Sequence[Brick]) -> tuple[dict[int, set[int]], dict[int, set[int]]]:

        brick_supports = {i: set() for i in range(len(bricks))}
        supported_by_brick = {i: set() for i in range(len(bricks))}

        for j, above in enumerate(bricks):
            for i, below in enumerate(bricks[:j]):
                if below.overlaps(above) and above.end1.z == below.end2.z + 1:
                    brick_supports[i].add(j)
                    supported_by_brick[j].add(i)

        return brick_supports, supported_by_brick

    def safe_disintegration_count(self) -> int:

        bricks = self._fall(list(self.snapshot_bricks))

        brick_supports, supported_by_brick = self._bidirectional_supports(
            bricks)

        total = 0

        for i in range(len(bricks)):
            if all(len(supported_by_brick[j]) >= 2 for j in brick_supports[i]):
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
