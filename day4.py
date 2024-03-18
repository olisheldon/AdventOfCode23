from pathlib import Path
import argparse


class Scratchcard:

    def __init__(self, scratchcard_numbers: list[int], winning_numbers: list[int]):
        self.scratchcard_numbers: set[int] = set(scratchcard_numbers)
        self.winning_numbers: set[int] = set(winning_numbers)
        self.number_of_winners: int = len(
            self.scratchcard_numbers.intersection(self.winning_numbers))


class MultipleScratchcards(list):

    def __init__(self, scratchcards: list[Scratchcard]):
        super(MultipleScratchcards, self).__init__(scratchcards)
        self.number_of_scratchcards: list[int] = [
            1 for _ in range(len(scratchcards))]


class Day4:

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.multiple_scratchcards: MultipleScratchcards = MultipleScratchcards(
            self.parse())

    def part_1(self) -> int:
        return sum(int(2**(scratchcard.number_of_winners - 1)) for scratchcard in self.multiple_scratchcards)

    def part_2(self) -> int:
        i = 0
        while i < len(self.multiple_scratchcards):
            for j in range(1, self.multiple_scratchcards[i].number_of_winners + 1):
                if i + j < len(self.multiple_scratchcards):
                    self.multiple_scratchcards.number_of_scratchcards[i +
                                                                      j] += self.multiple_scratchcards.number_of_scratchcards[i]
                else:
                    break
            i += 1
        return sum(self.multiple_scratchcards.number_of_scratchcards)

    def parse_file(self) -> list[str]:
        with open(self.filepath, 'r', encoding="utf-8") as f:
            return f.read().splitlines()

    def parse(self) -> list[Scratchcard]:
        scratchcards = []
        for line in self.parse_file():
            numbers, winning_numbers = line.split('|')
            numbers, winning_numbers = numbers.split()[
                2:], winning_numbers.split()
            scratchcards.append(Scratchcard([int(num) for num in numbers], [
                                int(winning_num) for winning_num in winning_numbers]))
        return scratchcards


if __name__ == "__main__":
    INPUT_FILEPATH = Path(__file__).parent / "data" / \
        f"{Path(__file__).stem}.txt"
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?',
                        default=INPUT_FILEPATH, help=f"Path to data for {Path(__file__).stem}")
    args = parser.parse_args()

    day4 = Day4(Path(args.input).absolute())
    print(day4.part_1())
    print(day4.part_2())
