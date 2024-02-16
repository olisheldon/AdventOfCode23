from overrides import override
from aoc23_base import DayBase
from enum import Enum, auto
from dataclasses import dataclass

@dataclass(frozen=True)
class Coord:
    i: int
    j: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.i + other.i, self.j + other.j)
    
class Segment(Enum):
    INSIDE = auto()
    OUTSIDE = auto()
    NEITHER = auto()

class Move(Enum):
    NORTH = auto() 
    EAST = auto() 
    SOUTH = auto() 
    WEST = auto()

    INVALID = auto() 

    @classmethod
    def move_to_coord_offset(cls, move: 'Move') -> Coord:
        match move:
            case cls.NORTH:
                return Coord(-1, 0)
            case cls.EAST:
                return Coord(0, 1)
            case cls.SOUTH:
                return Coord(1, 0)
            case cls.WEST:
                return Coord(0, -1)
            case _:
                return Coord(0, 0)

class TileType(Enum):
    VERTICAL = auto() 
    HORIZONTAL = auto() 
    BENDNE = auto() 
    BENDNW = auto() 
    BENDSW = auto() 
    BENDSE = auto() 
    GROUND = auto() 
    START = auto() 


    @classmethod
    def from_str(cls, s: str) -> 'TileType':
        match s:
            case "|":
                return cls.VERTICAL
            case "-":
                return cls.HORIZONTAL
            case "L":
                return cls.BENDNE
            case "J":
                return cls.BENDNW
            case "7":
                return cls.BENDSW
            case "F":
                return cls.BENDSE
            case ".":
                return cls.GROUND
            case "S":
                return cls.START
            case _:
                raise RuntimeError(f"Tile type {s} is not recognised.")


class Tile:

    def __init__(self, tile_char: str):
        self.tile_type: TileType = TileType.from_str(tile_char)
        self.segment: Segment = Segment.NEITHER
    
    def __repr__(self) -> str:
        return self.tile_type.name
            
    def move(self, move_in: Move) -> Move:
        match self.tile_type:
            case TileType.START:
                return Move.INVALID
            case TileType.VERTICAL:
                match move_in:
                    case Move.SOUTH:
                        return Move.SOUTH
                    case Move.NORTH:
                        return Move.NORTH
                    case _:
                        return Move.INVALID
            case TileType.HORIZONTAL:
                match move_in:
                    case Move.EAST:
                        return Move.EAST
                    case Move.WEST:
                        return Move.WEST
                    case _:
                        return Move.INVALID
            case TileType.BENDNE:
                match move_in:
                    case Move.SOUTH:
                        return Move.EAST
                    case Move.WEST:
                        return Move.NORTH
                    case _:
                        return Move.INVALID
            case TileType.BENDNW:
                match move_in:
                    case Move.SOUTH:
                        return Move.WEST
                    case Move.EAST:
                        return Move.NORTH
                    case _:
                        return Move.INVALID
            case TileType.BENDSW:
                match move_in:
                    case Move.NORTH:
                        return Move.WEST
                    case Move.EAST:
                        return Move.SOUTH
                    case _:
                        return Move.INVALID
            case TileType.BENDSE:
                match move_in:
                    case Move.NORTH:
                        return Move.EAST
                    case Move.WEST:
                        return Move.SOUTH
                    case _:
                        return Move.INVALID
            case TileType.GROUND:
                raise RuntimeError(f"Tile type {move_in} should not be called with {self.__name__}.")
            case _:
                raise RuntimeError(f"Tile type {move_in} not recognised.")
            
    def declare_segment(self, segment: Segment):
        if self.tile_type == TileType.GROUND:
            self.segment = segment


class Maze:

    def __init__(self, tiles: list[str]):
        self.tiles: dict[Coord, Tile] = {}
        self.start: Coord = Coord(0, 0)
        for i in range(len(tiles)):
            for j in range(len(tiles[0])):
                coord = Coord(i, j)
                self.tiles[coord] = Tile(tiles[i][j])
                if self.tiles[coord].tile_type == TileType.START:
                    self.start = coord

    def get_beginning_moves(self) -> list[Move]:
        return list(move for move in Move if self.tiles[self.start + Move.move_to_coord_offset(move)].move(move) != Move.INVALID)
    
    def traverse_pipes(self) -> int:
        beginning_moves: list[Move] = self.get_beginning_moves()
        move = beginning_moves[0]
        move_count = 1
        coord = self.start + Move.move_to_coord_offset(move)
        while self.tiles[coord].tile_type != TileType.START:
            move = self.tiles[coord].move(move)
            coord += Move.move_to_coord_offset(move)
            move_count += 1
        return move_count
    
    def furthest_point(self) -> int:
        move_count = self.traverse_pipes()
        return move_count // 2 + 1 if move_count % 2 else move_count // 2
    
    def spread_segment(self):
        coord_offsets = (Coord(-1, -1), Coord(1, -1), Coord(-1, 1), Coord(1, 1))
        for tile_coord, tile in self.tiles.items():
            if tile.tile_type == TileType.GROUND and tile.segment:
                for coord_offset in coord_offsets:
                    coord = tile_coord + coord_offset
                    if coord in self.tiles:
                        self.tiles[coord].segment = tile.segment
    
    def count_ground_inside(self) -> int:
        count = 0
        for tile in self.tiles.values():
            if tile.segment == Segment.INSIDE:
                count += 1
        return count

    

class Day10(DayBase):
    
    def __init__(self):
        super().__init__()

    def parse(self) -> list[str]:
        return self.input
    
    @override
    def part_1(self) -> int:
        maze = Maze(self.input)
        return maze.furthest_point()
    
    @override
    def part_2(self) -> int:
        maze = Maze(self.input)
        maze.traverse_pipes()
        maze.spread_segment()
        return maze.count_ground_inside()


if __name__ == "__main__":
    day10 = Day10()
    print(day10.part_1())
    print(day10.part_2())
