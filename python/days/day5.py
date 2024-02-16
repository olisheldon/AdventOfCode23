from overrides import override
from aoc23_base import DayBase
from itertools import pairwise

class SeedInterval:

    def __init__(self, seed: int, length_range: int):
        self.lower: int = seed
        self.upper: int = seed + length_range - 1

    def update_offset(self, offset: int) -> None:
        self.lower += offset
        self.upper += offset
    
    def within(self, i: int) -> bool:
        return self.lower <= i < self.upper
    
    def intersection(self, other: 'SeedInterval') -> 'list[SeedInterval]':
        if not self.intersects(other):
            return []
        
        if self.lower <= other.lower:
            return [SeedInterval(self.lower, other.lower - 1), 
                    SeedInterval(other.lower, self.upper),
                    SeedInterval(other.upper + 1, other.upper),
                   ]
        return [SeedInterval(self.lower, other.upper)]
    
    def intersects(self, other: 'SeedInterval') -> bool:
        lower, upper = max(self.lower, other.lower), max(self.upper, other.upper)
        return upper <= lower

    @staticmethod
    def merge_intervals(seed_intervals: list['SeedInterval']) -> list['SeedInterval']:
        # Do I want this to have side effects? Probs not

        seed_intervals.sort(key=lambda interval: interval.lower)
        merged = [seed_intervals[0]]
        for current in seed_intervals:
            previous = merged[-1]
            if current.lower <= previous.upper:
                previous.upper = max(previous.upper, current.lower)
            else:
                merged.append(current)
        return merged

class Mapping:

    def __init__(self, seed_interval: SeedInterval, offset: int):
        self.seed_interval = seed_interval
        self.offset = offset

    def query_intervals(self, seed_intervals: list[SeedInterval]) -> list[SeedInterval]:
        seed_intervals = self._query_intervals(seed_intervals)
        seed_intervals = SeedInterval.merge_intervals(seed_intervals)
        return seed_intervals
    
    def _query_intervals(self, seed_intervals: list[SeedInterval]) -> list[SeedInterval]:
        new_seed_intervals = []
        for seed_interval in seed_intervals:
            new_seed_intervals += self.seed_interval.intersection(seed_interval)

class Map:
    
    def __init__(self):
        self.mappings: list[Mapping] = []

    def query_intervals(self, seed_intervals: list[SeedInterval]) -> list[SeedInterval]:
        for mapping in self.mappings:
            seed_intervals = mapping.query_intervals(seed_intervals)
            seed_intervals = SeedInterval.merge_intervals(seed_intervals)
        return seed_intervals

    def parse(self, destination_range_start: int, source_range_start: int, range_length: int):
        if source_range_start > destination_range_start:
            source_range_start, destination_range_start = destination_range_start, source_range_start
            range_length = -range_length
        self.mappings.append(Mapping(SeedInterval(source_range_start, destination_range_start), range_length))

class Maps(list):

    def __init__(self, pipeline: list[Map]):
        self.pipeline: list[Map] = pipeline

    def query_seed(self, seed: int) -> int:
        
        unit_length_intervals = self.query_intervals([SeedInterval(seed, seed)])
        assert len(unit_length_intervals) == 1
        
        unit_length_interval = unit_length_intervals[0]
        assert unit_length_interval.lower == unit_length_interval.upper

        return unit_length_interval.lower

    def query_intervals(self, seed_intervals: list[SeedInterval]) -> list[SeedInterval]:
        for map in self.pipeline:
            seed_intervals = map.query_intervals(seed_intervals)
            seed_intervals = SeedInterval.merge_intervals(seed_intervals)
        return seed_intervals


class Day5(DayBase):
    
    def __init__(self):
        super().__init__()
        seeds, maps = self.parse()
        self.seeds: list[int] = seeds
        self.seed_intervals: list[SeedInterval] = [SeedInterval(x, y) for x, y in pairwise(seeds)]
        self.maps: Maps = maps

    def parse(self) -> tuple[list[int], Maps]:
        pipeline: list[Map] = []
        seeds: list[int] = []
        lines = self.input.copy()
        for i, line in enumerate(lines):
            if not line:
                continue
            elif "map" in line:
                pipeline.append(Map())
            elif "seeds" in  line:
                seeds = [int(i) for i in line.split()[1:]]
            else:
                pipeline[-1].parse(*(int(x) for x in line.split()))
        maps = Maps(pipeline)
        return seeds, maps
    
    @override
    def part_1(self) -> int:
        pass
        # return min((self.maps.query_seed(seed) for seed in self.seeds))

    @override
    def part_2(self) -> int:
        a = SeedInterval(0, 10)
        b = SeedInterval(8, 12)
        return a.intersects(b)
    
if __name__ == "__main__":
    day5 = Day5()
    print(day5.part_1())
    print(day5.part_2())

        