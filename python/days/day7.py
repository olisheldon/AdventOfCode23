from overrides import override
from aoc23_base import DayBase
from enum import auto, IntEnum, EnumMeta
from collections import Counter
from itertools import cycle
from typing import Callable, Type

from dataclasses import dataclass, field

class CardHelperMixin:

    def __repr__(self) -> str:
        return self.card_to_char(self)
    
    @classmethod
    def assign_hand_type(cls, cards: tuple['Card', 'Card', 'Card', 'Card', 'Card']) -> 'HandType':
        raise RuntimeError("This should only be called by subclasses.")
    
    @classmethod
    def char_to_card(cls, c: str) -> 'Card':
        match c:
            case "A":
                return cls.ACE
            case "K":
                return cls.KING
            case "Q":
                return cls.QUEEN
            case "J":
                return cls.JACK
            case "T":
                return cls.TEN
            case "9":
                return cls.NINE
            case "8":
                return cls.EIGHT
            case "7":
                return cls.SEVEN
            case "6":
                return cls.SIX
            case "5":
                return cls.FIVE
            case "4":
                return cls.FOUR
            case "3":
                return cls.THREE
            case "2":
                return cls.TWO
        raise RuntimeError(f"Card {card} not recognised.")

    @classmethod
    def card_to_char(cls, card: 'Card') -> str:
        match card:
            case cls.ACE:
                return "A"
            case cls.KING:
                return "K"
            case cls.QUEEN:
                return "Q"
            case cls.JACK:
                return "J"
            case cls.TEN:
                return "T"
            case cls.NINE:
                return "9"
            case cls.EIGHT:
                return "8"
            case cls.SEVEN:
                return "7"
            case cls.SIX:
                return "6"
            case cls.FIVE:
                return "5"
            case cls.FOUR:
                return "4"
            case cls.THREE:
                return "3"
            case cls.TWO:
                return "2"
        raise RuntimeError(f"Card {card} not recognised.")

class Card(CardHelperMixin, IntEnum):
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    JACK = auto()
    QUEEN = auto()
    KING = auto()
    ACE = auto()

    @classmethod
    @override
    def assign_hand_type(cls, cards: tuple['Card', 'Card', 'Card', 'Card', 'Card']) -> 'HandType':
        unique_cards = set(cards)
        counter = Counter(cards)
        match len(unique_cards):
            case 1:
                return HandType.FIVE_OF_A_KIND
            case 2:
                if max(counter.values()) == 4:
                    return HandType.FOUR_OF_A_KIND
                return HandType.FULL_HOUSE
            case 3:
                if max(counter.values()) == 3:
                    return HandType.THREE_OF_A_KIND
                return HandType.TWO_PAIR
            case 4:
                return HandType.ONE_PAIR
            case 5:
                return HandType.HIGH_CARD
            case _:
                raise RuntimeError(f"Cards {cards} cannot be assigned a hand type.")

class CardWithJoker(CardHelperMixin, IntEnum):
    JACK = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    QUEEN = auto()
    KING = auto()
    ACE = auto()

    @classmethod
    @override
    def assign_hand_type(cls, cards: tuple['CardWithJoker', 'CardWithJoker', 'CardWithJoker', 'CardWithJoker', 'CardWithJoker']) -> 'HandType':
        cards_without_jack = [card for card in CardWithJoker if card != CardWithJoker.JACK]

        def possibilities(cards: tuple['CardWithJoker', 'CardWithJoker', 'CardWithJoker', 'CardWithJoker', 'CardWithJoker']) -> list[list[CardWithJoker]]:
            list_of_possible_cards = [[]]
            for card in cards:
                if card != CardWithJoker.JACK:
                    for possible_cards in list_of_possible_cards:
                        possible_cards.append(card)
                else:
                    list_of_possible_cards = [possible_cards.copy() for _ in range(len(cards_without_jack)) for possible_cards in list_of_possible_cards]
                    cycle_cards = cycle(cards_without_jack)
                    for possible_cards in list_of_possible_cards:
                        possible_cards.append(next(cycle_cards))
            return list_of_possible_cards
        
        best_hand: HandType = HandType.HIGH_CARD
        for possible_card in possibilities(cards):
            unique_cards = set(possible_card)
            counter = Counter(possible_card)
            match len(unique_cards):
                case 1:
                    best_hand = max(best_hand, HandType.FIVE_OF_A_KIND)
                case 2:
                    if max(counter.values()) == 4:
                        best_hand = max(best_hand, HandType.FOUR_OF_A_KIND)
                    else:
                        best_hand = max(best_hand, HandType.FULL_HOUSE)
                case 3:
                    if max(counter.values()) == 3:
                        best_hand = max(best_hand, HandType.THREE_OF_A_KIND)
                    else:
                        best_hand = max(best_hand, HandType.TWO_PAIR)
                case 4:
                    best_hand = max(best_hand, HandType.ONE_PAIR)
                case 5:
                    best_hand = max(best_hand, HandType.HIGH_CARD)
                case _:
                    raise RuntimeError(f"did not recognise card {len(unique_cards)}")
        return best_hand

