from overrides import override
from aoc23_base import DayBase
import itertools

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
    
    @property
    def bounds(self) -> tuple[int, int]:
        return (self.source_range_start, self.source_range_start + self.range_length)

class Map:
    
    def __init__(self):
        self.mappings: list[Mapping] = []

    def query(self, i: int) -> int:
        for mapping in self.mappings:
            if mapping.source_range_start < i < mapping.source_range_end:
                return i + mapping.offset
        # return i
        raise RuntimeError("Should not be called if not going to do any work because it is unnecessary!!")

    def parse(self, destination_range_start: int, source_range_start: int, range_length: int):
        self.mappings.append(Mapping(source_range_start, destination_range_start, range_length))

class Maps(list):

    def __init__(self, pipeline: list[Map]):
        self.pipeline: list[Map] = pipeline
        self.seed_ranges_requiring_work: list[tuple[int,int]] = self._create_seed_ranges_requiring_work(pipeline)

    @staticmethod
    def _merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
        list_intervals = [[interval[0], interval[1]] for interval in intervals]

        list_intervals.sort(key=lambda interval: interval[0])
        merged = [list_intervals[0]]
        for current in list_intervals:
            previous = merged[-1]
            if current[0] <= previous[1]:
                previous[1] = max(previous[1], current[1])
            else:
                merged.append(current)
        return [(interval[0], interval[1]) for interval in list_intervals]

    def _create_seed_ranges_requiring_work(self, pipeline: list[Map]) -> list[tuple[int,int]]:
        ranges = []
        for pipe in pipeline:
            for mapping in pipe.mappings:
                ranges.append(mapping.bounds)
        return self._merge_intervals(ranges)

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
        self.seed_ranges: list[tuple[int, int]] = []
        i = 0
        while i < len(seeds):
            self.seed_ranges.append((seeds[i], seeds[i + 1]))
            i += 2

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
        return 0
        # return min((self.maps.query(seed) for seed in self.seeds))

    @override
    def part_2(self) -> int:
        # result = int(1e100)
        # for seed_range in self.seed_ranges:
        #     for seed in seed_range.range:
        #         result = min(result, self.maps.query(seed))
        # return result

        seed_ranges_merged = Maps._merge_intervals(self.seed_ranges)
        map_ranges_requiring_work = self.maps.seed_ranges_requiring_work

        seeds_requiring_mapping = Maps._merge_intervals(list(itertools.chain(seed_ranges_merged, map_ranges_requiring_work)))

        