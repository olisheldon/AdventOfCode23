from overrides import override
from aoc23_base import DayBase
from enum import Enum, auto
from dataclasses import dataclass
import sys
sys.setrecursionlimit(2**15)

@dataclass(frozen = True)
class Coord:
    i: int
    j: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.i + other.i, self.j + other.j)

class Move(Enum):
    UP = auto(),
    RIGHT = auto(),
    DOWN = auto(),
    LEFT = auto(),

    @classmethod
    def move(cls, move: 'Move') -> Coord:
        match move:
            case cls.UP:
                return Coord(-1, 0)
            case cls.RIGHT:
                return Coord(0, 1)
            case cls.DOWN:
                return Coord(1, 0)
            case cls.LEFT:
                return Coord(0, -1)
            case _:
                raise RuntimeError(f"Move {move} is not recognised.")
            
    @classmethod
    @property
    def all_moves(cls) -> list['Move']:
        return [move for move in Move]

            
class PathTile(Enum):
    PATH = auto(),
    FOREST = auto(),
    SLOPE_UP = auto(),
    SLOPE_RIGHT = auto(),
    SLOPE_DOWN = auto(),
    SLOPE_LEFT = auto(),

    @classmethod
    def from_str(cls, c: str) -> 'PathTile':
        match c:
            case '.':
                return cls.PATH
            case '#':
                return cls.FOREST
            case '^':
                return cls.SLOPE_UP
            case '>':
                return cls.SLOPE_RIGHT
            case 'v':
                return cls.SLOPE_DOWN
            case '<':
                return cls.SLOPE_LEFT
            case _:
                raise RuntimeError(f"PathTile {c} is not recognised.")

    @classmethod
    def from_pathtile(cls, c: 'PathTile') -> str:
        match c:
            case cls.PATH:
                return '.'
            case cls.FOREST:
                return '#'
            case cls.SLOPE_UP:
                return '^'
            case cls.SLOPE_RIGHT:
                return '>'
            case cls.SLOPE_DOWN:
                return 'v'
            case cls.SLOPE_LEFT:
                return '<'
            case _:
                raise RuntimeError(f"PathTile {c} is not recognised.")
    
    @classmethod
    def possible_moves(cls, path_tile: 'PathTile') -> list[Move]:
        match path_tile:
            case cls.PATH:
                return Move.all_moves
            case cls.FOREST:
                return []
            case cls.SLOPE_UP:
                return [Move.UP]
            case cls.SLOPE_RIGHT:
                return [Move.RIGHT]
            case cls.SLOPE_DOWN:
                return [Move.DOWN]
            case cls.SLOPE_LEFT:
                return [Move.LEFT]
            case _:
                raise RuntimeError(f"PathTile {path_tile} is not recognised.")

    @classmethod
    def can_move(cls, path_tile: 'PathTile', move: Move) -> bool:
        match path_tile:
            case cls.PATH:
                return True
            case cls.FOREST:
                return False
            case cls.SLOPE_UP:
                if move is not Move.DOWN:
                    return True
                else:
                    return False
            case cls.SLOPE_RIGHT:
                if move is not Move.LEFT:
                    return True
                else:
                    return False
            case cls.SLOPE_DOWN:
                if move is not Move.UP:
                    return True
                else:
                    return False
            case cls.SLOPE_LEFT:
                if move is not Move.RIGHT:
                    return True
                else:
                    return False
            case _:
                raise RuntimeError(f"PathTile {path_tile} is not recognised.")

class HikingMap:

    def __init__(self, hiking_map: list[list[PathTile]]):
        self.hiking_map: list[list[PathTile]] = hiking_map

    def __repr__(self) -> str:
        return "\n".join("".join([PathTile.from_pathtile(tile) for tile in row]) for row in self.hiking_map)
    
    def repr_with_used_coords(self, used_coords: set[Coord]) -> str:
        return "\n".join("".join([PathTile.from_pathtile(tile) if Coord(i, j) not in used_coords else 'O' for (j, tile) in enumerate(row)]) for (i, row) in enumerate(self.hiking_map))


    def move(self, start: Coord = Coord(0, 1), end: Coord = Coord(22, 21)) -> int | float:
        used_coords: set[Coord] = set()

        def dfs(coord: Coord) -> int | float:
            if coord == end:
                return 0

            m = -float("inf")

            used_coords.add(coord)
            for move in Move.all_moves:
                new_coord = coord + Move.move(move)
                if self.within_boundary(new_coord) and PathTile.can_move(self.hiking_map[new_coord.i][new_coord.j], move) and new_coord not in used_coords:
                    m = max(m, dfs(new_coord) + 1)
            used_coords.remove(coord)

            return m
        
        res = dfs(start)

        return res

    def within_boundary(self, coord: Coord) -> bool:
        return 0 <= coord.i < len(self.hiking_map) \
           and 0 <= coord.j < len(self.hiking_map[0])



class Day23(DayBase):
    
    def __init__(self):
        super().__init__()
        self.hiking_map: HikingMap = HikingMap(self.parse())

    def parse(self) -> list[list[PathTile]]:
        hiking_map: list[list[PathTile]] = []
        for i, row in enumerate(self.input):
            tile_row = []
            for j, tile in enumerate(row):
                tile_row.append(PathTile.from_str(tile))
            hiking_map.append(tile_row)
        return hiking_map
                      
    @override
    def part_1(self) -> int:
        coords_longest_path = self.hiking_map.move()
        print(self.hiking_map)
        print(coords_longest_path)
        # print(self.hiking_map.repr_with_used_coords(coords_longest_path))

    @override
    def part_2(self) -> int:
        pass

if __name__ == "__main__":
    day23 = Day23()
    print(day23.part_1())
    print(day23.part_2())
