from overrides import override
from aoc23_base import DayBase


def extrapolate(subhistory: list[int], forwards: bool = True) -> int:
    if all(val == 0 for val in subhistory):
        return 0

    deltas: list[int] = [y - x for x, y in zip(subhistory, subhistory[1:])]
    diff: int = extrapolate(deltas, forwards)

    if not forwards:
        return subhistory[0] - diff
    return subhistory[-1] + diff


class Day9(DayBase):

    def __init__(self):
        super().__init__()
        self.histories: list[list[int]] = [
            list(map(int, x)) for x in self.parse()]

    def parse(self) -> list[list[str]]:
        return [line.split() for line in self.input]

    @override
    def part_1(self) -> int:
        return sum(extrapolate(history) for history in self.histories)

    @override
    def part_2(self) -> int:
        return sum(extrapolate(history, forwards=False) for history in self.histories)


if __name__ == "__main__":
    day9 = Day9()
    print(day9.part_1())
    print(day9.part_2())
