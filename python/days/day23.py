from overrides import override
from aoc23_base import DayBase
from enum import Enum, auto
from dataclasses import dataclass
from collections import deque

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

    def move(self, start: Coord = Coord(0, 1), end: Coord | None = None) -> int:
        used_coords: set[Coord] = set()
        used_coords.add(start)
        queue: deque[tuple[Coord, Move, int]] = deque()
        queue.append((start, Move.DOWN, 1))

        while queue:
            coord, move, length = queue.popleft()
            if not self.within_boundary(coord) or not PathTile.can_move(self.hiking_map[coord.i][coord.j], move):
                continue

            if coord == end:
                return length
            
            for move in Move.all_moves:
                new_coord = coord + Move.move(move)
                if new_coord not in used_coords:
                    queue.append((new_coord, move, length + 1))
                    used_coords.add(new_coord)
                    
        return -1



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
        start = 0, 1
        return self.hiking_map.move()

    @override
    def part_2(self) -> int:
        pass

if __name__ == "__main__":
    day23 = Day23()
    print(day23.part_1())
    print(day23.part_2())
