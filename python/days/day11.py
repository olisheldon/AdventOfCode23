from overrides import override
from aoc23_base import DayBase
from enum import Enum, auto
from itertools import combinations
from dataclasses import dataclass

class Pixel(Enum):
    GALAXY = auto(),
    SPACE = auto(),
    INVALID = auto(),

    @classmethod
    def from_str(cls, c: str):
        match c:
            case '#':
                return cls.GALAXY
            case '.':
                return cls.SPACE
            case _:
                raise RuntimeError(f"Pixel {c} is not recognised.")
            
@dataclass(frozen=True, order=True)
class Coord:
    i: int
    j: int

    def get_path(self, other: 'Coord') -> list['Coord']:
        path_vertical = self.get_path_vertical(other)
        path_horizontal = self.get_path_horizontal(path_vertical[-1])
        return sorted(list(set(path_vertical + path_horizontal)))
    
    def get_path_vertical(self, other: 'Coord') -> list['Coord']:
        coords = []

        if self.is_north(other):
            coords += Coord(self.i + 1, other.j).get_path_vertical(other)
        elif self.is_south(other):
            coords += Coord(self.i - 1, other.j).get_path_vertical(other)
        return coords + [Coord(self.i, other.j)]
    
    def get_path_horizontal(self, other: 'Coord') -> list['Coord']:
        coords = []

        if self.is_west(other):
            coords += Coord(other.i, self.j + 1).get_path_horizontal(other)
        elif self.is_east(other):
            coords += Coord(other.i, self.j - 1).get_path_horizontal(other)
        return coords + [Coord(other.i, self.j)]
            
    
    def is_west(self, other: 'Coord') -> bool:
        return self.j < other.j
    
    def is_east(self, other: 'Coord') -> bool:
        return self.j > other.j
    
    def is_north(self, other: 'Coord') -> bool:
        return self.i < other.i
    
    def is_south(self, other: 'Coord') -> bool:
        return self.i > other.i

class Image:

    def __init__(self, image_str: list[str]):
        self.image: list[list[Pixel]] = Image.create_image(image_str)
        self.galaxies: set[Coord] = Image.extract_galaxies(self.image)
        empty_columns, empty_rows = self.find_expanded_columns_and_rows(self.image)
        self.empty_columns: set[int] = empty_columns
        self.empty_rows: set[int] = empty_rows

    @staticmethod
    def create_image(image_str: list[str]) -> list[list[Pixel]]:
        image: list[list[Pixel]] = [[Pixel.INVALID] * len(image_str) for _ in range(len(image_str[0]))]
        for i, row in enumerate(image_str):
            for j, elem in enumerate(row):
                image[j][i] = Pixel.from_str(elem)
        return image
    
    @staticmethod
    def extract_galaxies(image: list[list[Pixel]]) -> set[Coord]:
        return set(Coord(i, j) for (j, row) in enumerate(image) for (i, pixel) in enumerate(row) if pixel is Pixel.GALAXY)

    @staticmethod
    def find_expanded_columns_and_rows(image: list[list[Pixel]]) -> tuple[set[int], set[int]]:
        empty_columns = set()
        empty_rows = set()
        for i in range(len(image)):
            if all([x == Pixel.SPACE for x in image[i]]):
                empty_rows.add(i)
        for j in range(len(image[0])):
            if all([row[j] == Pixel.SPACE for row in image]):
                empty_columns.add(j)
        return empty_columns, empty_rows
    
    def find_distances(self, expansion_coefficient: int = 2) -> int:
        moves = 0
        for gal1, gal2 in combinations(self.galaxies, 2):
            move = 0
            for coord in gal1.get_path(gal2):
                if coord != gal1:
                    if coord.i in self.empty_columns:
                        move += expansion_coefficient
                    elif coord.j in self.empty_rows:
                        move += expansion_coefficient
                    else:
                        move += 1
            moves += move
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
