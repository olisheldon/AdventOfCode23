from abc import abstractmethod, ABC

class DayBase(ABC):

    @abstractmethod
    def part_1(self) -> int:
        pass

    @abstractmethod
    def part_2(self) -> int:
        pass

    @classmethod
    def get_subclass_name(cls):
        return cls.__name__

    def get_input(self) -> list[str]:
        with open(f"../data/{self.get_subclass_name().lower()}.txt", 'r') as f:
            lines = f.read().splitlines()
        return lines