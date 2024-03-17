from pathlib import Path
import argparse
from dataclasses import dataclass
from typing import Sequence
from collections import deque


@dataclass()
class Coord:
    x: int
    y: int
    z: int

    @classmethod
    def from_csv(cls, brick_str: str) -> 'Coord':
        return Coord(*map(int, brick_str.split(',')))


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
        return (max(getattr(self.end1, axis_0), getattr(other.end1, axis_0)) <= min(getattr(self.end2, axis_0), getattr(other.end2, axis_0))
                and max(getattr(self.end1, axis_1), getattr(other.end1, axis_1)) <= min(getattr(self.end2, axis_1), getattr(other.end2, axis_1)))


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

        brick_supports_values = {i: set() for i in range(len(bricks))}
        values_that_support_brick = {i: set() for i in range(len(bricks))}

        for j, above in enumerate(bricks):
            for i, below in enumerate(bricks[:j]):
                if below.overlaps(above) and above.end1.z == below.end2.z + 1:
                    brick_supports_values[i].add(j)
                    values_that_support_brick[j].add(i)

        return brick_supports_values, values_that_support_brick

    def safe_disintegration_count(self) -> int:

        fallen_bricks = self._fall(list(self.snapshot_bricks))

        brick_supports_values, values_that_support_brick = self._bidirectional_supports(
            fallen_bricks)

        safe_count = 0

        for i in range(len(fallen_bricks)):
            if all(len(values_that_support_brick[j]) >= 2 for j in brick_supports_values[i]):
                safe_count += 1

        return safe_count

    def chain_reaction_count(self) -> int:

        fallen_bricks = self._fall(list(self.snapshot_bricks))

        brick_supports_values, values_that_support_brick = self._bidirectional_supports(
            fallen_bricks)

        chain_reaction_count = 0

        for dis_brick in range(len(fallen_bricks)):
            q = deque(other_brick for other_brick in brick_supports_values[dis_brick] if len(
                values_that_support_brick[other_brick]) == 1)
            falling: set[int] = set(q)
            falling.add(dis_brick)

            while q:
                non_supported_brick = q.popleft()
                for cascade_brick in brick_supports_values[non_supported_brick]:
                    if (cascade_brick not in falling and values_that_support_brick[cascade_brick].issubset(falling)):
                        q.append(cascade_brick)
                        falling.add(cascade_brick)

            chain_reaction_count += len(falling) - 1

        return chain_reaction_count


class Day22:

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.brick_container = BrickContainer(self.parse_file())

    def parse_file(self) -> list[str]:
        with open(self.filepath, 'r', encoding="utf-8") as f:
            return f.read().splitlines()

    def part_1(self) -> int:
        return self.brick_container.safe_disintegration_count()

    def part_2(self) -> int:
        return self.brick_container.chain_reaction_count()


if __name__ == "__main__":
    INPUT_FILEPATH = Path(__file__).parent / "data" / \
        f"{Path(__file__).stem}.txt"
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?',
                        default=INPUT_FILEPATH, help=f"Path to data for {Path(__file__).stem}")
    args = parser.parse_args()

    day22 = Day22(Path(args.input).absolute())
    print(day22.part_1())
    print(day22.part_2())
