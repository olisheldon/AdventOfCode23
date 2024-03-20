from pathlib import Path
import argparse
from functools import reduce


class RacePossibilities:

    def __init__(self, time: int, record_distance: int):
        self.time: int = time
        self.record_distance: int = record_distance

    @property
    def number_of_ways_to_beat(self):
        return sum(possible_distance > self.record_distance for possible_distance in self.possible_distances)

    @property
    def possible_distances(self):
        distances = []
        for time_holding_button in range(self.time + 1):
            time_moving = self.time - time_holding_button
            speed = time_holding_button
            distance = speed * time_moving
            distances.append(distance)
        return distances


class Day6:

    def __init__(self, filepath: Path):
        self.filepath = filepath
        times, distances = self.parse()
        self.individual_races: list[RacePossibilities] = [RacePossibilities(time, distance) for time, distance in zip(times, distances)]

        time, distance = "".join(map(str, times)), "".join(map(str, distances))
        self.one_race: RacePossibilities = RacePossibilities(int(time), int(distance))

    def parse_file(self) -> list[str]:
        with open(self.filepath, 'r', encoding="utf-8") as f:
            return f.read().splitlines()

    def parse(self) -> tuple[list[int], list[int]]:
        times = [int(i) for i in self.parse_file()[0].split()[1:]]
        distances = [int(i) for i in self.parse_file()[1].split()[1:]]
        return times, distances

    def part_1(self) -> int:
        possible_ways_per_race = [
            race.number_of_ways_to_beat for race in self.individual_races]
        result = reduce((lambda x, y: x * y), possible_ways_per_race)
        return result

    def part_2(self) -> int:
        return self.one_race.number_of_ways_to_beat


if __name__ == "__main__":
    INPUT_FILEPATH = Path(__file__).parent / "data" / f"{Path(__file__).stem}.txt"
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?', default=INPUT_FILEPATH, help=f"Path to data for {Path(__file__).stem}")
    args = parser.parse_args()

    day6 = Day6(Path(args.input).absolute())
    print(day6.part_1())
    print(day6.part_2())
