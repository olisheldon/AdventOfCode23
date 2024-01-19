from overrides import override
from aoc23_base import DayBase
from enum import Enum, StrEnum, auto
from dataclasses import dataclass
from typing import Any, Callable
from itertools import pairwise

class Outcome(StrEnum):
    A = auto(),
    R = auto(),

class PartCategory(StrEnum):
    x = auto(),
    m = auto(),
    a = auto(),
    s = auto(),

class PartRatings:

    def __init__(self, part_str: str):
        x, m, a, s = part_str[1:-1].split(',')
        self.x: int = int(x[2:])
        self.m: int = int(m[2:])
        self.a: int = int(a[2:])
        self.s: int = int(s[2:])

    def __repr__(self) -> str:
        return f"PartRatings({self.x}, {self.m}, {self.a}, {self.s})"

    def get_value(self, part_category: PartCategory) -> int:
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
                raise TypeError(f"PartCategory {part_category} does not have expected enumerations.")
        
    @property
    def total(self) -> int:
        return self.x + self.m + self.a + self.s

class Comparison(StrEnum):
    LESS_THAN = '<',
    GREATER_THAN = '>',

    @classmethod
    def query(cls, comparison: 'Comparison', l_value: int, r_value: int) -> bool:
        match comparison:
            case cls.LESS_THAN:
                return l_value < r_value
            case cls.GREATER_THAN:
                return l_value > r_value

class RuleComparison:

    def __init__(self, part_category: PartCategory, value: int, comparison_str: Comparison):
        self.part_category: PartCategory = part_category
        self.value: int = value
        self.comparison: Comparison = Comparison(comparison_str)
    
    def __call__(self, part_ratings: PartRatings) -> bool:
        return Comparison.query(self.comparison, part_ratings.get_value(self.part_category), self.value)


class Rule:

    def __init__(self, part_category: PartCategory, rule: RuleComparison, outcome: 'str | Outcome'):
        self._part_category: PartCategory = part_category
        self._rule: RuleComparison = rule
        self._outcome: 'str | Outcome' = outcome
        self._next_rule: 'Rule | None' = None

    def __repr__(self) -> str:
        return f"Rule({self._part_category}, {self._rule}, {self._outcome}, ({self._next_rule.__repr__()}))"

    def set_next(self, rule: 'Rule') -> 'Rule':
        self._next_rule = rule
        return rule
    
    def handle(self, part_ratings: PartRatings) -> Outcome | str | None:
        if self._rule(part_ratings):
            return self._outcome
        else:
            if self._next_rule:
                return self._next_rule.handle(part_ratings)
        return None

@dataclass(frozen=True)
class Workflow:
    name: str
    init_rule: Rule
    end_outcome: Outcome | str

class WorkflowContainer:

    def __init__(self, workflows: dict[str, Workflow]):
        self._workflows: dict[str, Workflow] = workflows

    def query(self, part_ratings: PartRatings, workflow_name: str = "in") -> Outcome:
        workflow = self._workflows[workflow_name]
        outcome: Outcome | str | None = workflow.init_rule.handle(part_ratings)

        if outcome is None:
            if isinstance(workflow.end_outcome, Outcome):
                return workflow.end_outcome
            else:
                outcome = workflow.end_outcome

        if outcome in Outcome._member_names_:
            return Outcome[outcome]
        elif isinstance(outcome, str):
            return self.query(part_ratings, outcome)
        
        raise RuntimeError()
        

class Day19(DayBase):
    
    def __init__(self):
        super().__init__()

    def parse(self) -> tuple[list[Workflow], list[PartRatings]]:
        i = 0
        workflows: list[Workflow] = []
        while self.input[i]:
            line = self.input[i]
            name, rules_str = line.split('{')
            *list_rules_and_outcome_str, end_outcome = rules_str.split(',')
            rules: list[Rule] = []
            for rule_str_and_outcome in list_rules_and_outcome_str:
                rule_str, outcome = rule_str_and_outcome.split(':')
                part_category = PartCategory(rule_str[0])
                compare_value = int(rule_str[2:])
                if '<' in rule_str:
                    rule = RuleComparison(part_category, compare_value, Comparison('<'))
                elif '>' in rule_str:
                    rule = RuleComparison(part_category, compare_value, Comparison('>'))
                else:
                    raise RuntimeError(f"Parsing error, {rule_str} does not contain '<' or '>'")
                if outcome in PartCategory._member_names_:
                    outcome = PartCategory(outcome)
                rules.append(Rule(part_category, rule, outcome))
            for rule, next_rule in pairwise(rules):
                rule.set_next(next_rule)
            workflows.append(Workflow(name, rules[0], end_outcome[:-1]))

            i += 1
        
        parts: list[PartRatings] = [PartRatings(line) for line in self.input[i + 1:]]

        return workflows, parts
        
                      

    @override
    def part_1(self) -> int:
        workflows_list, part_ratings_list = self.parse()
        workflow_container = WorkflowContainer({workflow.name : workflow for workflow in workflows_list})
        return sum(part_rating.total  for part_rating in part_ratings_list if workflow_container.query(part_rating) is Outcome.A)

    @override
    def part_2(self) -> int:
        pass

if __name__ == "__main__":
    day19 = Day19()
    print(day19.part_1())
    print(day19.part_2())
