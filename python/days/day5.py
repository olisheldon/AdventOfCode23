from overrides import override
from aoc23_base import DayBase

import math

class Mapping:
    def __init__(self, source_range_start: int, destination_range_start: int, range_length: int):
        self.source_range_start: int = source_range_start
        self.destination_range_start: int = destination_range_start
        self.range_length: int = range_length

        self.source_range_end: int = source_range_start + range_length
        self.offset: int = destination_range_start - source_range_start
    
    @property
    def range(self):
        return range(self.source_range_start, self.source_range_start + self.range_length)

class Map:
    
    def __init__(self):
        self.mappings: list[Mapping] = []

    def query(self, i: int) -> int:
        for mapping in self.mappings:
            if mapping.source_range_start < i < mapping.source_range_end:
                return i + mapping.offset
        raise RuntimeError("Should not be called if not going to do any work because it is unnecessary!!")

    def parse(self, destination_range_start: int, source_range_start: int, range_length: int):
        self.mappings.append(Mapping(source_range_start, destination_range_start, range_length))

class Maps(list):

    def __init__(self):
        self.pipeline: list[Map] = []


    def query(self, seed: int) -> int:
        for map in self.pipeline:
            seed = map.query(seed)
        return seed


class Day5(DayBase):
    
    def __init__(self):
        super().__init__()
        seeds, maps = self.parse()
        self.seeds: list[int] = seeds
        self.maps: Maps = maps

        # Part 2
        self.seed_ranges: list[Mapping] = []
        i = 0
        while i < len(seeds):
            self.seed_ranges.append(Mapping(seeds[i], seeds[i], seeds[i + 1]))
            i += 2

    def parse(self) -> tuple[list[int], Maps]:
        maps: Maps = Maps()
        seeds: list[int] = []
        lines = self.input.copy()
        for i, line in enumerate(lines):
            if not line:
                continue
            elif "map" in line:
                maps.pipeline.append(Map())
            elif "seeds" in  line:
                seeds = [int(i) for i in line.split()[1:]]
            else:
                maps.pipeline[-1].parse(*(int(x) for x in line.split()))
        return seeds, maps
    
    @override
    def part_1(self) -> int:
        return min((self.maps.query(seed) for seed in self.seeds))

    @override
    def part_2(self) -> int:
        result = int(1e100)
        for seed_range in self.seed_ranges:
            for seed in seed_range.range:
                result = min(result, self.maps.query(seed))
        return result