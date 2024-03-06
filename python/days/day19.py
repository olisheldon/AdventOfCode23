from overrides import override
from aoc23_base import DayBase
from enum import StrEnum, auto
from dataclasses import dataclass


class PartCategory(StrEnum):
    x = auto()
    m = auto()
    a = auto()
    s = auto()


@dataclass(order=True, frozen=True)
class Interval:
    lower: int
    upper: int

    @property
    def valid(self) -> bool:
        return self.length > 0

    @property
    def length(self) -> int:
        return self.upper - self.lower + 1


class Operator(StrEnum):
    LESS_THAN = '<'
    GREATER_THAN = '>'

    @classmethod
    def query(cls, comparison: 'Operator', l_value: int, r_value: int) -> bool:
        match comparison:
            case cls.LESS_THAN:
                return l_value < r_value
            case cls.GREATER_THAN:
                return l_value > r_value
            case _:
                raise RuntimeError(f"Operator {comparison} is not recognised.")

    @classmethod
    def partition(cls, comparison: 'Operator', interval: Interval, partition_value: int) -> tuple[Interval, Interval]:
        '''
        Returns true_interval, false_interval as a tuple
        '''
        match comparison:
            case cls.LESS_THAN:
                return Interval(interval.lower, min(partition_value - 1, interval.upper)), Interval(max(partition_value, interval.lower), interval.upper)
            case cls.GREATER_THAN:
                return Interval(max(partition_value + 1, interval.lower), interval.upper), Interval(interval.lower, min(partition_value, interval.upper))
            case _:
                raise RuntimeError(f"Operator {comparison} is not recognised.")


class Outcome(StrEnum):
    A = auto()
    R = auto()


class Part:

    def __init__(self, part_str: str):
        part_ratings = part_str[1:-1].split(',')
        assert len(part_ratings) == 4

        self.x: int = int(part_ratings[0][2:])
        self.m: int = int(part_ratings[1][2:])
        self.a: int = int(part_ratings[2][2:])
        self.s: int = int(part_ratings[3][2:])

    def get_rating(self, part_category: PartCategory) -> int:
        match part_category:
            case PartCategory.x:
                return self.x
            case PartCategory.m:
                return self.m
            case PartCategory.a:
                return self.a
            case PartCategory.s:
                return self.s
            case _:
                raise RuntimeError(
                    f"PartCategory {part_category} is not recognised.")

    @property
    def rating(self) -> int:
        return self.x + self.m + self.a + self.s


class PartInterval:

    def __init__(self, interval_dict: dict[PartCategory, Interval]):
        self.intervals = interval_dict

    def get_interval(self, part_category: PartCategory) -> Interval:
        return self.intervals[part_category]

    def copy(self) -> 'PartInterval':
        return PartInterval(self.intervals.copy())

    @property
    def valid(self) -> bool:
        return all(interval.valid for interval in self.intervals.values())

    @property
    def length_products(self) -> int:
        return self.intervals[PartCategory.x].length * self.intervals[PartCategory.m].length * self.intervals[PartCategory.a].length * self.intervals[PartCategory.s].length


class Rule:

    def __init__(self, rule_str: str):
        if ':' in rule_str:
            part_category, operator, *value_and_outcome = rule_str
            self.part_category: PartCategory = PartCategory(part_category)
            self.operator: Operator = Operator(operator)
            self.value: int = int("".join(value_and_outcome).split(':')[0])
            self.outcome: str = "".join(value_and_outcome).split(':')[1]
        else:
            self.part_category: PartCategory = PartCategory.x  # arbitrary
            self.operator: Operator = Operator.GREATER_THAN
            self.value: int = -1
            self.outcome: str = rule_str

    def query(self, part: Part) -> bool:
        return Operator.query(self.operator, part.get_rating(self.part_category), self.value)

    def partition(self, part_interval: PartInterval) -> tuple[PartInterval, PartInterval]:
        true_interval, false_interval = Operator.partition(
            self.operator, part_interval.get_interval(self.part_category), self.value)
        true_part_interval, false_part_interval = part_interval.copy(), part_interval.copy()
        true_part_interval.intervals[self.part_category] = true_interval
        false_part_interval.intervals[self.part_category] = false_interval
        return true_part_interval, false_part_interval


class Workflow:

    def __init__(self, workflow_str: str):
        name, rules = workflow_str.split('{')
        self.name: str = name
        self.rules: list[Rule] = list(map(Rule, rules[:-1].split(',')))

    def query_part(self, part: Part) -> list[tuple[Part, str]]:
        further_processing: list[tuple[Part, str]] = []
        for rule in self.rules:
            if rule.query(part):
                further_processing.append((part, rule.outcome))
            else:
                break
        return further_processing

    def query_interval(self, part_interval: PartInterval) -> list[tuple[PartInterval, str]]:
        further_processing: list[tuple[PartInterval, str]] = []
        for rule in self.rules:
            pass_part_interval, fail_part_interval = rule.partition(
                part_interval)
            if pass_part_interval.valid:
                further_processing.append((pass_part_interval, rule.outcome))
            if fail_part_interval.valid:
                part_interval = fail_part_interval
            else:
                break

        return further_processing


class Workflows:

    def __init__(self, workflows: list[Workflow]):
        self.workflows: dict[str, Workflow] = {
            workflow.name: workflow for workflow in workflows}

    def query_part(self, part: Part, query_workflow: str = "in") -> bool:

        # Base cases
        if query_workflow.lower() == str(Outcome.R):
            return False
        if query_workflow.lower() == str(Outcome.A):
            return True

        further_processing = self.workflows[query_workflow].query_part(part)

        valid = False

        for part, target_workflow in further_processing:
            valid = self.query_part(part, target_workflow)

        return valid

    def query_interval(self, part_interval: PartInterval, query_workflow: str = "in") -> list[PartInterval]:
        '''
        Recursive
        '''

        # Base cases
        if query_workflow.lower() == str(Outcome.R):
            return []
        if query_workflow.lower() == str(Outcome.A):
            return [part_interval]

        total_part_intervals = []

        further_processing = self.workflows[query_workflow].query_interval(
            part_interval)

        for part_interval, target_workflow in further_processing:
            total_part_intervals += self.query_interval(
                part_interval, target_workflow)

        return total_part_intervals


class Day19(DayBase):

    def __init__(self):
        super().__init__()
        workflows, parts = self.parse()
        self.parts: list[Part] = parts
        self.workflows: Workflows = Workflows(workflows)

    def parse(self) -> tuple[list[Workflow], list[Part]]:
        i = 0
        workflows: list[Workflow] = []
        parts: list[Part] = []

        while i < len(self.input):
            line = self.input[i]
            if not line:
                break
            workflows.append(Workflow(line))

            i += 1

        while i < len(self.input):
            line = self.input[i]
            if not line:
                break
            parts.append(Part(line))

            i += 1

        return workflows, parts

    @override
    def part_1(self) -> int:
        return sum(part.rating for part in self.parts if self.workflows.query_interval(part))

    @override
    def part_2(self) -> int:
        part_category_intervals = PartInterval(
            {part_category: Interval(1, 4000) for part_category in PartCategory})
        return sum(part_interval.length_products for part_interval in self.workflows.query_interval(part_category_intervals))


if __name__ == "__main__":
    day19 = Day19()
    print(day19.part_1())
    print(day19.part_2())
