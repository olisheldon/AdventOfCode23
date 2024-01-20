from overrides import override
from aoc23_base import DayBase
from enum import Enum, StrEnum, auto
from dataclasses import dataclass
from typing import Any, Callable
from itertools import pairwise
from collections import defaultdict

class Outcome(StrEnum):
    A = auto(),
    R = auto(),

class PartCategory(StrEnum):
    x = auto(),
    m = auto(),
    a = auto(),
    s = auto(),

class PartRatings:

    min_value: int = 0
    max_value: int = 4000

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

    def __repr__(self) -> str:
        return f"{self.part_category} {self.comparison} {self.value}"
    
    def __call__(self, part_ratings: PartRatings) -> bool:
        return Comparison.query(self.comparison, part_ratings.get_value(self.part_category), self.value)

class Rule:

    def __init__(self, rule: RuleComparison, outcome: 'str | Outcome'):
        self._rule: RuleComparison = rule
        self._outcome: 'str | Outcome' = outcome
        self._next_rule: 'Rule | None' = None

    def __repr__(self) -> str:
        return f"Rule({self._rule}, {self._outcome}, ({self._next_rule.__repr__()}))"

    def set_next(self, rule: 'Rule') -> 'Rule':
        self._next_rule = rule
        return rule

    def get_next(self) -> 'Rule | None':
        return self._next_rule
    
    def handle(self, part_ratings: PartRatings) -> Outcome | str | None:
        if self._rule(part_ratings):
            return self._outcome
        else:
            if self._next_rule:
                return self._next_rule.handle(part_ratings)
        return None
    
    def get_paths(self) -> tuple[str | Outcome, 'None | Rule']:
        return self._outcome, self._next_rule
    
    def get_values_in_range(self):
        match self._rule.comparison:
            case Comparison.LESS_THAN:
                return PartRatings.min_value, self._rule.value
            case Comparison.GREATER_THAN:
                return self._rule.value, PartRatings.max_value
            case _:
                raise RuntimeError()



class Workflow:

    def __init__(self, name: str, init_rule: Rule, end_outcome: Outcome | str):
        self.name: str = name
        self.init_rule: Rule = init_rule
        self.end_outcome: Outcome | str = end_outcome

    def get_paths(self) -> dict[str | Outcome, list[Rule]]:
        paths: dict[str | Outcome, list[Rule]] = defaultdict(list)
        rules: list[Rule] = [self.init_rule]
        rule = self.init_rule
        while rule:
            rule_paths: tuple[str | Outcome, 'None | Rule'] = rule.get_paths()
            pass_outcome: str | Outcome = rule_paths[0]
            fail_outcome: None | Rule = rule_paths[1]

            paths[pass_outcome] = rules

            if not fail_outcome:
                paths[self.end_outcome] = rules
            else:
                rule = fail_outcome            
                rules.append(rule)

            rule = rule.get_next()
        
        return paths


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
        
        raise RuntimeError(f"outcome is not a string, {outcome}")
    
    def get_paths(self, workflow_name: str = "in") -> dict[str | Outcome, list[Rule]]:
        paths: dict[str | Outcome, list[Rule]] = defaultdict(list)

        workflow_paths: dict[str, dict[str | Outcome, list[Rule]]] = {}
        for workflow_name, workflow in self._workflows.items():
            workflow_paths[workflow_name] = workflow.get_paths()

        for workflow_name, workflow in workflow_paths.items():
            for outcome, rules in workflow.items():
                paths[outcome] += rules
        
        return paths




    
    # def get_paths(self, workflow_name: str = "in") -> dict[Outcome, list[list[Rule]]]:
    #     paths: dict[Outcome, list[list[Rule]]] = {outcome : [] for outcome in Outcome}

    #     workflow_paths: dict[str, dict[str | Outcome, list[Rule]]] = {}
    #     for workflow_name, workflow in self._workflows.items():
    #         workflow_paths[workflow_name] = workflow.get_paths()

    #     for workflow_name, workflow in workflow_paths.items():
    #         rules_list = []
    #         for outcome, rules in workflow.items():
    #             rules_list += rules
    #             while outcome not in Outcome._member_names_:
    #                 workflow_path = workflow_paths[outcome]
    #                 workflow = self._workflows[outcome]
    #                 rules = workflow_path[outcome]
    #                 rules_list += rules



    #             paths[Outcome[outcome]].append(rules_list)
        
    #     return paths
        


        

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
                rules.append(Rule(rule, outcome))
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
        workflows_list, part_ratings_list = self.parse()
        workflow_container = WorkflowContainer({workflow.name : workflow for workflow in workflows_list})
        paths = workflow_container.get_paths()
        for path in paths.items():
            print(path)

        rule_comparisons: list[Rule] = []
        path_outcome_acceptance = paths["A"]
        for rule in path_outcome_acceptance:
            rule_comparisons.append(rule)

        range_values = {part_category : 0 for part_category in PartCategory}
        

        for rule in rule_comparisons:
            range_values[rule._rule.part_category] = abs(rule.get_values_in_range()[0] - rule.get_values_in_range()[1])
        
        print(range_values)
        from functools import reduce
        return reduce(lambda x, y: x*y, range_values.values())


if __name__ == "__main__":
    day19 = Day19()
    print(day19.part_1())
    print(day19.part_2())
