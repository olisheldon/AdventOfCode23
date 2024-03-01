from overrides import override
from aoc23_base import DayBase
from enum import Enum, auto
import abc

class Operation(Enum):
    EQUALS = auto()
    MINUS = auto()

    @classmethod
    def from_str(cls, s: str) -> 'Operation':
        if '=' in s and '-' not in s:
            return cls.EQUALS
        if '-' in s and '=' not in s:
            return cls.MINUS
        raise RuntimeError(f"String {s} does not contain only equals or minus.")

    @classmethod
    def from_char(cls, c: str) -> 'Operation':
        match c:
            case '=':
                return cls.EQUALS
            case '-':
                return cls.MINUS
            case _:
                raise RuntimeError(f"Char {c} is not recognised.")
                       
    @classmethod
    def from_operation(cls, s: 'Operation') -> str:
        match s:
            case cls.EQUALS:
                return '-'
            case cls.MINUS:
                return '='
            case _:
                raise RuntimeError(f"Operation {s} is not recognised.")
    
class Hasher:

    @staticmethod
    def hash_value(s: str) -> int:
        '''
        Determine the ASCII code for the current character of the string.
        Increase the current focal_length by the ASCII code you just determined.
        Set the current focal_length to itself multiplied by 17.
        Set the current focal_length to the remainder of dividing itself by 256.
        '''
        current_value = 0
        for c in s:
            ascii_value = ord(c)
            current_value += ascii_value
            current_value *= 17
            current_value %= 256
        return current_value

class InitSequenceElementBase(abc.ABC):

    def __init__(self, operation: Operation, name: str):
        self.operation: Operation = operation
        self.name: str = name
        self.hash_value: int = Hasher.hash_value(name)
    
    @classmethod
    def create_init_sequence_element(cls, s: str) -> 'InitSequenceElementBase':
        if '=' in s:
            name, val = s.split('=')
            return EqualInitSequenceElement(name, int(val))
        elif '-' in s:
            name = s[:-1]
            return MinusInitSequenceElement(name)
        raise RuntimeError(f"SequenceElement {s} is invalid.")
            
    @abc.abstractmethod
    def operate_on_boxes(self, boxes: 'Boxes') -> None:
        pass

class EqualInitSequenceElement(InitSequenceElementBase):

    def __init__(self, name: str, value: int):
        super().__init__(Operation.EQUALS, name)
        self.value: int = value

    @override
    def operate_on_boxes(self, boxes: 'Boxes') -> None:
        boxes.add(self.name, self.hash_value, self.value)


class MinusInitSequenceElement(InitSequenceElementBase):

    def __init__(self, name: str):
        super().__init__(Operation.MINUS, name)

    @override
    def operate_on_boxes(self, boxes: 'Boxes') -> None:
        boxes.remove(self.name, self.hash_value)

class Boxes:

    def __init__(self):
        self.boxes: list[list[str]] = [[] for _ in range(256)]
        self.focal_length_map: dict[str, int] = {}

    def process_sequence(self, sequence: list[InitSequenceElementBase]) -> None:
        for element in sequence:
            element.operate_on_boxes(self)
    
    def remove(self, name: str, hash_value: int) -> None:
        if name in self.boxes[hash_value]:
            self.boxes[hash_value].remove(name)
    
    def add(self, name: str, hash_value: int, value: int) -> None:
        if name not in self.boxes[hash_value]:
            self.boxes[hash_value].append(name)
        self.focal_length_map[name] = value
    
    @property
    def focusing_power(self) -> int:
        focusing_power = 0
        for box_index, box in enumerate(self.boxes):
            for lens_index, name in enumerate(box):
                focusing_power += (box_index + 1) * (lens_index + 1) * self.focal_length_map[name]
        return focusing_power


class Day15(DayBase):
    
    def __init__(self):
        super().__init__()
        

    def parse(self) -> list[str]:
        return self.input[0].split(',')

    @override
    def part_1(self) -> int:
        return sum(map(Hasher.hash_value, self.parse()))

    @override
    def part_2(self) -> int:
        sequence_elements: list[InitSequenceElementBase] = [InitSequenceElementBase.create_init_sequence_element(s) for s in self.parse()]
        boxes = Boxes()
        boxes.process_sequence(sequence_elements)
        return boxes.focusing_power



if __name__ == "__main__":
    day15 = Day15()
    print(day15.part_1())
    print(day15.part_2())
