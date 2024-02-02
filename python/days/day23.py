from overrides import override
from aoc23_base import DayBase
from enum import Enum, auto
from dataclasses import dataclass

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
            # case cls.FOREST:
            #     return []
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
        if end is None:
            end = Coord(len(self.hiking_map) - 1, len(self.hiking_map[0]) - 1)

        self._move(start, end, used_coords)
        return len(used_coords)
        
    def _move(self, start: Coord, end: Coord, used_coords: set[Coord]) -> set[Coord]:
        tile = self.hiking_map[start.i][start.j]
        possible_moves = PathTile.possible_moves(tile)
        used_coords.add(start)
        
        if start == end:
            return used_coords
        

        if not possible_moves:
            return set()
        
        new_moves: list[Move] = []
        for possible_move in possible_moves:
            new_coord = Move.move(possible_move) + start
            new_tile = self.hiking_map[new_coord.i][new_coord.j]
            if PathTile.can_move(new_tile, possible_move) and new_coord not in used_coords:
                new_moves.append(possible_move)

        for move in new_moves:
            self._move(start + Move.move(move), end, used_coords)



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
