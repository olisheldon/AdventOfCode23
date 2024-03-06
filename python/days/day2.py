from enum import StrEnum, auto
from overrides import override
from functools import reduce
from aoc23_base import DayBase


class DiceType(StrEnum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


class DiceBag:

    maximum_bag_contents = {
        DiceType.RED: 12,
        DiceType.GREEN: 13,
        DiceType.BLUE: 14
    }

    def __init__(self):
        super().__init__()
        self._bag: dict[DiceType, int] = {die: 0 for die in DiceType}

    def valid(self) -> bool:
        if set(self._bag.keys()) != set(die for die in DiceType):
            raise RuntimeError(
                f"Trying to check validity of invalid die dice_set: {self._bag.items()}")

        for die in DiceType:
            if self._bag[die] > DiceBag.maximum_bag_contents[die]:
                return False
        return True

    def get_dice(self) -> dict[DiceType, int]:
        return self._bag.copy()

    def get_num_dice_of_type(self, die_type: DiceType) -> int:
        return self._bag[die_type]

    def set_num_dice_of_type(self, die_type: DiceType, val: int) -> None:
        self._bag[die_type] = val

    def update_max(self, dice_set: 'DiceBag') -> None:
        for die in DiceType:
            if dice_set.get_num_dice_of_type(die) > self._bag[die]:
                self._bag[die] = dice_set.get_num_dice_of_type(die)


class Game:

    def __init__(self, game_id: int):
        self.game_id: int = game_id
        self.dice_sets: list[DiceBag] = []
        self.max_dice_set: DiceBag = DiceBag()

    def add_set(self, dice_set: DiceBag) -> None:
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
                set_of_dice = DiceBag()
                for num_and_colour in dice_set.split(','):
                    num, colour = num_and_colour.split()
                    dice_colour = DiceType(colour)
                    set_of_dice.set_num_dice_of_type(dice_colour, int(num))
                game.add_set(set_of_dice)
            games.append(game)
        return games

    @override
    def part_1(self) -> int:
        return sum(game.game_id for game in self.games if game.valid())

    @override
    def part_2(self) -> int:
        max_dice_required_per_game = (
            game.max_dice_set.get_dice().values() for game in self.games)
        power = 0
        for max_dice_nums in max_dice_required_per_game:
            power += reduce((lambda x, y: x * y), max_dice_nums)
        return power


if __name__ == "__main__":
    day2 = Day2()
    print(day2.part_1())
    print(day2.part_2())
