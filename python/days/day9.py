from overrides import override
from aoc23_base import DayBase
    
class History:

    def __init__(self, values_str: list[str]):
        values: list[int] = [int(value) for value in values_str]
        self.differences: list[list[int]] = History._generate_differences(values)

    def __repr__(self) -> str:
        repr = ""
        for difference in self.differences:
            repr += f"\n{len(difference)} {difference.__repr__()}"
        return repr

    @staticmethod
    def _generate_differences(init_values: list[int]) -> list[list[int]]:
        differences: list[list[int]] = [init_values]
        while any(differences[-1]):
            new_difference = []
            for i in range(len(differences[-1]) - 1):
                new_difference.append(differences[-1][i + 1] - differences[-1][i])
            differences.append(new_difference)
        return differences

    def predict_next_value(self):
        self.differences[-1].append(0)
        for i in range(len(self.differences) - 2, -1, -1):
            self.differences[i].append(self.differences[i][-1] + self.differences[i - 1][-1])
        self.differences[0][-1] = self.differences[0][-2] + self.differences[1][-1]

    def get_sum_of_final_values(self) -> int:
        return sum(difference[-1] for difference in self.differences)


class Day9(DayBase):
    
    def __init__(self):
        super().__init__()
        histories = self.parse()
        self.histories: list[History] = [History(history) for history in histories]


    def parse(self) -> list[list[str]]:
        return [line.split() for line in self.input]
    
    @override
    def part_1(self) -> int:
        return sum(history.get_sum_of_final_values() for history in self.histories)

    @override
    def part_2(self) -> int:
        pass

if __name__ == "__main__":
    day9 = Day9()
    print(day9.part_1())
    print(day9.part_2())
