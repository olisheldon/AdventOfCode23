from overrides import override
from aoc23_base import DayBase
from functools import reduce

class RacePossibilities:

    def __init__(self, time: int, record_distance: int):
        self.time = time
        self.record_distance = record_distance

    @property
    def number_of_ways_to_beat(self):
        return sum(possible_distance > self.record_distance for possible_distance in self.possible_distances)

    @property
    def possible_distances(self):
        distances = []
        for time_holding_button in range(1, self.time + 1):
            time_moving = self.time - time_holding_button
            speed = time_holding_button
            distance = speed * time_moving
            distances.append(distance)
        return distances

class Day6(DayBase):
    
    def __init__(self):
        super().__init__()
        times, distances = self.parse()
        self.individual_races: list[RacePossibilities] = [RacePossibilities(time, distance) for time, distance in zip(times, distances)]
        
        time, distance = "", ""
        for t, d in zip(times, distances):
            time += str(t)
            distance += str(d)
        self.one_race: RacePossibilities = RacePossibilities(int(time), int(distance))

    def parse(self) -> tuple[list[int], list[int]]:
        times = [int(i) for i in self.input[0].split()[1:]]
        distances = [int(i) for i in self.input[1].split()[1:]]
        return times, distances
    
    @override
    def part_1(self) -> int:
        possible_ways_per_race = [race.number_of_ways_to_beat for race in self.individual_races]
        result = 0
        result += reduce((lambda x, y: x * y), possible_ways_per_race)
        return result

    @override
    def part_2(self) -> int:
        return self.one_race.number_of_ways_to_beat
        