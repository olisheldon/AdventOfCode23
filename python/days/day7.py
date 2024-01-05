from overrides import override
from aoc23_base import DayBase
from enum import auto, IntEnum
from collections import Counter, OrderedDict
from itertools import cycle



class Card(IntEnum):
    TWO = auto(),
    THREE = auto(),
    FOUR = auto(),
    FIVE = auto(),
    SIX = auto(),
    SEVEN = auto(),
    EIGHT = auto(),
    NINE = auto(),
    TEN = auto(),
    JACK = auto(),
    QUEEN = auto(),
    KING = auto(),
    ACE = auto(),

# class CardWithJoker(IntEnum):
#     JACK = auto(),
#     TWO = auto(),
#     THREE = auto(),
#     FOUR = auto(),
#     FIVE = auto(),
#     SIX = auto(),
#     SEVEN = auto(),
#     EIGHT = auto(),
#     NINE = auto(),
#     TEN = auto(),
#     QUEEN = auto(),
#     KING = auto(),
#     ACE = auto(),


class HandType(IntEnum):
    HIGH_CARD = auto(),
    ONE_PAIR = auto(),
    TWO_PAIR = auto(),
    THREE_OF_A_KIND = auto(),
    FULL_HOUSE = auto(),
    FOUR_OF_A_KIND = auto(),
    FIVE_OF_A_KIND = auto(),

class SecondaryCheck(IntEnum):
    LOSE = auto(),
    DRAW = auto(),
    WIN = auto(),

class Hand:

    def __init__(self, cards: tuple[Card, Card, Card, Card, Card], primary_ranking):
        self.cards: tuple[Card, Card, Card, Card, Card] = cards
        self.primary_ranking: HandType = primary_ranking(self.cards)

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
        if self.primary_ranking == other.primary_ranking:
            match self.secondary_comparison(other):
                case SecondaryCheck.WIN:
                    return False
                case SecondaryCheck.DRAW:
                    return False
                case SecondaryCheck.LOSE:
                    return True
        return self.primary_ranking < other.primary_ranking
        
    def __le__(self, other: 'Hand') -> bool:
        if self.primary_ranking == other.primary_ranking:
            match self.secondary_comparison(other):
                case SecondaryCheck.WIN:
                    return False
                case SecondaryCheck.DRAW:
                    return True
                case SecondaryCheck.LOSE:
                    return True
        return self.primary_ranking < other.primary_ranking

    def __eq__(self, other: 'Hand') -> bool:
        return self.cards == other.cards
        
    def __ne__(self, other: 'Hand') -> bool:
        return not self.__eq__(other)
        
    def __gt__(self, other: 'Hand') -> bool:
        return not self.__lt__(other)
        
    def __ge__(self, other: 'Hand') -> bool:
        return not self.__le__(other)

class Player:
    
    def __init__(self, cards: tuple[Card, Card, Card, Card, Card], bid: int, primary_ranking):
        self.hand = Hand(cards, primary_ranking)
        self.bid: int = bid
    
    def __lt__(self, other: 'Player') -> bool:
        return self.hand.__lt__(other.hand)

    def __le__(self, other: 'Player') -> bool:
        return self.hand.__le__(other.hand)

    def __eq__(self, other: 'Player') -> bool:
        return self.hand.__eq__(other.hand)

    def __ne__(self, other: 'Player') -> bool:
        return self.hand.__ne__(other.hand)

    def __gt__(self, other: 'Player') -> bool:
        return self.hand.__gt__(other.hand)
        
    def __ge__(self, other: 'Player') -> bool:
        return self.hand.__ge__(other.hand)



class Day7(DayBase):
    
    def __init__(self):
        super().__init__()
        self.list_of_cards: list[str] = []
        self.bids: list[int] = []
        self.list_of_cards, self.bids = self.parse()

        # self.players: list[Player] = [] # can only be created once we know the properties of the deck

    def create_players(self, list_of_cards: list[str], bids: list[int], CardEnum, primary_ranking) -> list[Player]:
        players = []
        for cards, bid in zip(list_of_cards, bids):
            enum_cards = tuple(CardEnum.create_card(c) for c in cards)
            players.append(Player(enum_cards, bid, primary_ranking))
        return players

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
        card_order = "AKQJT98765432"
        CardEnum = EnumBuilder(card_order).DeckEnum

        def primary_ranking(cards: tuple[Card, Card, Card, Card, Card]) -> 'HandType':
            unique_cards = set(cards)
            counter = Counter(cards)
            match len(unique_cards):
                case 1:
                    return HandType.FIVE_OF_A_KIND
                case 2:
                    if max(counter.values()) == 4:
                        return HandType.FOUR_OF_A_KIND
                    else:
                        return HandType.FULL_HOUSE
                case 3:
                    if max(counter.values()) == 3:
                        return HandType.THREE_OF_A_KIND
                    else:
                        return HandType.TWO_PAIR
                case 4:
                    return HandType.ONE_PAIR
                case 5:
                    return HandType.HIGH_CARD
            raise RuntimeError("did not recognise card")

        players = self.create_players(self.list_of_cards, self.bids, CardEnum, primary_ranking)

        result = 0
        for i, player in enumerate(sorted(players)):
            result += (i + 1) * player.bid
        return result


    @override
    def part_2(self) -> int:
        card_order = "AKQT98765432J"
        CardEnum = EnumBuilder(card_order).DeckEnum

        def primary_ranking(cards: tuple[Card, Card, Card, Card, Card]) -> 'HandType':
            cards_without_jack = [card for card in Card if not Card.JACK]

            possible_cards: list[list[Card]] = [[]]
            for i in range(len(cards)):
                if cards[i] is not Card.JACK:
                    for k in range(len(possible_cards)):
                        possible_cards[k].append(cards[i])
                else:
                    possible_cards = len(cards_without_jack) * possible_cards
                    for j in range(len(possible_cards)):
                        cycle_cards = cycle(cards_without_jack)
                        possible_cards[j].append(next(cycle_cards))

            best_hand: HandType = HandType.HIGH_CARD
            for possible_card in possible_cards:
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
                        raise RuntimeError("did not recognise card")
            return best_hand


            
        players = self.create_players(self.list_of_cards, self.bids, CardEnum, primary_ranking)

        result = 0
        for i, player in enumerate(sorted(players)):
            result += (i + 1) * player.bid
        return result
    
class EnumBuilder:

    def __init__(self, card_order: str):
        self.DeckEnum = IntEnum("CustomCard", OrderedDict((card, auto()) for card in card_order))
        self.DeckEnum.create_card = EnumBuilder.create_card
    
    @staticmethod
    def create_card(c: str):
        match c:
            case "A":
                return Card.ACE
            case "K":
                return Card.KING
            case "Q":
                return Card.QUEEN
            case "J":
                return Card.JACK
            case "T":
                return Card.TEN
            case "9":
                return Card.NINE
            case "8":
                return Card.EIGHT
            case "7":
                return Card.SEVEN
            case "6":
                return Card.SIX
            case "5":
                return Card.FIVE
            case "4":
                return Card.FOUR
            case "3":
                return Card.THREE
            case "2":
                return Card.TWO
        raise RuntimeError(f"Card string {c} not recognised.")