from enum import StrEnum, auto
from dataclasses import dataclass
from collections import UserDict
import pandas
from IPython import embed

class Dice(StrEnum):
    RED = auto(),
    GREEN = auto(),
    BLUE = auto()


class DiceSet(UserDict):

    maximum_bag_contents = {
        Dice.RED : 12,
        Dice.GREEN : 13,
        Dice.BLUE : 14
    }

    def __init__(self):
        super().__init__()
        for dice in Dice:
            self.update({dice:0})


    def valid(self) -> bool:
        if set(self.keys()) != set(dice for dice in Dice):
            raise RuntimeError(f"Trying to check validity of invalid dice set: {self.items()}")

        for dice in Dice:
            if self[dice] > DiceSet.maximum_bag_contents[dice]:
                return False
        return True

    
class Game:
    
    def __init__(self, id: int):
        self.id: int = id
        self.sets: list[DiceSet] = []

    def add_set(self, set: DiceSet) -> None:
        self.sets.append(set)

    def valid(self) -> bool:
        for set in self.sets:
            if not set.valid():
                return False
        return True

class Day2:

    def __init__(self):
        self.input: list[str] = Day2.get_input()
        self.games: list[Game] = self.parse()
        

    @staticmethod
    def get_input() -> list[str]:
        with open("input.txt", 'r') as f:
            lines = f.read().splitlines()
        return lines
    
    def parse(self) -> list[Game]:
        games = []
        for line in self.input:
            game = Game(int(line.split()[1][:-1]))
            info = line[line.find(':')+2:]
            sets = info.split(';')
            for set in sets:
                dice_set = DiceSet()
                for num_and_colour in set.split(','):
                    num, colour = num_and_colour.split()
                    dice_colour = Dice(colour)
                    dice_set[dice_colour] = int(num)
                game.add_set(dice_set)
            games.append(game)
        return games
    
    def part1(self):
        valid_ids = self.get_valid_game_ids()
        return sum(valid_ids)
    
    def get_valid_game_ids(self) -> list[int]:
        ids = []
        for game in self.games:
            if game.valid():
                ids.append(game.id)
        return ids
    

            
if __name__ == "__main__":
    day2 = Day2()
    print(day2.part1())