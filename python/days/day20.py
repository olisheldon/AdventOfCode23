from overrides import override
from aoc23_base import DayBase
from enum import Enum, Flag, auto
from abc import ABCMeta, abstractmethod
import string
from collections import deque

class PulseType(Flag):
    HIGH = True
    LOW = False

    @classmethod
    def default(cls) -> 'PulseType':
        return cls.LOW

    @classmethod
    def flip(cls, pulse_type: 'PulseType', predicate: bool = True) -> 'PulseType':
        if predicate:
            return ~pulse_type
        else:
            return pulse_type

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

class Message:

    number_of_high_pulses: int = 0
    number_of_low_pulses: int = 0

    def __init__(self, pulse_type: PulseType, source_name: str, destination_str: str):
        self.pulse_type: PulseType = pulse_type
        self.source_name: str = source_name
        self.destination_str: str = destination_str

        self.update_tallies()

    def __repr__(self) -> str:
        return f"{self.source_name} -{self.pulse_type}-> {self.destination_str}"

    def update_tallies(self) -> None:
        match self.pulse_type:
            case PulseType.HIGH:
                Message.number_of_high_pulses += 1
            case PulseType.LOW:
                Message.number_of_low_pulses += 1
            case _:
                raise RuntimeError(f"PulseType {self.pulse_type} is not recognised.")
        

class ModuleBase(metaclass=ABCMeta):
    
    def __init__(self, name: str, destinations_str: list[str]):
        self.name: str = name
        self.destinations_str: list[str] = destinations_str
        self.sources_str: list[str] = [] # populated by motherboard once all modules are created

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, sources={self.sources_str}, destinations={self.destinations_str})"

    @abstractmethod
    def handle(self, message: Message) -> list[Message]:
        pass

    def add_source(self, module_name: str) -> None:
        self.sources_str.append(module_name)

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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, state={self.state}, sources={self.sources_str}, destinations={self.destinations_str})"

    @override
    def handle(self, message: Message) -> list[Message]:

        if message.pulse_type is PulseType.HIGH:
            return []
        
        self.state = not self.state
        return [Message(PulseType.flip(message.pulse_type, self.state), self.name, destination) for destination in self.destinations_str]


class Conjunction(ModuleBase):

    def __init__(self, name: str, destinations_str: list[str]):
        super().__init__(name, destinations_str)
        self.sources_memory_dict: dict[str, PulseType] = {}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, sources_memory={self.sources_memory_dict}, sources={self.sources_str}, destinations={self.destinations_str})"

    @override
    def handle(self, message: Message) -> list[Message]:
        assert message.source_name

        assert message.source_name in self.sources_memory_dict
        self.sources_memory_dict[message.source_name] = message.pulse_type
        if all(pulse_memory is PulseType.HIGH for pulse_memory in self.sources_memory_dict.values()):
            pulse_to_send = PulseType.LOW
        else:
            pulse_to_send = PulseType.HIGH
        return [Message(pulse_to_send, self.name, destination) for destination in self.destinations_str]

    def add_source(self, module_name: str) -> None:
        super().add_source(module_name)
        self.sources_memory_dict[module_name] = PulseType.default()
        

class Broadcast(ModuleBase):

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, sources={self.sources_str}, destinations={self.destinations_str})"
    
    def handle(self, message: Message) -> list[Message]:
        return [Message(message.pulse_type, self.name, destination) for destination in self.destinations_str]
        

class Button(ModuleBase):

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, sources={self.sources_str}, destinations={self.destinations_str})"
    
    def handle(self, message: Message) -> list[Message]:
        return [Message(message.pulse_type, self.name, destination) for destination in self.destinations_str]

class Exit(ModuleBase):

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, sources={self.sources_str}, destinations={self.destinations_str})"
    
    def handle(self, message: Message) -> list[Message]:
        return []


class Motherboard:
    
    def __init__(self, modules: list[ModuleBase]):
        self.modules: dict[str, ModuleBase] = {module.name : module for module in modules}
        self._create_exit_modules()
        self._link_modules()

        self.message_log: list[Message] = list()
        self.deque: deque[Message] = deque()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: " + "\n".join(str(module) for (name, module) in self.modules.items())

    def _create_exit_modules(self) -> None:
        module_names = self.modules.keys()
        missing_module_names: list[str] = []
        for module_name, module in self.modules.items():
            for destination_name in module.destinations_str:
                if destination_name not in module_names:
                    missing_module_names.append(destination_name)
        
        for missing_module_name in missing_module_names:
            self.modules[missing_module_name] = Exit(missing_module_name, [])
                    


    def _link_modules(self) -> None:
        for module_name, module in self.modules.items():
            for destination_name in module.destinations_str:
                self.modules[destination_name].add_source(module_name)
                    

    def press_button(self, iterations: int):
        for _ in range(iterations):
            button_message = self.modules["broadcaster"].handle(Message(PulseType.LOW, "button", "broadcaster"))
            self.message_log.extend(button_message)
            self.deque.extend(button_message)
            while self.deque:
                message = self.deque.popleft()
                new_messages = self.modules[message.destination_str].handle(message)
                self.message_log.extend(new_messages)
                self.deque.extend(new_messages)

class Day20(DayBase):
    
    def __init__(self):
        super().__init__()
        self.motherboard: Motherboard = Motherboard(self.parse())

    def parse(self) -> list[ModuleBase]:
        return [ModuleBase.create_from_str(*line.split(' -> ')) for line in self.input]
                      
    @override
    def part_1(self) -> int:

        self.motherboard.press_button(1000)

        return Message.number_of_low_pulses * Message.number_of_high_pulses

    @override
    def part_2(self) -> int:
        pass

if __name__ == "__main__":
    day20 = Day20()
    print(day20.part_1())
    print(day20.part_2())