class HandType(IntEnum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()

class SecondaryCheck(IntEnum):
    LOSE = auto()
    DRAW = auto()
    WIN = auto()

class Hand:

    def __init__(self, cards: tuple[Card, Card, Card, Card, Card]):
        self.cards: tuple[Card, Card, Card, Card, Card] = cards
        self.hand_type: HandType = cards[0].assign_hand_type(self.cards)

    def __repr__(self) -> str:
        return f"Hand(cards={self.cards} hand_type={self.hand_type.name})"

    def secondary_comparison(self, hand: 'Hand') -> SecondaryCheck:
        for my_card, other_card in zip(self.cards, hand.cards):
            if my_card == other_card:
                continue
            elif my_card > other_card:
                return SecondaryCheck.WIN
            else:
                return SecondaryCheck.LOSE
        return SecondaryCheck.DRAW
    
    def __lt__(self, other: 'Hand') -> bool:
        if self.hand_type == other.hand_type:
            match self.secondary_comparison(other):
                case SecondaryCheck.WIN:
                    return False
                case SecondaryCheck.DRAW:
                    return False
                case SecondaryCheck.LOSE:
                    return True
        return self.hand_type < other.hand_type
        
    def __le__(self, other: 'Hand') -> bool:
        if self.hand_type == other.hand_type:
            match self.secondary_comparison(other):
                case SecondaryCheck.WIN:
                    return False
                case SecondaryCheck.DRAW:
                    return True
                case SecondaryCheck.LOSE:
                    return True
        return self.hand_type < other.hand_type

    def __eq__(self, other: 'Hand') -> bool:
        return self.cards == other.cards
        
    def __ne__(self, other: 'Hand') -> bool:
        return not self.__eq__(other)
        
    def __gt__(self, other: 'Hand') -> bool:
        return not self.__lt__(other)
        
    def __ge__(self, other: 'Hand') -> bool:
        return not self.__le__(other)

class HandOfCards:
    
    def __init__(self, cards: tuple[Card, Card, Card, Card, Card], bid: int):
        self.hand = Hand(cards)
        self.bid: int = bid
    
    def __repr__(self) -> str:
        return f"{self.hand} {self.bid}"
    
    def __lt__(self, other: 'HandOfCards') -> bool:
        return self.hand.__lt__(other.hand)

    def __le__(self, other: 'HandOfCards') -> bool:
        return self.hand.__le__(other.hand)

    def __eq__(self, other: 'HandOfCards') -> bool:
        return self.hand.__eq__(other.hand)

    def __ne__(self, other: 'HandOfCards') -> bool:
        return self.hand.__ne__(other.hand)

    def __gt__(self, other: 'HandOfCards') -> bool:
        return self.hand.__gt__(other.hand)
        
    def __ge__(self, other: 'HandOfCards') -> bool:
        return self.hand.__ge__(other.hand)



class Day7(DayBase):
    
    def __init__(self):
        super().__init__()
        self.list_of_cards: list[str] = []
        self.bids: list[int] = []
        self.list_of_cards, self.bids = self.parse()

    def create_hands_of_cards(self, list_of_cards: list[str], bids: list[int], CardEnum: Type[CardHelperMixin]) -> list[HandOfCards]:
        hand_of_cards = []
        for cards, bid in zip(list_of_cards, bids):
            enum_cards = tuple(CardEnum.char_to_card(c) for c in cards)
            hand_of_cards.append(HandOfCards(enum_cards, bid))
        return hand_of_cards

    def parse(self) -> tuple[list[str], list[int]]:
        list_of_cards: list[str] = []
        bids: list[int] = []
        for line in self.input:
            split_line = line.split()
            list_of_cards.append(split_line[0])
            bids.append(int(split_line[1]))
        return list_of_cards, bids
    
    @override
    def part_1(self) -> int:

        hands_of_cards = self.create_hands_of_cards(self.list_of_cards, self.bids, Card)

        return sum((i + 1) * hand_of_cards.bid for (i, hand_of_cards) in enumerate(sorted(hands_of_cards)))


    @override
    def part_2(self) -> int:
            
        hands_of_cards = self.create_hands_of_cards(self.list_of_cards, self.bids, CardWithJoker)
        
        return sum((i + 1) * hand_of_cards.bid for (i, hand_of_cards) in enumerate(sorted(hands_of_cards)))
    
if __name__ == "__main__":
    day7 = Day7()
    print(day7.part_1())
    print(day7.part_2())
