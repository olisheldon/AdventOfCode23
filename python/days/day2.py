from enum import StrEnum, auto
from collections import UserDict
from overrides import override
from functools import reduce
from aoc23_base import DayBase

class Dice(StrEnum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


class DiceDict(UserDict):

    maximum_bag_contents = {
        Dice.RED : 12,
        Dice.GREEN : 13,
        Dice.BLUE : 14
    }

    def __init__(self):
        super().__init__()
        for die in Dice:
            self.update({die:0})


    def valid(self) -> bool:
        if set(self.keys()) != set(die for die in Dice):
            raise RuntimeError(f"Trying to check validity of invalid die dice_set: {self.items()}")

        for die in Dice:
            if self[die] > DiceDict.maximum_bag_contents[die]:
                return False
        return True
    
    def update_max(self, dice_set: 'DiceDict') -> None:
        for die in Dice:
            if dice_set[die] > self[die]:
                self[die] = dice_set[die]

    
class Game:
    
    def __init__(self, id: int):
        self.id: int = id
        self.dice_sets: list[DiceDict] = []
        self.max_dice_set: DiceDict = DiceDict()

    def add_set(self, dice_set: DiceDict) -> None:
        self.max_dice_set.update_max(dice_set)
        self.dice_sets.append(dice_set)

    def valid(self) -> bool:
        for dice_set in self.dice_sets:
            if not dice_set.valid():
                return False
        return True

class Day2(DayBase):

    def __init__(self):
        super().__init__()
        self.games: list[Game] = self.parse()
    
    def parse(self) -> list[Game]:
        games = []
        for line in self.input:
            game = Game(int(line.split()[1][:-1]))
            info = line[line.find(':')+2:]
            dice_sets = info.split(';')
            for dice_set in dice_sets:
                set_of_dice = DiceDict()
                for num_and_colour in dice_set.split(','):
                    num, colour = num_and_colour.split()
                    dice_colour = Dice(colour)
                    set_of_dice[dice_colour] = int(num)
                game.add_set(set_of_dice)
            games.append(game)
        return games
    
    @override
    def part_1(self) -> int:
        return sum(game.id for game in self.games if game.valid())
    
    @override
    def part_2(self) -> int:
        max_dice_required_per_game = (game.max_dice_set.values() for game in self.games)
        power = 0
        for max_dice_nums in max_dice_required_per_game:
            power += reduce((lambda x, y: x * y), max_dice_nums)
        return power

    

            
if __name__ == "__main__":
    day2 = Day2()
    print(day2.part_1())
    print(day2.part_2())