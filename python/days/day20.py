from overrides import override
from aoc23_base import DayBase
from enum import Enum, Flag, auto
from abc import ABCMeta, abstractmethod
import string
from collections import deque

class PulseType(Flag):
    HIGH = True
    LOW = False

class ModuleType(Enum):
    FLIPFLOP = auto(),
    CONJUNCTION = auto(),
    BROADCASTER = auto(),

    @classmethod
    def from_str(cls, c: str) -> 'ModuleType':
        match c[0]:
            case '%':
                return ModuleType.FLIPFLOP
            case '&':
                return ModuleType.CONJUNCTION
            case 'b':
                return ModuleType.BROADCASTER
            case _:
                raise RuntimeError(f"ModuleType {c} is not recognised.")


class Pulse:

    def __init__(self, pulse_type: PulseType = PulseType.LOW):
        self.pulse_type: PulseType = pulse_type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.pulse_type})"

    def flip(self) -> 'Pulse':
        self.pulse_type = ~self.pulse_type
        return self

class Message:

    number_of_high_pulses: int = 0
    number_of_low_pulses: int = 0

    def __init__(self, pulse: Pulse, source_name: str, destination_str: str):
        self.pulse: Pulse = pulse
        self.source_name: str = source_name
        self.destination_str: str = destination_str

        self.update_tallies()
        print(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.pulse}, source={self.source_name}, destination={self.destination_str})"

    def update_tallies(self) -> None:
        match self.pulse.pulse_type:
            case PulseType.HIGH:
                Message.number_of_high_pulses += 1
            case PulseType.LOW:
                Message.number_of_low_pulses += 1
            case _:
                raise RuntimeError(f"PulseType {self.pulse.pulse_type} is not recognised.")
        

class ModuleBase(metaclass=ABCMeta):
    
    def __init__(self, name: str, destinations_str: list[str]):
        self.name: str = name
        self.destinations_str: list[str] = destinations_str
        self.sources_str: list[str] = [] # might be redundant
        # self.sources: list[ModuleBase] = [] # might be redundant
        # self.destinations: list[ModuleBase] = []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, sources={self.sources_str}, destinations={self.destinations_str})"

    @abstractmethod
    def handle(self, message: Message) -> list[Message]:
        pass

    # def add_destination(self, module: 'ModuleBase') -> None:
    #     self.destinations.append(module)

    def add_source(self, module: 'ModuleBase') -> None:
    #     self.sources.append(module)
        self.sources_str.append(module.name)

    @staticmethod
    def create_from_str(type_and_name: str, destinations: str) -> 'ModuleBase':
        module_type = ModuleType.from_str(type_and_name)

        if type_and_name[0] not in string.ascii_letters:
            name = type_and_name[1:]
        else:
            name = type_and_name

        split_destinations: list[str] = destinations.split(', ')
        
        match module_type:
            case ModuleType.FLIPFLOP:
                return FlipFlop(name, split_destinations)
            case ModuleType.CONJUNCTION:
                return Conjunction(name, split_destinations)
            case ModuleType.BROADCASTER:
                return Broadcast(name, split_destinations)
            case _:
                raise RuntimeError(f"ModuleType {module_type} is not recognised.")



class FlipFlop(ModuleBase):

    def __init__(self, name: str, destinations_str: list[str]):
        super().__init__(name, destinations_str)
        self.state: bool = False

    @override
    def handle(self, message: Message) -> list[Message]:

        if message.pulse.pulse_type is PulseType.HIGH:
            return []
        
        self.state = not self.state
        message.pulse.flip()
        return [Message(message.pulse, self.name, destination) for destination in self.destinations_str]


class Conjunction(ModuleBase):

    def __init__(self, name: str, destinations_str: list[str]):
        super().__init__(name, destinations_str)
        self.sources_memory_dict: dict[str, Pulse] = {}

    @override
    def handle(self, message: Message) -> list[Message]:
        assert message.source_name

        assert message.source_name in self.sources_memory_dict
        self.sources_memory_dict[message.source_name] = message.pulse
        if all(pulse_memory.pulse_type for pulse_memory in self.sources_memory_dict.values()):
            pulse_to_send = Pulse(PulseType.HIGH)
        else:
            pulse_to_send = Pulse(PulseType.LOW)
        return [Message(pulse_to_send, self.name, destination) for destination in self.destinations_str]

    def add_source(self, module: ModuleBase) -> None:
        super().add_source(module)
        self.sources_memory_dict[module.name] = Pulse()
        

class Broadcast(ModuleBase):

    def handle(self, message: Message) -> list[Message]:
        return [Message(message.pulse, self.name, destination) for destination in self.destinations_str]
        

class Button(ModuleBase):

    def handle(self, message: Message) -> list[Message]:
        return [Message(message.pulse, self.name, destination) for destination in self.destinations_str]


class Motherboard:
    
    def __init__(self, modules: list[ModuleBase]):
        self.modules: dict[str, ModuleBase] = {module.name : module for module in modules}
        self._link_modules()

        self.deque: deque[Message] = deque(self.modules["BUTTON"].handle(Message(Pulse(), "MOTHERBOARD", "BUTTON")))

    def _link_modules(self) -> None:
        for module_name, module in self.modules.items():
            for destination_name in module.destinations_str:
                # module.add_destination(self.modules[destination_name])
                self.modules[destination_name].add_source(module)

    def press_button(self, iterations: int):
        for _ in range(iterations):
            while self.deque:
                message = self.deque.popleft()
                new_messages = self.modules[message.destination_str].handle(message)
                self.deque.extendleft(new_messages)

class Day20(DayBase):
    
    def __init__(self):
        super().__init__()
        self.motherboard: Motherboard = Motherboard(self.parse())

    def parse(self) -> list[ModuleBase]:
        return [ModuleBase.create_from_str(*line.split(' -> ')) for line in self.input] + [Button("BUTTON", ["broadcaster"])]
                      
    @override
    def part_1(self) -> int:
        print(self.motherboard.modules.values())
        for module_name, module in self.motherboard.modules.items():
            print(module)

        self.motherboard.press_button(1)

        return Message.number_of_low_pulses, Message.number_of_high_pulses

    @override
    def part_2(self) -> int:
        pass

if __name__ == "__main__":
    day20 = Day20()
    print(day20.part_1())
    print(day20.part_2())
