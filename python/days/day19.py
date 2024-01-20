from overrides import override
from aoc23_base import DayBase
from enum import Enum, StrEnum, auto
from dataclasses import dataclass
from typing import Any, Callable
from itertools import pairwise
from collections import defaultdict

class PartRatingOutcome(StrEnum):
    A = auto(),
    R = auto(),
    NOT_DETERMINED = auto(),

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
    NO_COMPARISON = 'NO_COMPARISON',

    @classmethod
    def query(cls, comparison: 'Comparison', l_value: int, r_value: int) -> bool:
        match comparison:
            case cls.LESS_THAN:
                return l_value < r_value
            case cls.GREATER_THAN:
                return l_value > r_value
            case cls.NO_COMPARISON:
                return True
            case _:
                raise RuntimeError(f"Comparison {comparison} is not recognised.")

@dataclass
class Range:
    lower_bound: int
    upper_bound: int

class RuleComparison:

    def __init__(self, part_category: PartCategory, value: int, comparison: Comparison):
        self.part_category: PartCategory = part_category
        self.value: int = value
        self.comparison: Comparison = comparison

    def __repr__(self) -> str:
        return f"{self.part_category} {self.comparison} {self.value}"
    
    def __call__(self, part_ratings: PartRatings) -> bool:
        return Comparison.query(self.comparison, part_ratings.get_value(self.part_category), self.value)
    
    def get_valid_range(self) -> Range:
        match self.comparison:
            case Comparison.LESS_THAN:
                return Range(PartRatings.min_value, self.value)
            case Comparison.GREATER_THAN:
                return Range(self.value, PartRatings.max_value)
            case Comparison.GREATER_THAN:
                return Range(PartRatings.min_value, PartRatings.max_value)
            case _:
                raise RuntimeError()
            

class Rule:

    def __init__(self, rule_comparison: RuleComparison, outcome: str):
        self._rule_comparison: RuleComparison = rule_comparison
        self._pass_outcome: str = outcome
        self._pass_rule: 'Rule | None' = None
        self._fail_rule: 'Rule | None' = None

    def __repr__(self) -> str:
        return f"Rule({self._rule_comparison}, {self._pass_outcome})"

    def set_next_pass_rule(self, rule: 'Rule') -> 'Rule':
        self._pass_rule = rule
        return rule

    def set_next_fail_rule(self, rule: 'Rule') -> 'Rule':
        self._fail_rule = rule
        return rule
    
    def __call__(self, part_ratings: PartRatings) -> PartRatingOutcome:
        if self._rule_comparison(part_ratings):
            if self._pass_rule:
                return self._pass_rule(part_ratings)
            else:
                return PartRatingOutcome[self._pass_outcome.upper()]
        else:
            if self._fail_rule:
                return self._fail_rule(part_ratings)
            raise RuntimeError()
    
    def get_paths(self, paths: list[list['Rule']] | None = None, outcome_required: PartRatingOutcome = PartRatingOutcome.A) -> list[list['Rule']]:
        if paths is None:
            paths = [[self]]
        else:
            for path in paths:
                path.append(self)

        for path in paths:
            if self._pass_rule:
                path += self._pass_rule.get_paths(paths)
            if self._fail_rule:
                path += self._fail_rule.get_paths(paths)
        
        return paths



    
    # def get_paths(self, paths: defaultdict[PartRatingOutcome, list[list[RuleComparison]]] | None = None) -> defaultdict[PartRatingOutcome, list[list[RuleComparison]]]:
    #     if paths is None:
    #         paths: defaultdict[PartRatingOutcome, list[list[RuleComparison]]] = defaultdict(list)
    #         paths[PartRatingOutcome.NOT_DETERMINED] = [[self._rule_comparison]]
        
    #     for paths_to_explore in paths[PartRatingOutcome.NOT_DETERMINED]:
    #         if self._pass_rule:
    #             new_paths = self._pass_rule.get_paths(paths)
    #             for part_rating_outcome, rule_comparisons in new_paths.items():
    #                 paths[part_rating_outcreturn (rule_comparisons) # not sure about thipathss
    #         else:
    #             paths[PartRatingOutcome[self._pass_outcome.upper()]].append(paths_to_explore)

    #         if self._fail_rule:
    #             new_paths = self._fail_rule.get_paths(paths)
    #             for part_rating_outcome, rule_comparisons in new_paths.items():
    #                 paths[part_rating_outcreturn (rule_comparisons) # not sure about thipathss
    #         else:
    #             paths[PartRatingOutcome[self._pass_outcome.upper()]].append(paths_to_explore)

    #     return paths

