from overrides import override
from aoc23_base import DayBase
from dataclasses import dataclass


@dataclass(order=True)
class Interval:
    lower: int
    upper: int

    @staticmethod
    def merge_intervals(intervals: list['Interval']) -> list['Interval']:

        if not intervals:
            return intervals

        intervals.sort(key=lambda interval: interval.lower)
        merged_intervals = [intervals[0]]
        for current_interval in intervals:
            previous_interval = merged_intervals[-1]
            if current_interval.lower <= previous_interval.upper:
                previous_interval.upper = max(
                    previous_interval.upper, current_interval.lower)
            else:
                merged_intervals.append(current_interval)

        return merged_intervals


@dataclass(frozen=True)
class Mapping:
    destination_range_start: int
    source_range_start: int
    range_length: int


class Map:

    def __init__(self, name: str):
        self.name: str = name
        self.mappings: list[Mapping] = []

    def __repr__(self) -> str:
        return f"{self.mappings}"

    def query_mappings(self, intervals: list[Interval]) -> list[Interval]:
        new_intervals: list[Interval] = []

        while intervals:
            interval = intervals.pop()
            for mapping in self.mappings:
                interval_overlap_lower = max(
                    interval.lower, mapping.source_range_start)
                interval_overlap_upper = min(
                    interval.upper, mapping.source_range_start + mapping.range_length)
                if interval_overlap_lower < interval_overlap_upper:
                    new_intervals.append(Interval(interval_overlap_lower - mapping.source_range_start + mapping.destination_range_start,
                                         interval_overlap_upper - mapping.source_range_start + mapping.destination_range_start))
                    if interval_overlap_lower > interval.lower:
                        intervals.append(
                            Interval(interval.lower, interval_overlap_lower))
                    if interval.upper > interval_overlap_upper:
                        intervals.append(
                            Interval(interval_overlap_upper, interval.upper))
                    break
            else:
                new_intervals.append(interval)

        return new_intervals

    def parse(self, destination_range_start: int, source_range_start: int, range_length: int) -> None:
        assert range_length >= 0
        self.mappings.append(
            Mapping(destination_range_start, source_range_start, range_length))


class Maps:

    def __init__(self, pipeline: list[Map]):
        self.pipeline: list[Map] = pipeline

    def __repr__(self) -> str:
        return f"{self.pipeline}"

    def query_seed(self, seed: int) -> int:

        unit_length_intervals = self.query_intervals(
            [Interval(seed, seed + 1)])
        assert len(unit_length_intervals) == 1

        unit_length_interval = unit_length_intervals[0]
        assert unit_length_interval.lower == unit_length_interval.upper - 1

        return unit_length_interval.lower

    def query_intervals(self, intervals: list[Interval]) -> list[Interval]:
        intervals = intervals.copy()
        for pipeline in self.pipeline:
            intervals = pipeline.query_mappings(intervals)
            intervals = Interval.merge_intervals(intervals)
        return intervals


class Day5(DayBase):

    def __init__(self):
        super().__init__()
        seeds, maps = self.parse()
        self.seeds: list[int] = seeds
        self.maps: Maps = maps

        self.intervals: list[Interval] = []
        i = 0
        while i < len(seeds):
            self.intervals.append(Interval(seeds[i], seeds[i] + seeds[i + 1]))
            i += 2

    def parse(self) -> tuple[list[int], Maps]:
        pipeline: list[Map] = []
        seeds: list[int] = []
        lines = self.input.copy()
        for _, line in enumerate(lines):
            if not line:
                continue
            elif "map" in line:
                pipeline.append(Map(line.split()[0]))
            elif "seeds" in line:
                seeds = [int(i) for i in line.split()[1:]]
            else:
                pipeline[-1].parse(*(int(x) for x in line.split()))
        maps = Maps(pipeline)
        return seeds, maps

    @override
    def part_1(self) -> int:
        min_from_intervals = min(self.maps.query_intervals(
            [Interval(seed, seed + 1) for seed in self.seeds])).lower
        min_from_seed = min(self.maps.query_seed(seed) for seed in self.seeds)
        assert min_from_seed == min_from_intervals
        return min_from_seed

    @override
    def part_2(self) -> int:
        return min(self.maps.query_intervals(self.intervals)).lower


if __name__ == "__main__":
    day5 = Day5()
    print(day5.part_1())
    print(day5.part_2())
