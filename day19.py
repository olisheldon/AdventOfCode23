from pathlib import Path
import argparse
from overrides import override
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
    def rating(self) -> int:
        return sum(interval.lower for interval in self.intervals.values())

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


class Day19:

    def __init__(self, filepath: Path):
        self.filepath = filepath
        workflows, parts = self.parse()
        self.parts: list[dict[str, int]] = parts
        self.workflows: Workflows = Workflows(workflows)

    def parse_file(self) -> list[str]:
        with open(self.filepath, 'r', encoding="utf-8") as f:
            return f.read().splitlines()

    def parse(self) -> tuple[list[Workflow], list[dict[str, int]]]:
        i = 0
        workflows: list[Workflow] = []
        parts: list[dict[str, int]] = []

        while i < len(self.parse_file()):
            line = self.parse_file()[i]
            if not line:
                break
            workflows.append(Workflow(line))

            i += 1

        i += 1

        while i < len(self.parse_file()):
            line = self.parse_file()[i]
            if not line:
                break
            cat_and_vals = line[1:-1].split(',')
            parts.append({cat_and_val[0]: int(cat_and_val[2:])
                         for cat_and_val in cat_and_vals})
            i += 1

        return workflows, parts

    def part_1(self) -> int:
        part_intervals = list(PartInterval({PartCategory(k): Interval(
            v, v + 1) for k, v in part.items()}) for part in self.parts)
        return sum(queried_part_interval.rating for part_interval in part_intervals for queried_part_interval in self.workflows.query_interval(part_interval))

    def part_2(self) -> int:
        part_category_intervals = PartInterval(
            {part_category: Interval(1, 4000) for part_category in PartCategory})
        return sum(part_interval.length_products for part_interval in self.workflows.query_interval(part_category_intervals))


if __name__ == "__main__":
    INPUT_FILEPATH = Path(__file__).parent / "data" / \
        f"{Path(__file__).stem}.txt"
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?',
                        default=INPUT_FILEPATH, help=f"Path to data for {Path(__file__).stem}")
    args = parser.parse_args()

    day19 = Day19(Path(args.input).absolute())
    print(day19.part_1())
    print(day19.part_2())