class Workflow:

    def __init__(self, name: str, rules: list[Rule]):
        self.name: str = name
        self.rules: list[Rule] = rules

    def __repr__(self) -> str:
        return f"Workflow({self.name}, {self.rules})"
    
    def query(self, part_ratings: PartRatings) -> PartRatingOutcome:
        return self.rules[0](part_ratings)
        

    

class WorkflowContainer:

    def __init__(self, workflows: dict[str, Workflow]):
        self._workflows: dict[str, Workflow] = workflows

    def __repr__(self) -> str:
        return "\n".join(f"{name} : {workflow}" for name, workflow in self._workflows.items())

    def query(self, part_ratings: PartRatings, workflow_name: str = "in") -> PartRatingOutcome:
        workflow = self._workflows[workflow_name]
        return workflow.query(part_ratings)
    
    def get_paths(self, workflow_name: str = "in") -> list[list[Rule]]:
        return self._workflows[workflow_name].rules[0].get_paths()


class Day19(DayBase):
    
    def __init__(self):
        super().__init__()
        workflows_dict, part_ratings_list = self.parse()
        self.workflow_container: WorkflowContainer = WorkflowContainer(workflows_dict)
        self.part_ratings_list: list[PartRatings] = part_ratings_list

    def parse(self) -> tuple[dict[str, Workflow], list[PartRatings]]:
        i = 0
        workflows: list[Workflow] = []
        no_rule_comparison: RuleComparison = RuleComparison(PartCategory.x, 0, Comparison.NO_COMPARISON)
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
                    rule_comparison = RuleComparison(part_category, compare_value, Comparison.LESS_THAN)
                elif '>' in rule_str:
                    rule_comparison = RuleComparison(part_category, compare_value, Comparison.GREATER_THAN)
                else:
                    raise RuntimeError(f"Parsing error, {rule_str} does not contain '<' or '>'")
                
                rules.append(Rule(rule_comparison, outcome))

            rules.append(Rule(no_rule_comparison, end_outcome[:-1])) # interpreting final outcome as a rule that always passes
            workflows.append(Workflow(name, rules))

            i += 1

        # Post processing
        dict_workflows: dict[str, Workflow] = {workflow.name : workflow for workflow in workflows}
        for name, workflow in dict_workflows.items():
            for rule, next_rule in pairwise(workflow.rules):
                rule.set_next_fail_rule(next_rule)
            for rule in workflow.rules:
                if rule._pass_outcome not in PartRatingOutcome._member_names_:
                    rule.set_next_pass_rule(dict_workflows[rule._pass_outcome].rules[0])
                else:
                    rule.set_next_pass_rule(Rule(no_rule_comparison, PartRatingOutcome[rule._pass_outcome]))

        parts: list[PartRatings] = [PartRatings(line) for line in self.input[i + 1:]]

        return dict_workflows, parts
        
                      

    @override
    def part_1(self) -> int:
        return sum(part_rating.total  for part_rating in self.part_ratings_list if self.workflow_container.query(part_rating) is PartRatingOutcome.A)

    @override
    def part_2(self) -> int:
        all_paths = self.workflow_container.get_paths()
        print(len(all_paths))
        print(len(all_paths[0]))
        all_paths_to_A: list[list[Rule]] = []
        # for path in all_paths:
        #     if path[-1]._pass_outcome.upper() == PartRatingOutcome.A:
        #         all_paths_to_A.append(path)
        



if __name__ == "__main__":
    day19 = Day19()
    print(day19.part_1())
    print(day19.part_2())
