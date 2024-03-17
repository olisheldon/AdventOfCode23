from pathlib import Path
import argparse
from overrides import override


class Day25:

    def __init__(self, filepath: Path):
        self.filepath = filepath

    def parse_file(self) -> list[str]:
        with open(self.filepath, 'r', encoding="utf-8") as f:
            return f.read().splitlines()

    def parse(self) -> list[str]:
        pass

    def part_1(self) -> int:
        pass

    def part_2(self) -> int:
        pass


if __name__ == "__main__":
    INPUT_FILEPATH = Path(__file__).parent / "data" / \
        f"{Path(__file__).stem}.txt"
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?',
                        default=INPUT_FILEPATH, help=f"Path to data for {Path(__file__).stem}")
    args = parser.parse_args()

    day25 = Day25(Path(args.input).absolute())
    print(day25.part_1())
    print(day25.part_2())
