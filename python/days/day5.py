from overrides import override
from aoc23_base import DayBase

from IPython import embed


class SeedInterval:

    def __init__(self, lower: int, upper: int):
        if not lower <= upper:
            raise RuntimeError(f"{lower}, {upper}")
        if lower < 0:
            embed()
        self.lower: int = lower
        self.upper: int = upper
    
    def __repr__(self) -> str:
        return f"SeedInterval(lower={self.lower}, upper={self.upper})"
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, SeedInterval):
            raise RuntimeError()
        
        return self.lower == __value.lower and self.upper == __value.upper

    def apply_offset(self, offset: int) -> None:
        self.lower += offset
        self.upper += offset

        assert 0 <= self.lower <= self.upper
    
    def within(self, i: int) -> bool:
        return self.lower <= i < self.upper
    
    # def intersection(self, other: 'SeedInterval') -> 'list[SeedInterval]':
    #     if not self.intersects(other):
    #         return []
        
    #     if self.lower <= other.lower:
    #         return [SeedInterval(other.lower, self.upper)]
    #     return [SeedInterval(self.lower, other.upper)]
    
    def intersect_and_apply_offset(self, other: 'SeedInterval', offset: int) -> 'list[SeedInterval]':
        a, b = self, other

        if not a.intersects(b):
            return [other]

        intersections = self.interval_intersection([self], [other])
        
        if intersections:
            
            if intersections[0].lower > other.lower:
                intersections.append(SeedInterval(other.lower, intersections[0].lower - 1))
            
            if intersections[0].upper < other.upper:
                intersections.append(SeedInterval(intersections[0].upper + 1, other.upper))


        
        intersections[0].apply_offset(offset)

        if len(intersections) > 1:
            print(1)

        return intersections
    
    @staticmethod
    def interval_intersection(A: list['SeedInterval'], B: list['SeedInterval']) -> list['SeedInterval']:
        ans: list['SeedInterval'] = []
        i = j = 0

        while i < len(A) and j < len(B):
            # Let's check if A[i] intersects B[j].
            # lo - the startpoint of the intersection
            # hi - the endpoint of the intersection
            lo = max(A[i].lower, B[j].lower)
            hi = min(A[i].upper, B[j].upper)
            if lo <= hi:
                ans.append(SeedInterval(lo, hi))

            # Remove the interval with the smallest endpoint
            if A[i].upper < B[j].upper:
                i += 1
            else:
                j += 1

        return ans
    
    def intersects(self, other: 'SeedInterval') -> bool:
        sorted_seed_intervals = sorted([self, other], key=lambda x: x.lower)
        return sorted_seed_intervals[0].upper >= sorted_seed_intervals[1].lower

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

    def __repr__(self) -> str:
        return f"Mapping(seed_interval={self.seed_interval}, offset={self.offset})"

    def query_intervals(self, seed_intervals: list[SeedInterval]) -> list[SeedInterval]:
        seed_intervals = self._query_intervals(seed_intervals)
        seed_intervals = SeedInterval.merge_intervals(seed_intervals)
        return seed_intervals
    
    def _query_intervals(self, seed_intervals: list[SeedInterval]) -> list[SeedInterval]:
        new_seed_intervals = []
        for seed_interval in seed_intervals:
            new_seed_intervals += self.seed_interval.intersect_and_apply_offset(seed_interval, self.offset)
        return new_seed_intervals

class Map:
    
    def __init__(self):
        self.mappings: list[Mapping] = []

    def __repr__(self) -> str:
        return f"{self.mappings}"

    def query_intervals(self, seed_intervals: list[SeedInterval]) -> list[SeedInterval]:
        new_seed_intervals = []
        for mapping in self.mappings:
            new_seed_intervals += mapping.query_intervals(seed_intervals)
            new_seed_intervals = SeedInterval.merge_intervals(new_seed_intervals)
        return new_seed_intervals

    def parse(self, destination_range_start: int, source_range_start: int, range_length: int):
        assert range_length >= 0
        offset = destination_range_start - source_range_start
        self.mappings.append(Mapping(SeedInterval(source_range_start, source_range_start + range_length - 1), offset))

class Maps:

    def __init__(self, pipeline: list[Map]):
        self.pipeline: list[Map] = pipeline

    def __repr__(self) -> str:
        return f"{self.pipeline}"

    def query_seed(self, seed: int) -> int:
        
        unit_length_intervals = self.query_intervals([SeedInterval(seed, seed)])
        assert len(unit_length_intervals) == 1
        
        unit_length_interval = unit_length_intervals[0]
        assert unit_length_interval.lower == unit_length_interval.upper

        return unit_length_interval.lower

    def query_intervals(self, seed_intervals: list[SeedInterval]) -> list[SeedInterval]:
        new_seed_intervals = []
        for pipeline in self.pipeline:
            new_seed_intervals += pipeline.query_intervals(seed_intervals)
            new_seed_intervals = SeedInterval.merge_intervals(new_seed_intervals)
        return new_seed_intervals


class Day5(DayBase):
    
    def __init__(self):
        super().__init__()
        seeds, maps = self.parse()
        self.seeds: list[int] = seeds
        self.maps: Maps = maps

        self.seed_intervals: list[SeedInterval] = []
        i = 0
        while i < len(seeds):
            self.seed_intervals.append(SeedInterval(seeds[i], seeds[i] + seeds[i + 1] - 1))
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
        return [self.maps.query_intervals([SeedInterval(seed, seed)]) for seed in [self.seeds[0]]]

    @override
    def part_2(self) -> int:
        # seed_intervals = self.maps.query_intervals(self.seed_intervals)
        seed_intervals = self.maps.query_intervals([SeedInterval(a, b) for a, b in [(79, 79), (14, 14), (55, 55), (13, 13)]])
        # return seed_intervals
        return min(seed_interval.lower for seed_interval in  seed_intervals)

if __name__ == "__main__":
    day5 = Day5()

    # day5.maps.pipeline = [day5.maps.pipeline[0]]

    print(day5.part_1())
    print(day5.part_2())