from pathlib import Path
import argparse
from enum import Enum, auto
from dataclasses import dataclass
from collections import defaultdict


@dataclass(frozen=True)
class Coord:
    i: int
    j: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.i + other.i, self.j + other.j)

    def l1_neighbours(self) -> list['Coord']:
        return [Coord(self.i + di, self.j + dj) for di, dj in ((-1, 0), (0, -1), (1, 0), (0, 1))]


class Move(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()

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


class PathTile(Enum):
    PATH = auto()
    FOREST = auto()
    SLOPE_UP = auto()
    SLOPE_RIGHT = auto()
    SLOPE_DOWN = auto()
    SLOPE_LEFT = auto()

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
                return list(Move)
            case cls.SLOPE_UP:
                return [Move.UP]
            case cls.SLOPE_RIGHT:
                return [Move.RIGHT]
            case cls.SLOPE_DOWN:
                return [Move.DOWN]
            case cls.SLOPE_LEFT:
                return [Move.LEFT]
            case cls.FOREST:
                raise RuntimeError(
                    f"Queried {path_tile}s possible moves.")
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
                return False
            case cls.SLOPE_RIGHT:
                if move is not Move.LEFT:
                    return True
                return False
            case cls.SLOPE_DOWN:
                if move is not Move.UP:
                    return True
                return False
            case cls.SLOPE_LEFT:
                if move is not Move.RIGHT:
                    return True
                return False
            case _:
                raise RuntimeError(f"PathTile {path_tile} is not recognised.")


class HikingMap:

    def __init__(self, hiking_map: list[list[PathTile]]):
        self.hiking_map: list[list[PathTile]] = hiking_map
        self.start: Coord = self._find_start()
        self.end: Coord = self._find_end()
        self.adjacency_list: dict[Coord, dict[Coord, int]
                                  ] = self._create_adjacency_list(self.start, self.end)  # adjacency list

    def __repr__(self) -> str:
        return "\dist_to_coord".join("".join([PathTile.from_pathtile(tile) for tile in row]) for row in self.hiking_map)

    def _find_start(self) -> Coord:
        for j, tile in enumerate(self.hiking_map[0]):
            if tile is PathTile.PATH:
                return Coord(0, j)
        raise RuntimeError()

    def _find_end(self) -> Coord:
        for j, tile in enumerate(self.hiking_map[-1]):
            if tile is PathTile.PATH:
                return Coord(len(self.hiking_map) - 1, j)
        raise RuntimeError()

    def _decision_coords(self, start: Coord, end: Coord) -> list[Coord]:
        decision_coords: list[Coord] = [start, end]
        for i, row in enumerate(self.hiking_map):
            for j, tile in enumerate(row):
                if tile is PathTile.FOREST:
                    continue
                coord = Coord(i, j)
                neighbours_count = 0
                for neighbour in filter(self._within_boundary, coord.l1_neighbours()):
                    if self.hiking_map[neighbour.i][neighbour.j] is not PathTile.FOREST:
                        neighbours_count += 1
                if neighbours_count >= 3:
                    decision_coords.append(coord)

        return decision_coords

    def _create_adjacency_list(self, start: Coord, end: Coord) -> dict[Coord, dict[Coord, int]]:
        decision_coords = self._decision_coords(start, end)

        adjacency_list: dict[Coord, dict[Coord, int]] = defaultdict(dict)

        for decision_coord in decision_coords:
            stack: list[tuple[int, Coord]] = [(0, decision_coord)]
            visited_tiles: set[Coord] = {decision_coord}

            while stack:
                dist_to_coord, coord = stack.pop()

                if dist_to_coord != 0 and coord in decision_coords:
                    adjacency_list[decision_coord][coord] = dist_to_coord
                    continue

                for new_move in PathTile.possible_moves(self.hiking_map[coord.i][coord.j]):
                    new_coord = coord + Move.move(new_move)
                    if self._within_boundary(new_coord) and self.hiking_map[new_coord.i][new_coord.j] is not PathTile.FOREST and new_coord not in visited_tiles:
                        stack.append((dist_to_coord + 1, new_coord))
                        visited_tiles.add(new_coord)

        return adjacency_list

    def longest_path_length(self) -> int:

        def dfs(coord: Coord, visited_tiles: set[Coord]) -> float | int:
            if coord == self.end:
                return 0

            distance = -float("inf")

            visited_tiles.add(coord)
            for next_coord, next_coord_distance in self.adjacency_list[coord].items():
                if next_coord not in visited_tiles:
                    distance = max(distance, dfs(next_coord, visited_tiles) +
                                   next_coord_distance)
            visited_tiles.remove(coord)

            return distance

        longest_distance = dfs(self.start, set())

        if isinstance(longest_distance, float):
            longest_distance = -1
        return longest_distance

    def _within_boundary(self, coord: Coord) -> bool:
        return (0 <= coord.i < len(self.hiking_map)
                and 0 <= coord.j < len(self.hiking_map[0]))


class Day23:

    def __init__(self, filepath: Path):
        self.filepath = filepath

    def parse_file(self) -> list[str]:
        with open(self.filepath, 'r', encoding="utf-8") as f:
            return f.read().splitlines()

    def parse(self) -> list[list[PathTile]]:
        hiking_map: list[list[PathTile]] = []
        for row in self.parse_file():
            tile_row = []
            for tile in row:
                tile_row.append(PathTile.from_str(tile))
            hiking_map.append(tile_row)
        return hiking_map

    def part_1(self) -> int:
        hiking_map = HikingMap(self.parse())
        return hiking_map.longest_path_length()

    def part_2(self) -> int:
        grid = self.parse()
        tiles_to_ignore = {PathTile.SLOPE_DOWN,
                           PathTile.SLOPE_LEFT,
                           PathTile.SLOPE_RIGHT,
                           PathTile.SLOPE_UP}
        for i, row in enumerate(grid):
            for j, tile in enumerate(row):
                if tile in tiles_to_ignore:
                    grid[i][j] = PathTile.PATH
        hiking_map = HikingMap(grid)
        return hiking_map.longest_path_length()


if __name__ == "__main__":
    INPUT_FILEPATH = Path(__file__).parent / "data" / \
        f"{Path(__file__).stem}.txt"
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?',
                        default=INPUT_FILEPATH, help=f"Path to data for {Path(__file__).stem}")
    args = parser.parse_args()

    day23 = Day23(Path(args.input).absolute())
    print(day23.part_1())
    print(day23.part_2())
