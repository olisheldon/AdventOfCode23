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
class PartCategoryRange:
    part_category: PartCategory
    lower_bound: int = 0
    upper_bound: int = 4000

    def merge(self, part_category_range: 'PartCategoryRange') -> None:
        assert self.part_category == part_category_range.part_category

        self.lower_bound = min(self.lower_bound, part_category_range.lower_bound)
        self.upper_bound = max(self.upper_bound, part_category_range.upper_bound)



class PartCategoriesRange:

    def __init__(self):
        self.x_part_category_range: PartCategoryRange = PartCategoryRange(PartCategory.x)
        self.m_part_category_range: PartCategoryRange = PartCategoryRange(PartCategory.m)
        self.a_part_category_range: PartCategoryRange = PartCategoryRange(PartCategory.a)
        self.s_part_category_range: PartCategoryRange = PartCategoryRange(PartCategory.s)

    @staticmethod
    def merge(part_categories_ranges: list['PartCategoriesRange']) -> 'PartCategoriesRange':
        part_categories_range = PartCategoriesRange()
        for part_categories_range in part_categories_ranges:
            part_categories_range.x_part_category_range.merge(part_categories_range.x_part_category_range)
            part_categories_range.m_part_category_range.merge(part_categories_range.m_part_category_range)
            part_categories_range.a_part_category_range.merge(part_categories_range.a_part_category_range)
            part_categories_range.s_part_category_range.merge(part_categories_range.s_part_category_range)
        return part_categories_range
            
    @staticmethod
    def _merge_part_category_ranges(part_category_ranges: list[PartCategoryRange]) -> list[PartCategoryRange]:
        part_category_ranges.sort(key=lambda part_category_range: part_category_range.lower_bound)
        merged = [part_category_ranges[0]]
        for current in part_category_ranges:
            previous = merged[-1]
            if current.lower_bound <= previous.upper_bound:
                previous.upper_bound = max(previous.upper_bound, current.upper_bound)
            else:
                merged.append(current)
        return merged
    
    @staticmethod
    def merge_list(part_category_ranges: list[PartCategoryRange]) -> 'PartCategoriesRange':
        part_categories_range = PartCategoriesRange()
        for part_category_range in part_category_ranges:
            match part_category_range.part_category:
                case PartCategory.x:
                    part_category_range.merge(part_categories_range.x_part_category_range)
                case PartCategory.m:
                    part_category_range.merge(part_categories_range.m_part_category_range)
                case PartCategory.a:
                    part_category_range.merge(part_categories_range.a_part_category_range)
                case PartCategory.s:
                    part_category_range.merge(part_categories_range.s_part_category_range)
                case _:
                    raise RuntimeError(f"part_category_range {part_category_range} is not recognised.")
        return part_categories_range


class RuleComparison:

    def __init__(self, part_category: PartCategory, value: int, comparison: Comparison):
        self.part_category: PartCategory = part_category
        self.value: int = value
        self.comparison: Comparison = comparison

    def __repr__(self) -> str:
        return f"{self.part_category} {self.comparison} {self.value}"
    
    def __call__(self, part_ratings: PartRatings) -> bool:
        return Comparison.query(self.comparison, part_ratings.get_value(self.part_category), self.value)
    
    def get_valid_part_category_range(self) -> PartCategoryRange:
        match self.comparison:
            case Comparison.LESS_THAN:
                return PartCategoryRange(self.part_category, PartRatings.min_value, self.value)
            case Comparison.GREATER_THAN:
                return PartCategoryRange(self.part_category, self.value, PartRatings.max_value)
            case Comparison.NO_COMPARISON:
                return PartCategoryRange(self.part_category, PartRatings.min_value, PartRatings.max_value)
            case _:
                raise RuntimeError(f"RuleComparison {self.comparison} is not recognised.")

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

    @classmethod
    def _paths(cls, tree: 'Rule'):
        root = tree
        rooted_paths = [[root]]
        unrooted_paths = []
        for subtree in (tree._pass_rule, tree._fail_rule):
            if subtree:
                useable, unusable = Rule._paths(subtree)
                for path in useable:
                    unrooted_paths.append(path)
                    rooted_paths.append([root] + path)
                for path in unusable:
                    unrooted_paths.append(path)
        return (rooted_paths, unrooted_paths)

    def get_paths(self):
        a, b = Rule._paths(self)
        return a + b

    @classmethod
    def find_paths(cls, root: 'Rule'):
        if root._pass_rule is None and root._fail_rule is None:
            yield [root]

        for child in (root._pass_rule, root._fail_rule):
            if child:
                for path in cls.find_paths(child):
                    yield [root] + path

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
        # all_paths = self.workflow_container.get_paths()
        # # for path in all_paths:
        # #     print(len(path))

        paths = Rule.find_paths(self.workflow_container._workflows["in"].rules[0])
        paths_to_A = filter(lambda x : x[-1]._pass_outcome == PartRatingOutcome.A, paths)
        # print(list(paths_to_A))
        
        # for path_to_A in paths_to_A:
        #     map(lambda x : x._rule_comparison, path_to_A)
        #     print(path_to_A)
        
        paths_part_category_ranges = []
        for path_to_A in paths_to_A:
            path_part_category_ranges = []
            for path in path_to_A:
                path_part_category_ranges.append(path._rule_comparison.get_valid_part_category_range())
            paths_part_category_ranges.append(path_part_category_ranges)
        
        print(paths_part_category_ranges)
        print(paths_part_category_ranges[0])

        part_categories_ranges = [PartCategoriesRange.merge_list(paths_part_category_range) for paths_part_category_range in paths_part_category_ranges]
        # part_categories_range = PartCategoriesRange.merge_list(paths_part_category_ranges)
        
        part_categories_range = PartCategoriesRange.merge(part_categories_ranges)

        return part_categories_range.x_part_category_range





if __name__ == "__main__":
    day19 = Day19()
    print(day19.part_1())
    print(day19.part_2())
