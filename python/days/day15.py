from overrides import override
from collections import deque
from aoc23_base import DayBase
from enum import Enum, auto


class Operation(Enum):
    EQUALS = auto(),
    MINUS = auto(),

    @classmethod
    def from_str(cls, c: str) -> 'Operation':
        match c:
            case '=':
                return cls.EQUALS
            case '-':
                return cls.MINUS
            case _:
                raise RuntimeError(f"Operation {c} is not recognised.")
                       
    @classmethod
    def from_platform_object(cls, s: 'Operation') -> str:
        match s:
            case cls.EQUALS:
                return '-'
            case cls.MINUS:
                return '#'
            case _:
                raise RuntimeError(f"Operation {s} is not recognised.")
    
            
class Hasher:

    @staticmethod
    def hash(s: str) -> int:
        # Determine the ASCII code for the current character of the string.
        # Increase the current focal_length by the ASCII code you just determined.
        # Set the current focal_length to itself multiplied by 17.
        # Set the current focal_length to the remainder of dividing itself by 256.
        current_value = 0
        for c in s:
            ascii_value = ord(c)
            current_value += ascii_value
            current_value *= 17
            current_value %= 256
        return current_value


class InitSequenceElement:

    def __init__(self, s: str):
        hash_value = None
        operation = None
        label = None
        focal_length = None
        for c in ['-', '=']:
            if c in s:
                label: str = s.split(c)[0]
                hash_value: int = Hasher.hash(s.split(c)[0])
                operation: Operation = Operation.from_str(c)
                if operation is Operation.EQUALS:
                    focal_length = int(s.split(c)[-1])
        self.hash_value: int = hash_value
        self.label = label
        self.operation: Operation = operation
        self.focal_length: None | int = focal_length or None
    
    def __eq__(self, other: 'InitSequenceElement'):
        return self.label == other.label


class Day15(DayBase):
    
    def __init__(self):
        super().__init__()
        self.boxes: list[deque[InitSequenceElement]] = [deque() for _ in range(256)]

    def parse(self) -> list[str]:
        return self.input[0].split(',')

    @override
    def part_1(self) -> int:
        return sum(Hasher.hash(s) for s in self.parse())
        

    @override
    def part_2(self) -> int:
        sequence_elements = [InitSequenceElement(s) for s in self.parse()]
        for sequence_element in sequence_elements:
            print(sequence_element)
            box = self.boxes[sequence_element.hash_value]
            match sequence_element.operation:
                case Operation.MINUS:
                    for i, already_present_sequence_element in enumerate(box):
                        if sequence_element == already_present_sequence_element:
                            del box[i]
                            break
                case Operation.EQUALS:
                    assigned = False
                    for i, already_present_sequence_element in enumerate(box):
                        if sequence_element == already_present_sequence_element:
                            box[i] = sequence_element
                            assigned = True
                            break
                    if not assigned:
                        box.append(sequence_element)
                case _:
                    raise RuntimeError(f"operation {sequence_element.operation} not recognised.")
        
        print(sequence_elements)
        for box in self.boxes:
            print(box)


        score = 0
        for box_number, box in enumerate(self.boxes):
            for sequence_number, sequence_element in enumerate(box):
                score += (box_number + 1) * (sequence_number + 1) * (sequence_element.focal_length)
        return score





if __name__ == "__main__":
    day15 = Day15()
    print(day15.part_1())
    print(day15.part_2())
