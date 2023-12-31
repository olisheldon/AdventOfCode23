from overrides import override

from aoc23_base import DayBase

class WinningNumbers(set):
    pass
    
    # def __init__(self, winning_numbers: list[int]):
    #     self.winning_numbers: set[int] = set(winning_numbers)

class ScratchcardNumbers(set):
    pass
    
    # def __init__(self, scratchcard_numbers: list[int]):
    #     self.scratchcard_numbers: set[int] = set(scratchcard_numbers)

class Scratchcard:
    
    def __init__(self, scratchcard_numbers: list[int], winning_numbers: list[int]):
        self.scratchcard_numbers = ScratchcardNumbers(scratchcard_numbers)
        self.winning_numbers = WinningNumbers(winning_numbers)
        self.number_of_winners: int = len(self.scratchcard_numbers.intersection(self.winning_numbers)) 

class MultipleScratchcards(list):

    def __init__(self, scratchcards: list[Scratchcard]):
        super(MultipleScratchcards, self).__init__(scratchcards)
        self.number_of_scratchcards: list[int] = [1 for i in range(len(scratchcards))]



class Day4(DayBase):
    
    def __init__(self):
        super().__init__()
        self.multiple_scratchcards: MultipleScratchcards = MultipleScratchcards(self.parse())
    
    @override
    def part_1(self) -> int:
        return sum(int(2**(scratchcard.number_of_winners - 1)) for scratchcard in self.multiple_scratchcards)

    @override
    def part_2(self) -> int:
        i = 0
        while i < len(self.multiple_scratchcards):
            for _ in range(self.multiple_scratchcards.number_of_scratchcards[i]):
                for j in range(1, self.multiple_scratchcards[i].number_of_winners + 1):
                    if i + j < len(self.multiple_scratchcards):
                        self.multiple_scratchcards.number_of_scratchcards[i + j] += 1
                    else:
                        break
            i += 1
        return sum(self.multiple_scratchcards.number_of_scratchcards)
    
    def parse(self) -> list[Scratchcard]:
        scratchcards = []
        for line in self.input:
            numbers, winning_numbers = line.split('|')
            numbers, winning_numbers = numbers.split()[2:], winning_numbers.split()
            scratchcards.append(Scratchcard([int(num) for num in numbers], [int(winning_num) for winning_num in winning_numbers]))
        return scratchcards