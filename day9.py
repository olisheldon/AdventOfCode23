from pathlib import Path
import argparse


def extrapolate(subhistory: list[int], forwards: bool = True) -> int:
    if all(val == 0 for val in subhistory):
        return 0

    deltas: list[int] = [y - x for x, y in zip(subhistory, subhistory[1:])]
    diff: int = extrapolate(deltas, forwards)

    if not forwards:
        return subhistory[0] - diff
    return subhistory[-1] + diff


class Day9:

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.histories: list[list[int]] = [
            list(map(int, x)) for x in self.parse()]

    def parse_file(self) -> list[str]:
        with open(self.filepath, 'r', encoding="utf-8") as f:
            return f.read().splitlines()

    def parse(self) -> list[list[str]]:
        return [line.split() for line in self.parse_file()]

    def part_1(self) -> int:
        return sum(extrapolate(history) for history in self.histories)

    def part_2(self) -> int:
        return sum(extrapolate(history, forwards=False) for history in self.histories)


if __name__ == "__main__":
    INPUT_FILEPATH = Path(__file__).parent / "data" / \
        f"{Path(__file__).stem}.txt"
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?',
                        default=INPUT_FILEPATH, help=f"Path to data for {Path(__file__).stem}")
    args = parser.parse_args()

    day9 = Day9(Path(args.input).absolute())
    print(day9.part_1())
    print(day9.part_2())
