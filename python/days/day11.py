from overrides import override
from aoc23_base import DayBase
from enum import Enum, auto
from dataclasses import dataclass


class Pixel(Enum):
    GALAXY = auto()
    SPACE = auto()
    INVALID = auto()

    @classmethod
    def from_str(cls, c: str):
        match c:
            case '#':
                return cls.GALAXY
            case '.':
                return cls.SPACE
            case _:
                raise RuntimeError(f"Pixel {c} is not recognised.")


@dataclass(frozen=True)
class Coord:
    i: int
    j: int


class Image:

    def __init__(self, image_str: list[str]):
        self.image: list[list[Pixel]] = Image.create_image(image_str)
        self.galaxies: list[Coord] = Image.extract_galaxies(self.image)
        empty_columns, empty_rows = self.find_expanded_columns_and_rows(
            self.image)
        self.empty_columns: set[int] = empty_columns
        self.empty_rows: set[int] = empty_rows

    @staticmethod
    def create_image(image_str: list[str]) -> list[list[Pixel]]:
        image: list[list[Pixel]] = [[Pixel.INVALID] *
                                    len(image_str) for _ in range(len(image_str[0]))]
        for i, row in enumerate(image_str):
            for j, elem in enumerate(row):
                image[i][j] = Pixel.from_str(elem)
        return image

    @staticmethod
    def extract_galaxies(image: list[list[Pixel]]) -> list[Coord]:
        return list(Coord(i, j) for (i, row) in enumerate(image) for (j, pixel) in enumerate(row) if pixel is Pixel.GALAXY)

    @staticmethod
    def find_expanded_columns_and_rows(image: list[list[Pixel]]) -> tuple[set[int], set[int]]:
        empty_columns = set()
        empty_rows = set()
        for i in range(len(image)):
            if all(x is Pixel.SPACE for x in image[i]):
                empty_rows.add(i)
        for j in range(len(image[0])):
            if all(row[j] is Pixel.SPACE for row in image):
                empty_columns.add(j)
        return empty_columns, empty_rows

    def find_distances(self, expansion_coefficient: int = 2) -> int:
        moves = 0
        for i, gal1 in enumerate(self.galaxies):
            for gal2 in self.galaxies[:i]:
                for r in range(min(gal1.i, gal2.i), max(gal1.i, gal2.i)):
                    moves += expansion_coefficient if r in self.empty_rows else 1
                for c in range(min(gal1.j, gal2.j), max(gal1.j, gal2.j)):
                    moves += expansion_coefficient if c in self.empty_columns else 1
        return moves


class Day11(DayBase):

    def __init__(self):
        super().__init__()
        self.image = Image(self.parse())

    def parse(self) -> list[str]:
        return self.input

    @override
    def part_1(self) -> int:
        return self.image.find_distances()

    @override
    def part_2(self) -> int:
        return self.image.find_distances(expansion_coefficient=1000000)


if __name__ == "__main__":
    day11 = Day11()
    print(day11.part_1())
    print(day11.part_2())
